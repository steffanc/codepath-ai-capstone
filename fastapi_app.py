import chainlit as cl
from chainlit.context import init_ws_context
from chainlit.session import WebsocketSession, ws_sessions_id
from chainlit.utils import mount_chainlit
from fastapi import FastAPI, Request

from youtube import get_video_details_with_transcript

# Create a FastAPI app
app = FastAPI()


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
    message_history.append({"role": "system", "content": f"Metadata and transcript for video id {video_id}: {metadata}"})
    cl.user_session.set("message_history", message_history)


# Mount the Chainlit app
mount_chainlit(app=app, target="chainlit_app.py", path="/chainlit")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
