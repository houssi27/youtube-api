import requests
import json
from tqdm import tqdm
class youtube_statistics:

    def __init__(self, api_key, channel_id):
        super().__init__()
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None


    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["statistics"]
        except KeyError:
            data = None
        self.channel_statistics = data
        return data

    def get_channel_video_data(self):
        channel_videos = self.get_channel_videos(limit=50)
        print(len(channel_videos))
        parts = ['statistics','contentDetails']
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self.get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
        self.video_data = channel_videos
        return channel_videos

    def get_single_video_data(self,video_id,part):
        url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except KeyError as e:
            print(f'Error! Could not get {part} part of data: \n{data}')
            data = dict()
        return data

    def get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit is not None and isinstance(limit,int):
            url += "&maxResults=" + str(limit)
        video, nextPageToken = self.get_channel_video_per_page(url)
        i = 0
        while(nextPageToken is not None and i < 10):
            next_url = url + "&pageToken=" + nextPageToken
            next_video, nextPageToken = self.get_channel_video_per_page(next_url)
            video.update(next_video)
            i += 1
        return video

    def get_channel_video_per_page(self,url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_video = dict()
        if 'items' not in data:
            return channel_video, None
        item_data = data ['items']
        nextPageToken = data.get('nextPageToken', None)
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == "youtube#video":
                    video_id = item['id']['videoId']
                    channel_video[video_id] =dict()
            except KeyError:
                print('error')
        return channel_video, nextPageToken 

    '''def dump(self):
        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return
        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics,"video_data": self.video_data}}
        channel_title = (self.video_data.popitem()[1].get('channelTitle', self.channel_id))
        channel_title = channel_title.replace(" ", "_").lower()
        filename = channel_title + '.json'
        with open(filename, 'w') as f:
            json.dump(fused_data, f, indent=4)
        
        print('file dumped to', filename)'''
    
    def dump(self):
        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return
        #fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics,"video_data": self.video_data}}
        fused_data = {self.channel_id: {"video_data": self.video_data}}
        channel_title = (self.video_data.popitem()[1].get('channelTitle', self.channel_id))
        channel_title = channel_title.replace(" ", "_").lower()
        filename = channel_title + '.json'
        webhook_url = "https://webhook.site/64b3365f-cd55-4e84-9136-805268c12c4a"
        r = requests.post(webhook_url, data = json.dumps(fused_data), headers={'Content-Type': 'application/json'})
        print('file dumped to', filename)