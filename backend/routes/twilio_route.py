from datetime import datetime
import string
import time
from typing import Annotated, Optional, Dict, Any, List
from pydantic import BaseModel
import boto3 as boto3
import pg8000.native
from pg8000.native import literal
from sqlalchemy import select, or_
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from sqlalchemy.orm import Session, subqueryload
from schema import ApiResponse
from models import (
    MessageSentToUser,
    Stakeholder,
    User,
    get_db,
    MessageReceived,
    MessageSent,
    Project,
)
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from helpers.config import settings

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


def set_whatsapp_last_received(connection, user_id, stakeholder_id):
    update_sql = f"UPDATE users SET whatsapp_last_received = NOW() WHERE id = {user_id}"

    if stakeholder_id is not None:
        update_sql = f"UPDATE stakeholders SET whatsapp_last_received = NOW() WHERE id = {stakeholder_id}"

    print(update_sql)
    connection.run(update_sql)


def get_channel(receiver: User | Stakeholder) -> str:
    return "w" if receiver.whatsapp is not None else "s"


def record_message_sent(
    message_sent: MessageSent,
    receiver: User | Stakeholder,
    to_stakeholder: bool,
    success: bool,
    waiting: bool,
    declined: bool,
    message_sid,
    db: Session,
):
    # Save to message sent to users table
    msg_sent = MessageSentToUser()
    msg_sent.msg_sent_id = message_sent.id
    msg_sent.user_id = receiver.id if not to_stakeholder else None
    msg_sent.success = success
    msg_sent.channel = get_channel(receiver)
    msg_sent.waiting = waiting
    msg_sent.declined = declined
    msg_sent.message_sid = message_sid
    msg_sent.stakeholder_id = receiver.id if to_stakeholder else None

    db.add(msg_sent)
    db.commit()

    return msg_sent


def update_message(
    receiver: User | Stakeholder,
    sender: User,
    project_name: str,
    message_sent: MessageSent,
    to_stakeholder: bool,
    waiting: bool,
    db: Session,
):
    WHATSAPP_MAX_LENGTH = int(1600 * 0.95)
    channel = get_channel(receiver)
    phone = f"whatsapp:{receiver.whatsapp}" if channel == "w" else f"sms:{receiver.sms}"

    intro_message = f"Hello {receiver.address_as},\n\n{sender.address_as} wanted to share the latest update to the {project_name} program.\n\nPlease reply to this text to post your comments.\n------------\n"

    success = False
    message = str(message_sent.message)
    if len(intro_message) + len(message) < WHATSAPP_MAX_LENGTH:
        full_message = intro_message + message
        resp = send_twilio(phone, full_message, channel)

        success = resp.get("success", False)
        message_sid = resp["response"].sid if success else None
        record_message_sent(
            message_sent=message_sent,
            receiver=receiver,
            to_stakeholder=to_stakeholder,
            success=success,
            waiting=waiting,
            declined=False,
            message_sid=message_sid,
            db=db,
        )
    else:
        success = send_twilio(phone, intro_message, channel)
        for chunk in chunk_string(message, WHATSAPP_MAX_LENGTH):
            time.sleep(1)

            resp = send_twilio(phone, chunk, channel)
            success = not resp.get("success", False)
            message_sid = resp["response"].sid if success else None
            record_message_sent(
                message_sent=message_sent,
                receiver=receiver,
                to_stakeholder=to_stakeholder,
                success=success,
                waiting=waiting,
                declined=False,
                message_sid=message_sid,
                db=db,
            )
    return success


def notify_message(sender, project_name, related_item):
    # Thank you for subscribing to updates about "{{1}}".\n\n
    # {{2}} has just updated the {{3}}.\n\n
    # Would you like details about the update?

    address_as = sender.address_as if sender.address_as is not None else sender.name

    if related_item is None:
        related_item = "program plan"
    message = f'Thank you for subscribing to updates about "{project_name}".\n\n'
    message += f"{address_as} has just updated the {related_item} module.\n\n"
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
    message_sent: MessageSent,
    project: Project,
    sender: User,
    db: Session,
    to_stakeholders: bool = False,
):
    for receiver in receivers:
        in_window = False

        # Check if last message was sent within the last 24 hours
        if receiver.whatsapp_last_received is not None:
            duration_in_s = time.time() - receiver.whatsapp_last_received.timestamp()
            in_window = divmod(duration_in_s, 3600)[0] < 24

        if in_window:
            update_message(
                receiver=receiver,
                sender=sender,
                project_name=project.name,
                message_sent=message_sent,
                db=db,
                waiting=False,
                to_stakeholder=to_stakeholders,
            )
        else:
            full_message = notify_message(
                sender, project.name, message_sent.related_item
            )
            channel = "w" if receiver.whatsapp is not None else "s"
            phone = (
                f"whatsapp:{receiver.whatsapp}"
                if channel == "w"
                else f"sms:{receiver.sms}"
            )
            resp = send_twilio(phone, full_message, channel)
            success = bool(resp.get("success", False))

            # Save to message sent to users table
            record_message_sent(
                message_sent=message_sent,
                receiver=receiver,
                to_stakeholder=to_stakeholders,
                success=bool(success),
                waiting=True,
                declined=False,
                message_sid=resp["response"].sid if success else None,
                db=db,
            )


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
            .filter((User.whatsapp != None) | (User.sms != None))
            .filter(User.id.in_(body.user_ids))
            .all()
        )

        send_message(
            receivers=users,
            message_sent=record,
            project=project,
            sender=sender,
            db=db,
            to_stakeholders=False,
        )

    stakeholders: List[Stakeholder] = []
    if len(body.stakeholder_ids) > 0:
        stakeholders = (
            db.query(Stakeholder)
            .filter((Stakeholder.whatsapp != None) | ((Stakeholder.sms != None)))
            .filter(Stakeholder.id.in_(body.stakeholder_ids))
            .all()
        )

        send_message(
            receivers=stakeholders,
            message_sent=record,
            project=project,
            sender=sender,
            db=db,
            to_stakeholders=True,
        )


# ============= END: Message broadcast route =============


# ============= START: Twilio Webhook Handler =============#


def get_message_sent_to_user_by_phone(
    from_number, db: Session, original_message_sid: str | None = None
) -> MessageSentToUser | None:
    """Get user by phone number"""

    phone = from_number[10:] if from_number.startswith("whatsapp:") else from_number
    phone_numbers = [phone, f"+{phone}"]

    # Query for user/stakeholder
    user_subquery = (
        db.query(User.id)
        .filter((User.whatsapp.in_(phone_numbers)) | (User.sms.in_(phone_numbers)))
        .subquery()
    )
    stakeholder_subquery = (
        db.query(Stakeholder.id)
        .filter(
            (Stakeholder.whatsapp.in_(phone_numbers))
            | (Stakeholder.sms.in_(phone_numbers))
        )
        .subquery()
    )
    query = (
        db.query(MessageSentToUser)
        .filter(
            (MessageSentToUser.user_id.in_(select(user_subquery)))
            | (MessageSentToUser.stakeholder_id.in_(select(stakeholder_subquery)))
        )
        .order_by(MessageSentToUser.id.desc())
        .options(
            subqueryload(MessageSentToUser.user),
            subqueryload(MessageSentToUser.stakeholder),
            subqueryload(MessageSentToUser.msg_sent).options(
                subqueryload(MessageSent.project),
                subqueryload(MessageSent.user),
            ),
        )
    )

    # The original message sid is included in the response if the user replied to the message (using whatsapp reply feature).
    # We can use this to find the original message sent to the user.
    #
    # Otherwise, we have to guess which message was sent to the user (see the first query).
    if original_message_sid is not None and original_message_sid != "None":
        query = query.filter(MessageSentToUser.message_sid == original_message_sid)

    msg = query.first()

    if msg is None:
        return None
    # TODO: send error to sentry
    return msg


@router.post("/webhook")
async def webhook_handler(request: Request, db: Session = Depends(get_db)):
    """
    Twilio webhook for SMS/Whatsapp.
    Handle incoming messages from Twilio and update the database.
    """

    connection = get_db_connection()

    # API called by Twilio after receipt of message
    params = await request.form()
    phone_number = str(params["From"])
    message = str(params["Body"])
    original_message_sid = params.get("OriginalRepliedMessageSid")

    user_message: MessageSentToUser | None = get_message_sent_to_user_by_phone(
        phone_number, db, str(original_message_sid)
    )

    if user_message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    channel = user_message.channel

    # Save received message
    record = MessageReceived()
    record.message = message
    record.user_id = user_message.user_id
    record.stakeholder_id = user_message.stakeholder_id
    record.related_msg_id = user_message.msg_sent_id
    record.channel = channel

    db.add(record)
    db.commit()
    db.refresh(record)

    # Send replies
    message_sent: MessageSent = user_message.msg_sent
    project: Project = message_sent.project

    waiting = user_message.waiting
    first_word = message.lstrip().split()[0].lower().rstrip(string.punctuation)

    if waiting and first_word == "no":
        update_log_msg_sent_user(
            connection,
            user_message.id,
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
                receiver=user_message.user
                if user_message.user_id is not None
                else user_message.stakeholder,
                sender=message_sent.user,
                project_name=project.name,
                message_sent=message_sent,
                db=db,
                waiting=False,
                to_stakeholder=user_message.stakeholder_id is not None,
            )

            waiting = not success
            update_log_msg_sent_user(
                connection,
                user_message.id,
                success,
                record.channel,
                waiting,
                declined=False,
            )

    return {}


# ============= END: Twilio Webhook =============


@router.get("")
def get_messages(request: Request, db: Session = Depends(get_db)):
    # request from SBC web app for list of broadcast and received messages
    params = request.query_params
    prj_id = int(params["prj_id"])
    related_item = params["related_item"]
    since_sent_id = int(params["since_sent_id"]) if "since_sent_id" in params else 0
    since_received_id = (
        int(params["since_received_id"]) if "since_received_id" in params else 0
    )

    result = (
        db.query(MessageSent)
        .filter(
            MessageSent.prj_id == prj_id,
            MessageSent.related_item == related_item,
        )
        .options(
            subqueryload(MessageSent.user),
            subqueryload(MessageSent.replies).options(
                subqueryload(MessageReceived.user),
                subqueryload(MessageReceived.stakeholder),
            ),
        )
        .order_by(MessageSent.id.desc())
        .all()
    )

    return ApiResponse(data=result)
