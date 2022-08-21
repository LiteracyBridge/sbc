import json
import time
import traceback
from typing import Optional

import boto3 as boto3
import pg8000.native
from pg8000.native import identifier, literal
from botocore.exceptions import ClientError
from pg8000 import Connection, Cursor
# from amplio.rolemanager import manager
from functools import reduce

########################################################################################################################
# Get a database connection

def _get_secret() -> dict:
    # Name of the secrets in secrets manager.
    secret_name = "lb_stats_test" #lb_stats_access2
    region_name = "us-west-2"

    result = None

    start = time.time()

    # Create a Secrets Manager client
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    except Exception as e:
        print('    Exception getting session client: {}, elapsed: {}'.format(str(e), time.time() - start))
        raise e

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        else:
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            result = json.loads(secret)
        # else:
        # Our secrets are text, so we don't need this.
        #     decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        #     result = decoded_binary_secret

    # Your code goes here.
    return result


_db_connection: Optional[Connection] = None


def get_db_connection() -> Connection:
    global _db_connection
    if _db_connection is None:
        secret = _get_secret()

        parms = {'database': 'impact', 'user': secret['username'], 'password': secret['password'],
                 'host': secret['host'], 'port': secret['port']}

        _db_connection = pg8000.native.Connection(**parms)
    return _db_connection


########################################################################################################################

def get(prj_id,all = True):
    result = table = attributes = None
    
    for name,value in params.items():
        if name == 'object':
            table = identifier(value) # quotes to prevent sql injection
        elif name == 'attributes':
            attributes = value
            # split the list, quote each column name, join back together
            columns = attributes.split(',')
            columns = ','.join(map(identifier,columns))
        else:
            if where_clause == '':
                where_clause = ' WHERE '
            else:
                where_clause += ' AND '
            where_clause += identifier(name) + ' = ' + literal(value)
    if table is not None and attributes is not None:
        sql = "SELECT " + attributes + ' FROM ' + table + where_clause
        connection: Connection = get_db_connection()
        result = connection.run(sql)
    return result



def lambda_handler(event, context):
    start = time.time_ns()
    method = event['httpMethod']
    if method == 'GET':
        all = None
        prj_id = event['queryStringParameters']['prj_id']
        if 'all' in event['queryStringParameters']:
            all = event['queryStringParameters']['all']
        result = get(event['queryStringParameters'])
        get(prj_id,all)
    # elif method == 'POST':
    #     bodystring = event['body']
    #     body = json.loads(bodystring)    
    #     result = post(body)
    # elif method == 'DELETE':
    #     result = delete(event['queryStringParameters'])
    # elif method == 'PUT':
    #     bodystring = event['body']
    #     body = json.loads(bodystring)    
    #     result = put(body)

    # Return the response object
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*","Content-Type":"application/json"},
        "body": json.dumps(result,default=str)
    }


if __name__ == '__main__':
    def test_main():
        event_text_0 = '{"queryStringParameters":{}}'
        event_text_1 = '{"queryStringParameters":{"object":"drivers","filter_name":"id","filter_value":1,"attributes":["id","name","category","parent_id","sequence","sem_id","text_short","text_long"]}}'
        event_text = '{"body":{"object":"drivers","filter_name":"id","filter_value":1,"attributes":["id","name","category","parent_id","sequence","sem_id","text_short","text_long"]}}'
        event = json.loads(event_text)
        print(lambda_handler(event,None))
        
    test_main()
