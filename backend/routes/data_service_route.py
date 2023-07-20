import json
import time
import traceback

# from amplio.rolemanager import manager
from functools import reduce
from typing import Dict, List, Optional, Any

import boto3 as boto3
import models
import pg8000.native
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, Request
from models import (
    Activity,
    Monitoring,
    ProjectIndicators,
    Risk,
    TheoryOfChange,
    TheoryOfChangeIndicator,
)
from config import settings
from pg8000 import Connection, Cursor
from pg8000.native import identifier, literal
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, joinedload, subqueryload

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


def get(params):
    result = table = attributes = None
    where_clause = ""
    for name, value in params.items():
        if name == "object":
            table = identifier(value)  # quotes to prevent sql injection
        elif name == "attributes":
            attributes = value
            # split the list, quote each column name, join back together
            columns = attributes.split(",")
            columns = ",".join(map(identifier, columns))
        else:
            if where_clause != "":
                where_clause += " AND "
            where_clause += "(" + identifier(name) + " = " + literal(value)
            where_clause += " OR prj_id IS NULL)" if name == "prj_id" else ")"
    if table is not None and attributes is not None:
        sql = (
            "SELECT "
            + attributes
            + " FROM "
            + table
            + ((" WHERE " + where_clause) if where_clause else "")
        )
        # only lookup tables require a sequence column to order the presentation of options
        # the 'drivers' view is a special exception since it joins a lookup table with project data
        if table.startswith("lu_"):
            sql += " ORDER BY sequence"
        elif table == "drivers":
            sql += " ORDER by parent_id, sequence"
        connection: Connection = get_db_connection()
        print(sql)
        result = connection.run(sql)
    return result


def post(body):
    object = attributes = filter_name = filter_value = None
    object = body["object"]
    attributes = body["attributes"]

    names = values = ""
    for name, value in attributes.items():
        # print('value:',value,type(value),literal(value));
        names += identifier(name) + ","
        literal_value = literal(value)
        if type(value) is list:
            literal_value = "'{" + literal_value[2:-2] + "}'"
        values += literal_value + ","
    names = names[0:-1]
    values = values[0:-1]
    insert_sql = (
        "INSERT INTO "
        + identifier(object)
        + " ("
        + names
        + ") VALUES ("
        + values
        + ") RETURNING id"
    )
    connection: Connection = get_db_connection()
    print(insert_sql)
    id = connection.run(insert_sql)

    return id


def delete(params):
    object = ids = None
    if "object" in params:
        table = params["object"]
        for id in params["ids"]:
            where_clause = literal(id) + ","
        delete_sql = (
            "DELETE FROM "
            + identifier(table)
            + " WHERE id IN ("
            + where_clause[:-1]
            + ")"
        )
        print(delete_sql)
        connection: Connection = get_db_connection()
        connection.run(delete_sql)
    return


def put(body):
    object = attributes = filter_name = filter_value = None
    object = body["object"]
    id = body["id"]
    attributes = body["attributes"]
    set_clause = " SET "
    names = values = ""
    for name, value in attributes.items():
        literal_value = literal(value)
        if type(value) is list:
            literal_value = "'{" + literal_value[2:-2] + "}'"
        set_clause += identifier(name) + " = " + literal_value + ", "
    set_clause = set_clause[0:-2]
    where_clause = " WHERE id = " + literal(id)
    update_sql = "UPDATE " + identifier(object) + set_clause + where_clause
    connection: Connection = get_db_connection()
    print(update_sql)
    connection.run(update_sql)
    return


@router.post("")
@router.get("")
@router.delete("")
@router.put("")
def handler(request: Request, body: Optional[Dict[Any, Any]] = None):
    print(body)
    print(request.query_params)

    start = time.time_ns()
    method = request.method.upper()
    result = {}

    if method == "GET":
        # result = get(event["queryStringParameters"])
        result = get(request.query_params)
    elif method == "POST":
        # bodystring = event["body"]
        # body = json.loads(bodystring)
        result = post(body)
    elif method == "DELETE":
        print("event['queryStringParameters']", request.query_params)
        # print(event)
        # bodystring = event["body"]
        # print("bodystring", bodystring)
        # body = json.loads(bodystring)
        result = delete(body)
    elif method == "PUT":
        # bodystring = event["body"]
        # body = json.loads(bodystring)
        result = put(body)

    # Return the response object
    return result
