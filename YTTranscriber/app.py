import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the environment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a youtube video summerizer. You will be taking the transcrit text ans summerizing the entire video and providing the important summary in points within 250 words. Please provide the summary of text given here : """



## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript =""
        for i in transcript_text:
            transcript +=" " + i["text"]

        return transcript


    except Exception as e:
        raise e

## Getting the summary based on Prompt from Googlr Gemini Pro
def generate_gemini_content(transcipt_text,prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcipt_text)
    return response.text

st.title("Youtube Trannscript to Detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width = True)

if st.button("Get Detailed Note"):
    transcipt_text = extract_transcript_details(youtube_link)

    if(transcipt_text):
        summary = generate_gemini_content(transcipt_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
