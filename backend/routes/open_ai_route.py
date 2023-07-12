from functools import reduce
from typing import Dict, Any
import json
import time
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, Request
import openai
from openai.error import RateLimitError

from schema import ApiResponse
from config import settings


router = APIRouter()


FORMATS = {
    "list": "Respond only with a list and without any other text.",
    "sentence": "Respond only with one sentence.",
    "paragraph": "Respond only with one paragraph.",
    "item": "Respond only with a single item, not a list or a sentence.",
}


########################################################################################################################
# Get a database connection


# def _get_secret(secret_name) -> dict:
#     # Name of the secrets in secrets manager.
#     region_name = "us-west-2"
#     result = None

#     # start = time.time()

#     # Create a Secrets Manager client
#     try:
#         session = boto3.session.Session()
#         client = session.client(service_name="secretsmanager", region_name=region_name)
#     except Exception as e:
#         # print('    Exception getting session client: {}, elapsed: {}'.format(str(e), time.time() - start))
#         raise e

#     # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
#     # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#     # We rethrow the exception by default.

#     try:
#         get_secret_value_response = client.get_secret_value(SecretId=secret_name)
#     except ClientError as e:
#         if e.response["Error"]["Code"] == "DecryptionFailureException":
#             # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
#             # Deal with the exception here, and/or rethrow at your discretion.
#             raise e
#         elif e.response["Error"]["Code"] == "InternalServiceErrorException":
#             # An error occurred on the server side.
#             # Deal with the exception here, and/or rethrow at your discretion.
#             raise e
#         elif e.response["Error"]["Code"] == "InvalidParameterException":
#             # You provided an invalid value for a parameter.
#             # Deal with the exception here, and/or rethrow at your discretion.
#             raise e
#         elif e.response["Error"]["Code"] == "InvalidRequestException":
#             # You provided a parameter value that is not valid for the current state of the resource.
#             # Deal with the exception here, and/or rethrow at your discretion.
#             raise e
#         elif e.response["Error"]["Code"] == "ResourceNotFoundException":
#             # We can't find the resource that you asked for.
#             # Deal with the exception here, and/or rethrow at your discretion.
#             raise e
#         else:
#             raise e
#     else:
#         # Decrypts secret using the associated KMS CMK.
#         # Depending on whether the secret is a string or binary, one of these fields will be populated.
#         if "SecretString" in get_secret_value_response:
#             secret = get_secret_value_response["SecretString"]
#             result = json.loads(secret)
#         # else:
#         # Our secrets are text, so we don't need this.
#         #     decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
#         #     result = decoded_binary_secret

#     # Your code goes here.
#     return result


########################################################################################################################


def call_openai_api(prompt, context, stop):
    # secret = _get_secret("openai")
    openai.api_key = settings.open_ai_key
    retries = 5
    backoff = 1

    # for i in range(retries):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            stop=stop,
            temperature=0.5,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
            ],
        )
        return response["choices"][0]["message"]["content"]
    except RateLimitError as e:
        # if i < retries - 1:
        #     time.sleep(backoff)
        #     backoff *= 2
        #     continue
        # else:
        error_message = f"Request failed after {retries} retries due to rate limiting. Error: {str(e)}"
        print(error_message)
        return error_message

    # url = "https://api.openai.com/v1/chat/completions"
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": f"Bearer {secret['Authorization']}",
    # }
    # data = {
    #     "model": "gpt-3.5-turbo",
    #     "temperature": 0.5,
    #     "stop": stop,
    #     "messages": [
    #         {"role": "system", "content": context},
    #         {"role": "user", "content": prompt},
    #     ],
    # }

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=headers, json=data) as resp:
    #         response = await resp.json()
    #         print("response:")
    #         print(response)
    #         print("tokens used:" + str(response['usage']['total_tokens']))
    #         return response['choices'][0]['message']['content']


# TODO: Check for this error
# WITH API:
#   RateLimitError: That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID 7193111c4ddd952fa8d1ea2267508191 in your message.)
# WITH async http:
# {'error': {'message': 'That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID 2645a3244006b290d746957562e683c1 in your message.)', 'type': 'server_error', 'param': None, 'code': None}}


def gptCompletion(prompt, context=None, format_type=None, start="", stop=""):
    BASE_CONTEXT = "Act as an expert consultant on social and behavior change for global development in low and middle income countries. Your strongest area of expertise is in the UNICEF Behavioural Drivers Model.\n"
    full_context = BASE_CONTEXT

    if context is not None:
        full_context += "Context:\n" + context + "\n"
    if format_type is not None:
        full_context += FORMATS[format_type]
    if start == "":
        full_prompt = prompt
    else:
        full_prompt = prompt + "\n" + start

    completion = call_openai_api(full_prompt, full_context, stop)
    response = start + completion

    return response


def allowance_ok(prj_id):
    # TODO: log usage and cut off project by returning False if usage is too high in a day/month/etc
    return True


# Rewrite this lambda to use as fastapi route endpoint
def lambda_handler(event, context):
    result = "BAD METHOD"
    request_id = event["x-amz-request-id"]
    print(request_id)
    # bodystring = event['body-json']
    params = event["body-json"]  # json.loads(event)
    prj_id = params["prj_id"]
    if allowance_ok(prj_id):
        prompt = params["prompt"]
        context = params["context"] if "context" in params else None
        format_type = params["format"] if "format" in params else None
        start = params["start"] if "start" in params else ""
        stop = params["stop"] if "stop" in params else ""

        # def process():
        response = gptCompletion(prompt, context, format_type, start, stop)
        s3 = boto3.client("s3")
        BUCKET_NAME = "sbc-temp"
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{request_id}.json",
            Body=json.dumps(response),
            ContentType="application/json",
        )

        # asyncio.run(process())

        return {
            "statusCode": 200,
            "body": json.dumps(request_id),
            "headers": {
                "Content-Type": "application/json",
            },
        }
    else:
        result = "LIMIT REACHED"
    return {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": json.dumps(result, default=str),
    }


@router.post("")
@router.get("")
@router.put("")
def handler(body: Dict[Any, Any], request: Request):
    result = "BAD METHOD"
    request_id = request.headers.get("x-amz-request-id", str(uuid4()))

    # bodystring = event['body-json']
    # params = request.body  # json.loads(event)
    prj_id = body["prj_id"]
    print(body)

    if allowance_ok(prj_id):
        prompt = body["prompt"]
        context = body["context"] if "context" in body else None
        format_type = body["format"] if "format" in body else None
        start = body["start"] if "start" in body else ""
        stop = body["stop"] if "stop" in body else ""

        # def process():
        response = gptCompletion(prompt, context, format_type, start, stop)
        # s3 = boto3.client("s3")
        # BUCKET_NAME = "sbc-temp"
        # s3.put_object(
        #     Bucket=BUCKET_NAME,
        #     Key=f"{request_id}.json",
        #     Body=json.dumps(response),
        #     ContentType="application/json",
        # )
        # # asyncio.run(process())

        return {"result": response}
    else:
        result = "LIMIT REACHED"

    return {"result": result}


# if __name__ == "__main__":

#     def test_main():
#         get_msg = '{"httpMethod":"GET","queryStringParameters":{"prj_id":"28","format":"item","prompt":"What are some acronyns I should know?","start":"","stop":"5."}}'
#         print(lambda_handler(json.loads(get_msg), None))

#     test_main()
