from typing import Dict, Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
import openai
from openai.error import RateLimitError
from sqlalchemy.orm import Session
from models import OpenAIUsage, get_db
from pydantic import BaseModel
from schema import ApiResponse
from helpers.config import settings


router = APIRouter()


FORMATS = {
    "list": "Respond only with a list and without any other text.",
    "sentence": "Respond only with one sentence.",
    "paragraph": "Respond only with one paragraph.",
    "item": "Respond only with a single item, not a list or a sentence.",
    "short_answer": "Respond with a list of short sentences, not a paragraph.",
    "essay": "Respond in essay, content must be suited to the question.",
}


def call_openai_api(prompt, context, stop):
    openai.api_key = settings.open_ai_key
    retries = 5
    backoff = 1

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


def gptCompletion(
    prompt, context=None, format_type=None, start="", stop=""
) -> Dict[str, str | None]:
    BASE_CONTEXT = "Act as an expert consultant on social and behavior change for global development in low and middle income countries. Your strongest area of expertise is in the UNICEF Behavioural Drivers Model.\n"
    full_context = BASE_CONTEXT
    start = "" if start is None else start

    if context is not None:
        full_context += "Context:\n" + context + "\n"
    if format_type is not None:
        full_context += FORMATS[format_type]
    if start == "":
        full_prompt = prompt
    else:
        full_prompt = prompt + "\n" + start

    # Post-prompt to control ChatGPT response
    full_prompt += "Don’t justify your answers"

    completion = call_openai_api(full_prompt, full_context, stop)
    response = start + completion

    return {
        "response": response,
        "prompt": full_prompt,
        "context": full_context,
        "error": completion if "Request failed after" in completion else None,
    }


def allowance_ok(prj_id):
    # TODO: log usage and cut off project by returning False if usage is too high in a day/month/etc
    return True


@router.post("")
@router.get("")
@router.put("")
def handler(body: Dict[Any, Any], db: Session = Depends(get_db)):
    result = "BAD METHOD"

    prj_id = body["prj_id"]
    print(body)

    if allowance_ok(prj_id):
        prompt = body["prompt"]
        context = body.get("context", None)
        format_type = body.get("format", None)
        start = body.get("start", "")
        stop = body.get("stop", "")

        result = gptCompletion(prompt, context, format_type, start, stop)

        # Record usage
        usage = OpenAIUsage()
        usage.project_id = prj_id
        usage.prompt = result["prompt"]
        usage.context = result["context"]
        usage.response = result["response"]
        usage.user_id = body["user_id"]

        if result.get("error") is not None:
            usage.status = "error"

        # TODO: track errors

        db.add(usage)
        db.commit()

        return ApiResponse(data=[{"result": result["response"], "id": usage.id}])

    return ApiResponse(
        data=[
            {
                "error": "AI service is not available at the moment. Please try again after some time",
                "result": None,
            }
        ]
    )


class UsageDto(BaseModel):
    id: int
    status: str


@router.post("/usage")
def track_usage(dto: UsageDto, db: Session = Depends(get_db)):
    usage = db.query(OpenAIUsage).filter(OpenAIUsage.id == dto.id).first()

    if usage is None:
        raise HTTPException(status_code=404, detail="Usage not found")

    if usage.status != dto.status:
        usage.status = dto.status

    db.commit()
    db.refresh(usage)

    return ApiResponse(data=[usage])
