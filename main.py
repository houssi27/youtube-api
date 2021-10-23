from api import youtube_statistics

api_key= 'AIzaSyCdzjdk1OZeX7crANG3hHcYnj8xpIDCKVo'
channel_id = 'UCZ3wH-v5zOcq4ZZWI58TGKA'

youtube = youtube_statistics(api_key,channel_id)
youtube.get_channel_statistics()
youtube.get_channel_video_data()
youtube.dump()