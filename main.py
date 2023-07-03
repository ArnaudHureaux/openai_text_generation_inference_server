from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import json
import random
import openai
import asyncio
import os

load_dotenv()

app = FastAPI()

openai.api_key = "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"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 3900


class RequestBody(BaseModel):
    inputs: str
    parameters: Optional[dict]


async def get_openai_stream_data(request):
    events = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": request.inputs}],
        stream=True,
        temperature=request.parameters['temperature'] if 'parameters' in request else DEFAULT_TEMPERATURE,
        max_tokens=request.parameters['max_tokens'] if 'parameters' in request else DEFAULT_MAX_TOKENS,
    )

    gen_text = ""
    end = "\n\n"
    tok_cnt = 0
    async for event in events:
        # print(event)
        try:
            content = event['choices'][0]['delta']['content']
        except KeyError:
            content = None
        finish_reason = event['choices'][0]['finish_reason']
        tok_cnt += 1
        if content or finish_reason != None:
            if content:
                gen_text += content
            final_text = None
            details = None
            special = False
            if finish_reason != None:
                final_text = gen_text
                special = True
                details = {"finish_reason": finish_reason,
                           "generated_tokens": tok_cnt-1, "seed": None}
                end = "\n\n\n"
            tok = {
                "token": {
                    "id": random.randrange(0, 2**32),
                    "text": content,
                    "logprob": 0,
                    "special": special,
                },
                "generated_text": final_text,
                "details": details
            }
            json_string = json.dumps(tok, separators=(',', ':'))
            result = f"data:{json_string}"
            print(result)
            yield result + end
            await asyncio.sleep(0)  # Allow other tasks to run


@app.post("/generate_stream")
async def chat_completions(request: RequestBody):
    return StreamingResponse(get_openai_stream_data(request), media_type="text/event-stream", headers={"Content-Type": "text/event-stream"})
