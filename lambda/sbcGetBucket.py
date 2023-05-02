import json
from typing import Optional

import boto3 as boto3
from botocore.exceptions import ClientError
import os
# import openai

from functools import reduce


########################################################################################################################
# Get a database connection

def get_response_from_s3(request_id):
    s3 = boto3.client('s3')
    BUCKET_NAME = 'sbc-temp'
    try:
        response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=f"{request_id}.json"
        )
        return json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        print(f"Error retrieving response from S3: {e}")
        return None


def lambda_handler(event, context):
    params = event['queryStringParameters']
    request_id = params['request_id']
    response = get_response_from_s3(request_id)
    if response is None:
        statusCode = 404
        body = f"Error retrieving request id {request_id}"
        content_type = "application/txt"
    else:
        statusCode = 200
        body = json.dumps(response,default=str)
        content_type = "application/json"
    return {
        "statusCode": statusCode,
        "headers": {"Access-Control-Allow-Origin": "*","Content-Type":content_type},
        "body": body
    }



if __name__ == '__main__':
    def test_main():
        get_msg = '{"httpMethod":"GET","queryStringParameters":{"request_id":"52aabd0e-e784-4e9f-b25f-c5e21c33fec9"}}'
        print(lambda_handler(json.loads(get_msg),None))
        
    test_main()
