import os
import requests

dump_directory = os.path.join(os.getcwd(), 'mp4')
os.makedirs(dump_directory, exist_ok=True)

video = input("Enter the video URL: ")
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
    video_id = data4.get('vid', {})
    k_value = data4["links"]["mp4"]["137"]["k"]
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
            print(initial_request.status_code)

            if initial_request.status_code == 200:
                filename = os.path.join(dump_directory, 'video.mp4')
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
