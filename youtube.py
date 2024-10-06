import isodate  # Library to parse ISO 8601 durations
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Initialize the YouTube Data API client with your API key
API_KEY = 'AIzaSyBkHfBiJS8wsvbBtswR7MDBJeFcOEISf-c'  # Replace with your actual API key
youtube = build('youtube', 'v3', developerKey=API_KEY)


# Function to fetch video metadata and transcript
def get_video_details_with_transcript(video_id, languages=['en']):
    try:
        # Fetch video metadata from the YouTube Data API
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics,status',
            id=video_id
        )
        response = request.execute()

        # Check if the video is found
        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]

            # Extract snippet details (title, description, tags, etc.)
            snippet = video.get('snippet', {})
            title = snippet.get('title')
            description = snippet.get('description')
            tags = snippet.get('tags', [])
            category_id = snippet.get('categoryId')
            published_at = snippet.get('publishedAt')
            channel_id = snippet.get('channelId')
            channel_title = snippet.get('channelTitle')

            # Extract content details (duration, etc.)
            content_details = video.get('contentDetails', {})
            iso_duration = content_details.get('duration')  # ISO 8601 duration format (e.g., PT4M13S)
            duration_seconds = convert_iso_duration_to_seconds(iso_duration)  # Convert to seconds

            # Extract statistics (view count, likes, etc.)
            statistics = video.get('statistics', {})
            view_count = statistics.get('viewCount')
            like_count = statistics.get('likeCount')
            dislike_count = statistics.get('dislikeCount', 'Unavailable')
            comment_count = statistics.get('commentCount')

            # Extract video status (privacy status)
            status = video.get('status', {})
            privacy_status = status.get('privacyStatus')

            # Fetch video transcript using youtube-transcript-api
            transcript_data = None
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_transcript(languages)
                transcript_data = transcript.fetch()
            except Exception as e:
                print(f"Error fetching transcript: {e}")

            # Combine all metadata and transcript into a single dictionary
            return {
                'title': title,
                'description': description,
                'tags': tags,
                'category_id': category_id,
                'published_at': published_at,
                'channel_id': channel_id,
                'channel_title': channel_title,
                'duration_seconds': duration_seconds,
                'view_count': view_count,
                'like_count': like_count,
                'dislike_count': dislike_count,
                'comment_count': comment_count,
                'privacy_status': privacy_status,
                'transcript': transcript_data
            }

        else:
            return None

    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None

# Helper function to convert ISO 8601 duration to seconds
def convert_iso_duration_to_seconds(iso_duration):
    duration = isodate.parse_duration(iso_duration)
    return int(duration.total_seconds())

