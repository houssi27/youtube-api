from api import youtube_statistics
import pandas as pd

api_key= 'AIzaSyCdzjdk1OZeX7crANG3hHcYnj8xpIDCKVo'
channel_id = "UC04FyDIvYXNecpbG8gyOw4A"

'''scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("youtube").sheet1
data = sheet.get_all_records()
print(data)'''

youtube = youtube_statistics(api_key,channel_id)
youtube.get_channel_statistics()
youtube.get_channel_video_data()
youtube.dump()