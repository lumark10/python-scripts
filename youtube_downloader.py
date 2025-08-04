import yt_dlp
import os

#---- Configs
DOWNLOAD_DIR = r'C:\Path\To\Your\Downloads'  # Change this to download dir

# YouTube URLs to download 
URLS = [
    'https://www.youtube.com/watch?v=EXAMPLE_VIDEO_ID',  # Replace with actual URLs and add more if wanted
   
]

# Download options configuration
DOWNLOAD_OPTIONS = {
    'format': 'bestaudio/best',                           
    'outtmpl': DOWNLOAD_DIR + '/%(title)s.%(ext)s',      
    'noplaylist': True,                                  
    'extractaudio': True,                                 
    'audioformat': 'mp3',                                
    'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '192',                       
    }],

    'quiet': False,                                       
    'no_warnings': False,                                 
}

def main():
    """
    Downloads YouTube videos/audio using yt-dlp.
    Supports various formats and quality options.
    """
    
    if not validate_config():
        return
    
    # Create download dir
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"Download directory: {DOWNLOAD_DIR}")
    
    valid_urls = [url for url in URLS if 'EXAMPLE_VIDEO_ID' not in url and url.strip()]
    
    if not valid_urls:
        print("No valid URLs found. Please add YouTube URLs to the URLS list.")
        return
    
    print(f"Preparing to download {len(valid_urls)} video(s)...")
    print("-" * 50)
    
    success_count = 0
    error_count = 0
    
    with yt_dlp.YoutubeDL(DOWNLOAD_OPTIONS) as ydl:
        for i, url in enumerate(valid_urls, 1):
            print(f"\\nDownloading {i}/{len(valid_urls)}: {url}")
            try:
                ydl.download([url])
                print(f"✓ Successfully downloaded: {url}")
                success_count += 1
            except Exception as e:
                print(f"✗ Error downloading {url}: {e}")
                error_count += 1
    
    print("\\n" + "="*50)
    print("DOWNLOAD SUMMARY")
    print(f"Successful downloads: {success_count}")
    print(f"Failed downloads: {error_count}")
    print(f"Files saved to: {DOWNLOAD_DIR}")
    print("="*50)


def validate_config():

    if 'Path\\To\\Your' in DOWNLOAD_DIR:
        print("Error: Please update DOWNLOAD_DIR with your actual download path.")
        print(f"Current path: {DOWNLOAD_DIR}")
        return False
    
    if not URLS or all('EXAMPLE_VIDEO_ID' in url for url in URLS):
        print("Error: Please add actual YouTube URLs to the URLS list.")
        print("Example: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        return False
    
    return True


def get_video_info(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'view_count': info.get('view_count'),
                'upload_date': info.get('upload_date')
            }
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None


def download_playlist(playlist_url, max_downloads=None):
 
    playlist_options = DOWNLOAD_OPTIONS.copy()
    playlist_options['noplaylist'] = False  
    
    if max_downloads:
        playlist_options['playlistend'] = max_downloads
    
    with yt_dlp.YoutubeDL(playlist_options) as ydl:
        try:
            ydl.download([playlist_url])
            print(f"✓ Successfully downloaded playlist: {playlist_url}")
        except Exception as e:
            print(f"✗ Error downloading playlist: {e}")


if __name__ == "__main__":
    main()
