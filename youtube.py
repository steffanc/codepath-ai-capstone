import json

from youtube_transcript_api import YouTubeTranscriptApi


def download_youtube_captions_as_json(video_id: str, language: str = 'en'):
    try:
        # Fetch transcript for the video ID in the specified language
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return json.dumps(transcript)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
if __name__ == "__main__":
    video_id = "E3g-zgSmwUs"  # Replace with actual video ID
    download_youtube_captions_as_json(video_id)
