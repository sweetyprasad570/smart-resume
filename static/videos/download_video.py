#!/usr/bin/env python3
"""
Script to download video from Pinterest link and save as background.mp4
"""

import requests
import re
import os
from urllib.parse import urlparse

def download_pinterest_video(pinterest_url):
    """
    Download video from Pinterest URL
    Note: This is a basic implementation. Pinterest may require authentication
    or have anti-bot measures that prevent direct downloading.
    """
    try:
        # Follow redirects to get the actual URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Attempting to access: {pinterest_url}")
        response = requests.get(pinterest_url, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            # Look for video URLs in the response
            video_urls = re.findall(r'https?://[^"\s]+\.mp4[^"\s]*', response.text)
            
            if video_urls:
                video_url = video_urls[0]
                print(f"Found video URL: {video_url}")
                
                # Download the video
                video_response = requests.get(video_url, headers=headers, stream=True)
                
                if video_response.status_code == 200:
                    # Save the video
                    output_path = os.path.join(os.path.dirname(__file__), 'background.mp4')
                    
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"Video saved to: {output_path}")
                    return True
                else:
                    print(f"Failed to download video. Status code: {video_response.status_code}")
            else:
                print("No video URL found in the page response.")
        else:
            print(f"Failed to access Pinterest URL. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error downloading video: {e}")
    
    return False

def main():
    pinterest_url = "https://pin.it/YO3vyWbCw"
    
    print("Pinterest Video Downloader")
    print("=" * 30)
    print(f"URL: {pinterest_url}")
    print()
    
    if download_pinterest_video(pinterest_url):
        print("\n✅ Video downloaded successfully!")
        print("The video background should now work on your homepage.")
    else:
        print("\n❌ Failed to download video automatically.")
        print("\nAlternative methods:")
        print("1. Use a Pinterest video downloader website")
        print("2. Use browser extensions to download the video")
        print("3. Manually save the video and place it in this directory")
        print("\nOnce you have the video file, save it as 'background.mp4' in this directory.")

if __name__ == "__main__":
    main()
