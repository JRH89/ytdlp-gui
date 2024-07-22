from pytube import YouTube

def download_youtube_video(url):
    try:
        # Create a YouTube object with the URL
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()
        
        # Print the title of the video
        print(f"Title: {yt.title}")
        
        # Download the video
        print("Downloading...")
        stream.download()
        print("Download completed!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Prompt the user to enter a YouTube URL
    url = input("Enter the YouTube URL: ")
    download_youtube_video(url)
