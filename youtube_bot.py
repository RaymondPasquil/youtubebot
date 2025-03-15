import pickle
import os
import random
import openai
from googleapiclient.discovery import build

CREDENTIALS_FOLDER = "credentials/"

# Load OpenAI API Key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Function to load a random authenticated YouTube account
def get_authenticated_youtube():
    token_files = [f for f in os.listdir(CREDENTIALS_FOLDER) if f.endswith("_token.pickle")]
    random_token = random.choice(token_files)

    with open(os.path.join(CREDENTIALS_FOLDER, random_token), 'rb') as token:
        creds = pickle.load(token)

    print(f"Using account: {random_token}")
    return build("youtube", "v3", credentials=creds)

# Function to get comments from a video
def get_video_comments(youtube, video_id):
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText")
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments

# Function to generate AI-based reply
def generate_reply(comment):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Reply to this YouTube comment: {comment}"}]
    )
    return response["choices"][0]["message"]["content"]

# Function to post comment
def post_comment(youtube, video_id, text):
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": text
                    }
                }
            }
        }
    )
    response = request.execute()
    return response

# Main function to execute the process
def comment_on_video(video_id):
    youtube = get_authenticated_youtube()
    comments = get_video_comments(youtube, video_id)
    
    if comments:
        chosen_comment = random.choice(comments)
        reply_text = generate_reply(chosen_comment)
        post_comment(youtube, video_id, reply_text)
        print(f"Commented: {reply_text}")
    else:
        print("No comments found.")
