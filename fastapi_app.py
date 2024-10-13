import json

import chainlit as cl
import openai
from chainlit.context import init_ws_context
from chainlit.session import WebsocketSession
from chainlit.utils import mount_chainlit
from fastapi import FastAPI, Request
from langsmith.wrappers import wrap_openai

from youtube import get_video_details_with_transcript

# Create a FastAPI app
app = FastAPI()
client = wrap_openai(openai.AsyncClient())


# Basic FastAPI route
@app.get("/youtube-metadata/{session_id}/{video_id}")
async def youtube_metadata(
        request: Request,
        session_id: str,
        video_id: str
):
    ws_session = WebsocketSession.get_by_id(session_id=session_id)
    init_ws_context(ws_session)
    metadata = get_video_details_with_transcript(video_id)
    message_history = cl.user_session.get("message_history", [])
    message_history.append({
        "role": "system",
        "content": f"Metadata and transcript for YouTube video id {video_id}: {metadata}"}
    )
    cl.user_session.set("message_history", message_history)


@app.get("/youtube-timestamp/{session_id}/{video_id}/{timestamp_seconds}")
async def youtube_metadata(
        request: Request,
        session_id: str,
        video_id: str,
        timestamp_seconds: str
):
    ws_session = WebsocketSession.get_by_id(session_id=session_id)
    init_ws_context(ws_session)

    print(f'timestamp_seconds: {timestamp_seconds}')
    message_history = cl.user_session.get("message_history", [])
    message_history.append({
        "role": "system",
        "content": json.dumps({"video_id": video_id, "timestamp_seconds": timestamp_seconds})

    })
    cl.user_session.set("message_history", message_history)


# Mount the Chainlit app
mount_chainlit(app=app, target="chainlit_app.py", path="/chainlit")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
