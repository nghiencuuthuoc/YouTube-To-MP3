import requests
from pytube import YouTube
import os
from pydub import AudioSegment
import re
import urllib.parse
from time import sleep

# Function to remove non-alphabet characters from the title.
def remove_non_alpha(s):
    return re.sub(r"[^a-zA-Z\s]", '', s).replace(' ', '-')


# An input is requested and stored in a variable
url_list_file = input ("Enter a url_list_file url list file: ")

f = open(url_list_file,'r')
urls = f.readlines()
for url in urls:
    print(url)
    
    # Validating input url
    try:
        # url = input("Paste YouTube URL: ")
        result = urllib.parse.urlparse(url)

        # Check if the URL is valid and belongs to YouTube.com
        if result.scheme == "https" and result.netloc == "www.youtube.com" or "youtu.be" in url:
            print("URL check... PASS")
            try:
                yt = YouTube(url)
            except:
                print("Failed to read url. Retrying...")
                sleep(2)
                yt = YouTube(url)
            raw_title = yt.title
            title = remove_non_alpha(raw_title)

            # Send a request to the URL and check if the video is available
            response = requests.get(url)
            if "Video unavailable" in response.text:
                print("Video is not available on YouTube")
                raise ValueError("Video is not available on YouTube")
            else:
                print(f"Title: {title}")
                print("Gathering available streams...")
                sleep(2)

                # Downloading the audio stream
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_file = os.path.join(os.getcwd(), f"{title}.mp4")
                audio_stream.download(output_path=os.getcwd(), filename=f"{title}.mp4")

                # Convert the downloaded audio to MP3
                audio = AudioSegment.from_file(os.path.abspath(audio_file), format='mp4')
                mp3_file = os.path.join(os.getcwd(), f"{raw_title}.mp3")
                audio.export(os.path.abspath(mp3_file), format='mp3', bitrate='320k')

                # Clean up - remove the original MP4 audio file
                os.remove(audio_file)

                print("Audio conversion completed")
                print(f"MP3 file saved: {mp3_file}")

        else:
            print("URL is not valid or does not belong to youtube.com")
            raise ValueError("Invalid URL or URL does not belong to youtube.com")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    with open(url_list_file, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != url:
                f.write(i)
        f.truncate()


