from datetime import datetime
import string
import time
import json
from json import JSONDecodeError
from typing import Annotated, Optional, Dict, Any, List
from pydantic import BaseModel
import boto3 as boto3
import pg8000.native
from pg8000.native import identifier, literal
from botocore.exceptions import ClientError
from pg8000.native import Connection
from sqlalchemy import select, or_
from twilio.http import response
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from sqlalchemy.orm import Session, joinedload, subqueryload
from models import (
    MessageSentToUser,
    ProjectUser,
    Stakeholder,
    User,
    get_db,
    MessageReceived,
    MessageSent,
    Project,
)
from functools import reduce
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from config import settings

router = APIRouter()


def get_db_connection():
    parms = {
        "database": settings.db_name,
        "user": settings.db_user,
        "password": settings.db_password,
        "host": settings.db_host,
        "port": settings.db_port,
    }

    _db_connection = pg8000.native.Connection(**parms)
    return _db_connection


########################################################################################################################


def send_twilio(to_number, message, channel):
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    from_number = settings.twilio_whatapp_number

    if channel != "w":  # to_number.startswith("whatsapp:"):
        from_number = settings.twilio_sms_number

    try:
        resp = client.messages.create(body=message, from_=from_number, to=to_number)
        print(resp)
        return {"success": True, "response": resp}
    except TwilioRestException as e:
        print(f"Error: {e.msg}")
        return {"success": False, "response": {}}


def setupTwilio():
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

    def sendTwilio(to_number, message, channel):
        from_number = settings.twilio_whatapp_number

        if channel != "w":  # to_number.startswith("whatsapp:"):
            from_number = settings.twilio_sms_number

        try:
            resp = client.messages.create(body=message, from_=from_number, to=to_number)
            print(resp)
            return True
        except TwilioRestException as e:
            print(f"Error: {e.msg}")
            return False

    return sendTwilio


def userFromNumber(connection, from_number):
    sql = """SELECT u.id AS receiver_id, ms.id AS msg_id, u.address_as as receiver, msu.waiting,
                    u2.address_as AS sender, p.name AS project_name, msu.id AS msu_id, ms.message
            FROM users u
            LEFT JOIN msgs_sent_users msu ON msu.user_id = u.id
            LEFT JOIN msgs_sent ms ON msu.msg_sent_id = ms.id
            LEFT JOIN users u2 ON ms.user_id_sending = u2.id
            LEFT JOIN projects p ON  ms.prj_id = p.id
            """
    if from_number.startswith("whatsapp:"):
        sql += "WHERE msu.channel = 'w' AND u.whatsapp = " + literal(from_number[9:])
        channel = "w"
    else:
        sql += "WHERE msu.channel = 's' AND u.sms = " + literal(from_number)
        channel = "s"
    sql += "ORDER BY ms.sent_time DESC LIMIT 1"
    print(sql)
    result = connection.run(sql)

    if len(result) == 1:
        receiver_id = result[0][0]
        related_msg_id = result[0][1]
        receiver_address_as = result[0][2]
        waiting = result[0][3]
        sender = result[0][4]
        project_name = result[0][5]
        msu_id = result[0][6]
        message = result[0][7]

    return (
        receiver_id,
        related_msg_id,
        channel,
        receiver_address_as,
        waiting,
        sender,
        project_name,
        msu_id,
        message,
    )


def set_whatsapp_last_received(connection, user_id, stakeholder_id):
    update_sql = f"UPDATE {'users' if user_id is not None else 'stakeholders'} SET whatsapp_last_received = NOW() WHERE id = {str(user_id)}"

    print(update_sql)
    connection.run(update_sql)


def incomingMessage(connection, user_id, related_msg_id, message, channel):
    insert_sql = (
        "INSERT INTO msgs_received (message,user_id,related_msg_id,channel) VALUES ("
        + literal(message)
        + ","
        + str(user_id)
        + ","
        + str(related_msg_id)
        + ", "
        + literal(channel)
        + ")"
    )
    print(insert_sql)
    connection.run(insert_sql)


def update_message(address_as, sender, project_name, message, phone, channel):
    WHATSAPP_MAX_LENGTH = int(1600 * 0.95)
    sendTwilio = setupTwilio()

    intro_message = (
        "Hello "
        + address_as
        + ",\n"
        + sender
        + " wanted to share the latest update to the "
        + project_name
        + " program.\n\n"
    )
    intro_message += "Please reply to this text to post your comments.\n------------\n"
    if len(intro_message) + len(message) < WHATSAPP_MAX_LENGTH:
        full_message = intro_message + message
        success = sendTwilio(phone, full_message, channel)
    else:
        success = sendTwilio(phone, intro_message, channel)
        for chunk in chunk_string(message, WHATSAPP_MAX_LENGTH):
            time.sleep(1)
            success = success and sendTwilio(phone, chunk, channel)
    return success


def notify_message(sender, project_name, related_item):
    # Thank you for subscribing to updates about "{{1}}".\n\n
    # {{2}} has just updated the {{3}}.\n\n
    # Would you like details about the update?
    if related_item is None:
        related_item = "program plan"
    message = f'Thank you for subscribing to updates about "{project_name}".\n\n'
    message += f"{sender} has just updated the {related_item} module.\n\n"
    message += "Would you like details about the update?"
    print(message)
    return message


def update_log_msg_sent_user(
    connection, msu_id, success, channel, waiting, declined=None
):
    if declined is None:
        declined_string = "NULL"
    else:
        declined_string = str(declined)
    insert_sql = f"UPDATE msgs_sent_users SET success={str(success)},channel={literal(channel)},waiting={str(waiting)},declined={declined_string} WHERE id={msu_id}"
    print(insert_sql)
    connection.run(insert_sql)


def chunk_string(s, max_chunk):
    start = 0
    while start < len(s):
        # print("start:",start)
        # Try to find a paragraph boundary first
        end = s.rfind("\n\n", start, start + max_chunk)
        new_start = end + 2
        # if end != -1:
        #     print("1st")
        if end == -1:
            # If not found, try to find a single new line
            end = s.rfind("\n", start, start + max_chunk)
            new_start = end + 1
            # if end != -1:
            #     print("2nd")
        if end == -1:
            # If not found, try to find a period
            # print('attempting period')
            end = s.rfind(".", start, start + max_chunk) + 1
            # print('period end',end)
            new_start = end
            # if end != -1:
            #     print("3rd")
        if end == -1:
            # If not found, try to find a space
            end = s.rfind(" ", start, start + max_chunk)
            new_start = end + 1
            # if end != -1:
            #     print("4th")
        # print ("first end:", end)
        if end == -1 or end == start:
            # If not found or reached the end, just break at max_chunk
            end = min(start + max_chunk, len(s))
            new_start = end
            # print("5th")
        # print ("second end:", end)
        yield s[start:end].strip()
        start = new_start


# TODO: move this into a separte route
# TODO: accept list of users & stakeholders in body
# ============= Message Broadcast Route =============
class MessageBroadcastDto(BaseModel):
    project_id: int
    message: str
    related_item: Optional[str]
    stakeholder_ids: List[int]
    user_ids: List[int]
    user_id_sending: int


def send_message(
    receivers: List[User | Stakeholder],
    record: MessageSent,
    project: Project,
    sender: str,
    db: Session,
    to_stakeholders: bool = False,
):
    sendTwilio = setupTwilio()

    for user in receivers:
        in_window = False
        message_sid = None

        # Check if last message was sent within the last 24 hours
        if user.whatsapp_last_received is not None:
            duration_in_s = time.time() - user.whatsapp_last_received.timestamp()
            in_window = divmod(duration_in_s, 3600)[0] < 24

        channel = "w" if user.whatsapp is not None else "s"
        phone = f"whatsapp:{user.whatsapp}" if channel == "w" else f"sms:{user.sms}"
        if in_window:
            success = update_message(
                user.address_as if user.address_as is not None else user.name,
                sender,
                project.name,
                record.message,
                phone,
                channel,
            )
            waiting = False
            declined = False
        else:
            full_message = notify_message(sender, project.name, record.related_item)
            resp = send_twilio(phone, full_message, channel)

            success = resp.get("success", False)
            waiting = True
            declined = None
            message_sid = resp.response.sid if success else None

        # Save to message sent to users table
        msg_sent = MessageSentToUser()
        msg_sent.msg_sent_id = record.user_id_sending
        msg_sent.user_id = None if to_stakeholders else user.id
        msg_sent.success = success
        msg_sent.channel = channel
        msg_sent.waiting = waiting
        msg_sent.declined = declined
        msg_sent.message_sid = message_sid
        msg_sent.stakeholder_id = user.id if to_stakeholders else None

        db.add(msg_sent)
        db.commit()


@router.post("/broadcast")
def broadcast_message(
    body: MessageBroadcastDto,
    db: Session = Depends(get_db),
):
    project_id = body.project_id

    # Save the message in the database
    record: MessageSent = MessageSent()
    record.prj_id = project_id
    record.message = body.message
    record.user_id_sending = body.user_id_sending
    record.related_item = body.related_item
    record.sent_time = datetime.now()

    db.add(record)
    db.commit()
    db.refresh(record)

    sender: User | None = db.query(User).filter(User.id == body.user_id_sending).first()
    project: Project | None = db.query(Project).filter(Project.id == project_id).first()

    # Send whatsapp messages to users with whatsapp numbers
    users: List[User] = []
    if len(body.user_ids) > 0:
        users = (
            db.query(User)
            .filter(
                ((User.notify_whatsapp == True) & (User.whatsapp != None))
                | ((User.notify_sms == True) & (User.sms != None))
            )
            .filter(User.id.in_(body.user_ids))
            .all()
        )

        send_message(
            receivers=users,
            record=record,
            project=project,
            sender=sender.name,
            db=db,
            to_stakeholders=False,
        )

    stakeholders: List[Stakeholder] = []
    if len(body.stakeholder_ids) > 0:
        stakeholders = (
            db.query(Stakeholder)
            .filter((User.whatsapp != None) | ((User.sms != None)))
            .filter(Stakeholder.id.in_(body.stakeholder_ids))
            .all()
        )

        send_message(
            receivers=stakeholders,
            record=record,
            project=project,
            sender=sender.name,
            db=db,
            to_stakeholders=True,
        )


# ============= END: Message broadcast route =============


def getMessages(connection, prj_id, related_item, since_sent_id, since_received_id):
    sql = f"""
    SELECT
        s.id, s.sent_time, s.user_id_sending, s.message, r.id, r.received_time, r.user_id, r.stakeholder_id, r.message
    FROM msgs_sent s
    LEFT JOIN msgs_received r ON s.id = r.related_msg_id
    WHERE s.prj_id = {str(prj_id)} AND
        s.related_item = {literal(related_item)} AND
        (s.id > {str(since_sent_id)} OR r.id > {str(since_received_id)})
    ORDER BY s.id DESC, r.id
    """

    print(sql)

    results = connection.run(sql)
    last = None
    for result in results:
        sent_id = result[0]
        if last != sent_id and sent_id > since_sent_id:
            last = sent_id
        else:
            result[1] = None
            result[2] = None
            result[3] = None

    return results


# ============= START: Twilio Webhook =============
def get_user_or_stakeholder_by_phone(from_number, db: Session):
    """Get user by phone number"""

    phone = from_number[9:] if from_number.startswith("whatsapp:") else from_number

    # First check if the number belongs to a user
    subquery = (
        db.query(User.id)
        .filter((User.whatsapp == phone) | (User.sms == phone))
        .subquery()
    )
    user = (
        db.query(MessageSentToUser)
        .filter(MessageSentToUser.user_id.in_(select(subquery)))
        .options(
            subqueryload(MessageSentToUser.user),
            subqueryload(MessageSentToUser.msg_sent).options(
                subqueryload(MessageSent.project),
                subqueryload(MessageSent.user),
            ),
        )
        .order_by(MessageSentToUser.updated_at.desc())
        .all()
    )

    if len(user) > 0:
        return {"user": user[0], "stakeholder": None}

    # If not, check if the number belongs to a stakeholder
    subquery = (
        db.query(Stakeholder.id)
        .filter((Stakeholder.whatsapp == phone) | (Stakeholder.sms == phone))
        .subquery()
    )
    stakeholder = (
        db.query(MessageSentToUser)
        .filter(MessageSentToUser.stakeholder_id.in_(select(subquery)))
        .order_by(MessageSentToUser.updated_at.desc())
        .options(
            subqueryload(MessageSentToUser.stakeholder),
            subqueryload(MessageSentToUser.msg_sent).options(
                subqueryload(MessageSent.project),
                subqueryload(MessageSent.user),
            ),
        )
        .order_by(MessageSentToUser.updated_at.desc())
        .all()
    )
    return {"user": None, "stakeholder": stakeholder[0]}


@router.post("/webhook")
async def webhook_handler(request: Request, db: Session = Depends(get_db)):
    """
    Twilio webhook for SMS/Whatsapp.
    Handle incoming messages from Twilio and update the database.
    """

    connection = get_db_connection()

    # API called by Twilio after receipt of message
    # print("body", body)
    params = await request.form()
    phone_number = params["From"]
    message = params["Body"]

    original_message_sid = params.get("OriginalRepliedMessageSid")
    data = get_user_or_stakeholder_by_phone(phone_number, db)
    user = data["user"]
    stakeholder = data["stakeholder"]
    message_sent: MessageSent = (
        user.msg_sent if user is not None else stakeholder.msg_sent
    )
    channel = user.channel if user is not None else stakeholder.channel

    # Save received message
    record = MessageReceived()
    record.message = message
    record.user_id = user.user_id if user is not None else None
    record.stakeholder_id = (
        stakeholder.stakeholder_id if stakeholder is not None else None
    )
    record.related_msg_id = (
        stakeholder.msg_sent_id if stakeholder is not None else user.msg_sent_id
    )
    record.channel = channel

    db.add(record)
    db.commit()
    db.refresh(record)

    # (
    #     user_id,
    #     related_msg_id,
    #     channel,
    #     address_as,
    #     waiting,
    #     sender,
    #     project_name,
    #     msu_id,
    #     outgoing_message,
    # ) = userFromNumber(connection, phone_number)

    # incomingMessage(connection, user_id, related_msg_id, message, channel)
    first_word = message.lstrip().split()[0].lower().rstrip(string.punctuation)
    waiting = user.waiting if user is not None else stakeholder.waiting
    address_as = (
        user.user.address_as if user is not None else stakeholder.stakeholder.address_as
    )
    project = (
        user.msg_sent.project if user is not None else stakeholder.msg_sent.project
    )
    sender = (
        user.msg_sent.user.address_as
        if user is not None
        else stakeholder.msg_sent.user.address_as
    )

    print("first_word", first_word)
    if waiting and first_word == "no":
        update_log_msg_sent_user(
            connection,
            message_sent.id,
            success=False,
            channel=record.channel,
            waiting=False,
            declined=True,
        )
    else:
        if channel == "w":
            set_whatsapp_last_received(
                connection, record.user_id, record.stakeholder_id
            )
        if waiting:  # (and first_word != 'no', which is implied)
            success = update_message(
                address_as,
                sender,
                project.name,
                message_sent.message,
                phone_number,
                channel,
            )
            waiting = not success
            update_log_msg_sent_user(
                connection,
                message_sent.id,
                success,
                record.channel,
                waiting,
                declined=False,
            )

    return {}


# ============= END: Twilio Webhook =============


# @router.post("")
@router.get("")
def handler(request: Request, db: Session = Depends(get_db)):
    connection = get_db_connection()

    # if request.method == "GET":
    # request from SBC web app for list of broadcast and received messages
    params = request.query_params
    prj_id = int(params["prj_id"])
    related_item = params["related_item"]
    since_sent_id = int(params["since_sent_id"]) if "since_sent_id" in params else 0
    since_received_id = (
        int(params["since_received_id"]) if "since_received_id" in params else 0
    )
    result = getMessages(
        connection, prj_id, related_item, since_sent_id, since_received_id
    )

    # elif request.method == "POST":
    #     try:
    #         params = body
    #     except JSONDecodeError as e:
    #         # API called by Twilio after receipt of message
    #         print("body", body)
    #         params = request.query_params

    #         # Twilio webhook for SMS/Whatsapp
    #         phone_number = params["From"]
    #         (
    #             user_id,
    #             related_msg_id,
    #             channel,
    #             address_as,
    #             waiting,
    #             sender,
    #             project_name,
    #             msu_id,
    #             outgoing_message,
    #         ) = userFromNumber(connection, phone_number)
    #         message = params["Body"]
    #         incomingMessage(connection, user_id, related_msg_id, message, channel)
    #         first_word = message.lstrip().split()[0].lower().rstrip(string.punctuation)
    #         print("first_word", first_word)
    #         if waiting and first_word == "no":
    #             update_log_msg_sent_user(
    #                 connection,
    #                 msu_id,
    #                 success=False,
    #                 channel=channel,
    #                 waiting=False,
    #                 declined=True,
    #             )
    #         else:
    #             if channel == "w":
    #                 set_whatsapp_last_received(connection, user_id)
    #             if waiting:  # (and first_word != 'no', which is implied)
    #                 success = update_message(
    #                     address_as,
    #                     sender,
    #                     project_name,
    #                     outgoing_message,
    #                     phone_number,
    #                     channel,
    #                 )
    #                 waiting = not success
    #                 update_log_msg_sent_user(
    #                     connection, msu_id, success, channel, waiting, declined=False
    #                 )

    # else:
    #     # Message broadcast from SBC web app
    #     prj_id = int(params["prj_id"])
    #     user_id = int(params["user_id"])
    #     sender = params["user_name"]
    #     message = params["message"]
    #     project_name = params["prj_name"]
    #     related_item = params["related_item"] if "related_item" in params else None

    #     broadcast_message(
    #         connection,
    #         user_id,
    #         sender,
    #         prj_id,
    #         message,
    #         project_name,
    #         db,
    #         related_item,
    #     )

    # Return the response object
    return {}
