import requests as rq
import pandas as pd

class VideoFinder():
    def __init__(self, key, path):
        self.key = key
        self.path = path

    def find_videos(self, chan, n):
        '''
        find the n latest videos from a youtube channel using the youtube API
        '''
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key" : self.key,
            "channelId" : chan,
            "part" : "snippet,id",
            "order" : "date",
            "maxResults" : n
            }
        response = rq.get(url, params = params) # ask youtube API
        if response.status_code != 200:
            return pd.DataFrame()
        videos = response.json().get("items", [])
        result = []
        for video in videos:
            if video.get("id", {}).get("kind", "") == "youtube#video":
                video_id = video.get("id", {}).get("videoId", "")
                video_title = video.get("snippet", {}).get("title", "")
                video_date = video.get("snippet", {}).get("publishedAt", "XXXX-XX-XX")[:10]
                channel_title = video.get("snippet", {}).get("channelTitle", "")
                result.append({
                    "date" : video_date,
                    "channel" : chan,
                    "id" : video_id,
                    "channel title" : channel_title,
                    "video title" : video_title})
        return pd.DataFrame(result)

    def find_multichannel_videos(self, channels, n):
        '''
        find the n lastest videos from multiple channels
        '''
        videos_df = pd.DataFrame()
        for channel in channels["channel"]:
            videos_df = pd.concat([videos_df, self.find_videos(channel, n)])
        if videos_df.shape[0] > 0 and "date" in videos_df.columns:
            videos_df.sort_values(by = "date", ascending = False, inplace = True)
        return videos_df.head(n)

    def create_html(self, videos_df):
        '''
        create an html page that embed all youtube videos specified in id_list
        '''
        id_list = videos_df["id"].tolist()
        channel_title_list = videos_df["channel title"].tolist()
        video_title_list = videos_df["video title"].tolist()
        html_code = '<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<meta charset="utf-8">\n\t\t<title>youtube watchlist</title>\n\t</head>\n\t<body>\n\t\t<ul>'
        for video_id, video_title, channel_title in zip(id_list, video_title_list, channel_title_list):
            html_code += f'\n\t\t\t<li>{channel_title} - <a href="https://www.youtube.com/watch?v={video_id}">{video_title}</a></li>'
        html_code += '\n\t\t</ul>\n\t</body>\n</html>'
        return html_code

    def write_to_file(self, text):
        '''
        write text to a file at self.path
        '''
        with open(self.path, 'w') as file:
            file.write(text)

    def make(self, channels):
        '''
        get the latest videos from my favourites youtube channels
        and group them into a single web page
        '''
        latest_videos_df = self.find_multichannel_videos(channels, 40)
        if latest_videos_df.shape[0] > 0 :
            self.write_to_file(self.create_html(latest_videos_df))
            return "Created new HTML file"
        else:
            return "Cannot fetch videos (existing HTML file was preserved)"



# get API key from config file (contains only one key)
key_df = pd.read_csv("./config.csv")
key = key_df.loc[0, "key"]

# define path to same html file
path = "./youtubeWatchlist.html"

# get channels list
channels = pd.read_csv("./channels.csv")

# create and run video finder
video_finder = VideoFinder(key, path)
msg = video_finder.make(channels)
print(msg)
