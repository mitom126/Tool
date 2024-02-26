import requests
import json
import os

class YouTubeApi:
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    session = None

    def __init__(self, playlist_url: str, api_key: str):
        self.playlist_id = playlist_url.split('=')[-1]
        self.api_key = api_key
        self.session = requests.Session()

    def get_data_for_playlist(self) -> list:
        params = {
            "part": "snippet",
            "maxResults": 1000,
            "playlistId": self.playlist_id,
            "key": self.api_key
        }
        videos_data = []
        while True:
            res = self.session.get(self.base_url, params=params)
            data = json.loads(res.text)
            if 'items' in data:
                videos_data += [item['snippet']['resourceId']['videoId'] for item in data['items']]
            if 'nextPageToken' in data:
                params['pageToken'] = data['nextPageToken']
            else:
                break
        return videos_data

print("Playlist:")
playlist = input()
api = YouTubeApi(playlist, 'AIzaSyA5VrlQ2LSvU92-gh1Wyt-EkAZd_I4b82k')
videos_data = api.get_data_for_playlist()

index = 1  

for video_id in videos_data:

    video = f"https://www.youtube.com/watch?v={video_id}"
    dump_directory = os.path.join(os.getcwd(), 'mp4')
    os.makedirs(dump_directory, exist_ok=True)

    url1 = 'https://www.y2mate.com/mates/en891/analyzeV2/ajax'

    headers = {
        'Host': 'www.y2mate.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    data1 = {
        'k_query': video,
        'k_page': 'home',
        'hl': 'en',
        'q_auto': 0,
    }

    res1 = requests.post(url1, headers=headers, data=data1)

    if res1.status_code == 200:
        data4 = res1.json()
        idname = data4["title"]
        print(idname)
        video_id = data4.get('vid', {})
        video_data = data4["links"]["mp4"]
        k_value = None
        if '137' in video_data:
            k_value = video_data["137"]["k"]
        elif 'auto' in video_data:
            k_value = video_data["auto"]["k"]
        url2 = 'https://www.y2mate.com/mates/convertV2/index'
        data2 = {
            'vid': video_id,
            'k': k_value,
        }   
        res2 = requests.post(url2, headers=headers, data=data2)
        if res2.status_code == 200:
            payload = {
                'api': 'advanced',
                'format': 'JSON',
                'video': video,
            }
            datafinal = res2.json().get('dlink')

            if datafinal:
                datafinal = datafinal.replace('\/', '/')
                initial_request = requests.get(datafinal)
                if initial_request.status_code == 200:
                    filename = os.path.join(dump_directory, f'{idname}.mp4')
                    open(filename, 'wb').write(initial_request.content)
                    print(f"Video saved to {filename}")
                else:
                    print("Failed to download the converted video.")
            else:
                print("Failed to get the download link.")
        else:
            print("Failed to convert the video.")
    else:
        print("Failed to analyze the video URL.")
