import asyncio
import json
import os

import chainlit as cl
import openai
from langsmith.wrappers import wrap_openai

from prompts import SYSTEM_PROMPT

api_key = os.getenv("OPENAI_API_KEY")
endpoint_url = "https://api.openai.com/v1"
client = wrap_openai(openai.AsyncClient(api_key=api_key,
                                        base_url=endpoint_url))

# https://platform.openai.com/docs/models/gpt-4o
gen_kwargs = {
    "model": "chatgpt-4o-latest",
    "temperature": 0.3,
    "max_tokens": 500
}


@cl.on_chat_start
async def on_chart_start():
    message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    cl.user_session.set("message_history", message_history)


@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})

    response_message = await generate_response(client, message_history, gen_kwargs)

    content = response_message.content
    function_result = parse_and_invoke(content)
    if function_result is not None:
        print(f"Function result: {function_result}")

    # Record the AI's response in the history
    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)


async def generate_response(client, message_history, gen_kwargs):
    response_message = cl.Message(content="")
    await response_message.send()

    stream = await client.chat.completions.create(messages=message_history, stream=True, **gen_kwargs)
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)

    await response_message.update()

    return response_message


# Function to safely parse and invoke
def parse_and_invoke(json_string):
    try:
        # Parse the JSON string
        parsed = json.loads(json_string)

        # Extract the function name and parameters
        function_name = parsed.get("function_name")
        parameters = parsed.get("parameters", [])

        # Dynamically get the function by name
        func = globals().get(function_name)

        # Check if the function exists and invoke it with the parameters
        if func and callable(func):
            return func(*parameters)
        else:
            print(f"Function '{function_name}' not found or is not callable.")
            return None

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        # Handle any parsing or invocation errors
        print(f"Error parsing or invoking function: {e}")
        return None


def video_nuggets(video_id, interval_seconds):
    asyncio.create_task(surface_nuggets(video_id, interval_seconds))
    return True

async def surface_nuggets(video_id, interval_seconds):
    while True:
        message_history = cl.user_session.get("message_history", [])
        message_history.append({"role": "system", "content": f"Please surface a fun fact, trivia, insight, or behind-the-scenes detail about YouTube video {video_id} at the latest timestamp."})

        response_message = cl.Message(content="")
        await response_message.send()

        stream = await client.chat.completions.create(messages=message_history, stream=True, **gen_kwargs)
        async for part in stream:
            if token := part.choices[0].delta.content or "":
                await response_message.stream_token(token)

        await response_message.update()

        message_history.append({"role": "assistant", "content": response_message.content})
        cl.user_session.set("message_history", message_history)

        await asyncio.sleep(interval_seconds)
