import requests as rq
import pandas as pd

 # get API key from config file (contains only one key)
key_df = pd.read_csv("./config.csv")
key = key_df.loc[0, "key"]

def find_videos(chan, n):
    '''
    find the n latest videos from a youtube channel using the youtube API
    '''
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key" : key,
        "channelId" : chan,
        "part" : "snippet,id",
        "order" : "date",
        "maxResults" : n
        }
    response = rq.get(url, params = params).json() # ask youtube API
    videos = response["items"]
    result = []
    for video in videos:
        if video["id"]["kind"] == "youtube#video":
            video_id = video["id"]["videoId"]
            video_title = video["snippet"]["title"]
            video_date = video["snippet"]["publishedAt"][:10]
            channel_title = video["snippet"]["channelTitle"]
            result.append({
                "date" : video_date,
                "channel" : chan,
                "id" : video_id,
                "channel title" : channel_title,
                "video title" : video_title})
    return pd.DataFrame(result)

def find_multichannel_videos(channels, n):
    '''
    find the n lastest videos from multiple channels
    '''
    videos_df = pd.DataFrame()
    for channel in channels:
        videos_df = pd.concat([videos_df, find_videos(channel, n)])
    videos_df.sort_values(by = "date", ascending = False, inplace = True)
    return videos_df.head(n)

def create_html(id_list):
    '''
    create an html page that embed all youtube videos specified in id_list
    '''
    html_code = '<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<meta charset="utf-8">\n\t\t<title>youtube watchlist</title>\n\t</head>\n\t<body>'
    for video_id in id_list:
        html_code += '\n\t\t<iframe height="200" src="https://www.youtube.com/embed/' + video_id + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media" allowfullscreen></iframe>'
    html_code += '\n\t</body>\n</html>'
    return html_code

def main():
    '''
    get the latest videos from my favourites youtube channels
    and group them into a single web page
    '''
    channels = [
    "UC9hHeywcPBnLglqnQRaNShQ", # le fil d'actu
    "UCVeMw72tepFl1Zt5fvf9QKQ", # osons causer
    "UCyJDHgrsUKuWLe05GvC2lng", # stupid economics
    "UCP46_MXP_WG_auH88FnfS1A", # nota bene
    "UCGeFgMJfWclTWuPw8Ok5FUQ", # hacking social
    "UCtqICqGbPSbTN09K1_7VZ3Q", # dirtybiology
    "UCKjDY4joMPcoRMmd-G1yz1Q", # c'est une autre histoire
    "UCofQxJWd4qkqc7ZgaLkZfcw", # linguisticae
    "UCeR8BYZS7IHYjk_9Mh5JgkA", # scilabus
    "UC7sXGI8p8PvKosLWagkK9wQ", # euh?reka
    "UCS_7tplUgzJG4DhA16re5Yg", # balade mentale
    "UCypzG0nv9B65DwOLJ578rZQ", # le journal de l'espace
    "UCWty1tzwZW_ZNSp5GVGteaA", # la statistique expliquee a mon chat
    "UC2_OG1L8DLTzQ7UrZVOk7OA", # axolot
    "UCLXDNUOO3EQ80VmD9nQBHPg", # fouloscopie
    ] # channel IDs
    latest_videos_df = find_multichannel_videos(channels, 20)
    id_list = latest_videos_df["id"].tolist()
    print(create_html(id_list))

main()
