import youtube_dl

def download_video(url):
    
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = url,download=False
    )
    filename = f"{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl': f"Musik/{filename}",
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))
    return filename


if __name__=='__main__':
    url = "x"
    download_video(url)