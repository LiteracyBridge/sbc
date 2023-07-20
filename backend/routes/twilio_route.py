from datetime import datetime
import string
import time
import json
from json import JSONDecodeError
from typing import Optional, Dict, Any, List

import boto3 as boto3
import pg8000.native
from pg8000.native import identifier, literal
from botocore.exceptions import ClientError
from pg8000.native import Connection
from sqlalchemy import select, or_
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from sqlalchemy.orm import Session, joinedload, subqueryload
from models import ProjectUser, User, get_db, MessageReceived, MessageSent
from functools import reduce
from fastapi import APIRouter, Depends, HTTPException, Request
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


def setupTwilio():
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

    def sendTwilio(to_number, message, channel):
        if channel == "w":  # to_number.startswith("whatsapp:"):
            from_number = settings.twilio_whatapp_number
        else:
            from_number = settings.twilio_sms_number
        try:
            client.messages.create(body=message, from_=from_number, to=to_number)
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


def set_whatsapp_last_received(connection, user_id):
    update_sql = "UPDATE users SET whatsapp_last_received = NOW() WHERE id = " + str(
        user_id
    )
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


def log_msg_sent_user(
    connection, user_id, msg_id, success, channel, waiting, declined, db: Session
):
    if declined is None:
        declined_string = "NULL"
    else:
        declined_string = str(declined)
    insert_sql = f"INSERT INTO msgs_sent_users (msg_sent_id,user_id,success,channel, waiting, declined) VALUES ({str(msg_id)},{str(user_id)},{str(success)},{literal(channel)},{str(waiting)},{declined_string})"
    print(insert_sql)
    connection.run(insert_sql)


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
def outgoingMessage(
    connection,
    user_id,
    sender,
    prj_id,
    message,
    project_name,
    db: Session,
    related_item=None,
):
    # Save the message in the database
    record: MessageSent = MessageSent()
    record.prj_id = prj_id
    record.message = message
    record.user_id_sending = user_id
    record.related_item = related_item
    record.sent_time = datetime.now()
    db.add(record)
    db.commit()
    db.refresh(record)

    # insert_sql = (
    #     "INSERT INTO msgs_sent (prj_id, message, user_id_sending, related_item) VALUES ("
    #     + str(prj_id)
    #     + ","
    #     + literal(message)
    #     + ","
    #     + str(user_id)
    #     + ","
    # )
    # insert_sql += "NULL" if related_item is None else literal(related_item)
    # insert_sql += ") RETURNING id"
    # print(insert_sql)
    # msg_id = connection.run(insert_sql)[0][0]

    # Send whatsapp messages to users with whatsapp numbers
    sendTwilio = setupTwilio()

    project_users_query = (
        db.query(ProjectUser.user_id).filter(ProjectUser.prj_id == prj_id).subquery()
    )
    whatsapp_users: List[User] = (
        db.query(User)
        .filter(
            ((User.notify_whatsapp == True) & (User.whatsapp != None))
            | ((User.notify_sms == True) & (User.sms != None)),
        )
        .filter(User.id.in_(select(project_users_query)))
        .all()
    )

    # sql = (
    #     "SELECT id, address_as, phone, in_window FROM users_w_numbers WHERE prj_id = "
    #     + literal(prj_id)
    # )
    # connection: Connection = get_db_connection()
    # results = connection.run(sql)
    # print(results)
    for user in whatsapp_users:
        print(user)
        # user_id = result[0]
        # address_as = result[1]
        # phone = result[2]
        in_window = False

        # Check if last message was sent within the last 24 hours
        if user.whatsapp_last_received is not None:
            duration_in_s = time.time() - user.whatsapp_last_received.timestamp()
            in_window = divmod(duration_in_s, 3600)[0] < 24

        channel = "w" if user.whatsapp is not None else "s"
        if in_window:
            success = update_message(
                user.address_as, sender, project_name, message, user.whatsapp, channel
            )
            waiting = False
            declined = False
        else:
            full_message = notify_message(sender, project_name, related_item)
            success = sendTwilio(user.whatsapp, full_message, channel)
            waiting = True
            declined = None

        log_msg_sent_user(
            connection, user_id, record.id, success, channel, waiting, declined, db
        )


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


@router.post("")
@router.get("")
def handler(body: Dict[Any, Any], request: Request, db: Session = Depends(get_db)):
    connection = get_db_connection()

    if request.method == "GET":
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

    elif request.method == "POST":
        try:
            params = body
        except JSONDecodeError as e:
            # API called by Twilio after receipt of message
            print("body", body)
            params = request.query_params
            # Twilio webhook for SMS/Whatsapp
            phone_number = params["From"]
            (
                user_id,
                related_msg_id,
                channel,
                address_as,
                waiting,
                sender,
                project_name,
                msu_id,
                outgoing_message,
            ) = userFromNumber(connection, phone_number)
            message = params["Body"]
            incomingMessage(connection, user_id, related_msg_id, message, channel)
            first_word = message.lstrip().split()[0].lower().rstrip(string.punctuation)
            print("first_word", first_word)
            if waiting and first_word == "no":
                update_log_msg_sent_user(
                    connection,
                    msu_id,
                    success=False,
                    channel=channel,
                    waiting=False,
                    declined=True,
                )
            else:
                if channel == "w":
                    set_whatsapp_last_received(connection, user_id)
                if waiting:  # (and first_word != 'no', which is implied)
                    success = update_message(
                        address_as,
                        sender,
                        project_name,
                        outgoing_message,
                        phone_number,
                        channel,
                    )
                    waiting = not success
                    update_log_msg_sent_user(
                        connection, msu_id, success, channel, waiting, declined=False
                    )

        else:
            # Message broadcast from SBC web app
            prj_id = int(params["prj_id"])
            user_id = int(params["user_id"])
            sender = params["user_name"]
            message = params["message"]
            project_name = params["prj_name"]
            related_item = params["related_item"] if "related_item" in params else None

            outgoingMessage(
                connection,
                user_id,
                sender,
                prj_id,
                message,
                project_name,
                db,
                related_item,
            )

    # Return the response object
    return {}
