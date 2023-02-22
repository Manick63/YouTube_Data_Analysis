#!/usr/bin/env python
# coding: utf-8

# In[362]:


from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


# In[363]:


api_key='AIzaSyCQWSiXLMtmBXixsQUNyxUKhcWIZdmjX2s'
#channel_id= 'UCBJycsmduvYEL83R_U4JriQ'

channel_ids = ['UCq-Fj5jknLsUf-MWSy4_brA',#Tseries
              'UCbCmjCuTUZos6Inko4u57UQ',#Cocomelon
              'UCpEhnqL0y41EpW2TvWAHD7Q',#SETIndia
              'UCX6OQ3DkcsbYNE6H8uQQuVA',#MrBeast
              'UC-lHJZR3Gqxm24_Vd_AJ5Yw'#pewdiepie
             ]
youtube = build('youtube','v3',developerKey=api_key)


# In[364]:


def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute()
    for i in range(len(response['items'])):
        data =dict(channel_name = response['items'][i]['snippet']['title'],
              Subscribers = response['items'][i]['statistics']['subscriberCount'],
              Views = response['items'][i]['statistics']['viewCount'],
              Total_videos = response['items'][i]['statistics']['videoCount'],
              playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    return all_data


# In[365]:


channel_statistics = get_channel_stats(youtube, channel_ids)


# In[ ]:


channel_data = pd.DataFrame(channel_statistics)


# In[366]:


channel_data


# In[367]:


channel_data.dtypes


# In[ ]:


channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])
channel_data.dtypes


# In[ ]:


sns.set(rc = {'figure.figsize':(10,8)})
ax = sns.barplot(x='channel_name',y='Subscribers',data = channel_data)


# In[ ]:


ax = sns.barplot(x='channel_name',y='Views',data = channel_data)


# In[ ]:


ax = sns.barplot(x='channel_name',y='Total_videos',data = channel_data)


# In[368]:


channel_data


# In[369]:


playlist_id = channel_data.loc[channel_data['channel_name']=='MrBeast','playlist_id'].iloc[0]


# In[370]:


playlist_id


# In[371]:


def get_video_ids(youtube, playlist_id):
    video_ids = []
    next_page_token = None
    more_pages = True
    
    while more_pages:
        response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        if 'items' in response:
            for item in response['items']:
                video_ids.append(item['contentDetails']['videoId'])
        else:
            print('No items found in playlist')
            break

        next_page_token = response.get('nextPageToken')
        more_pages = next_page_token is not None
    
    return video_ids


# In[372]:


video_ids = get_video_ids(youtube, playlist_id)


# In[373]:


video_ids


# In[374]:


def get_video_details(youtube, video_ids):
    all_video_stats = []
    for i in range(0, len(video_ids),50):
    
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id = ','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response ['items']:
            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = video['statistics'].get('viewCount'),
                               Likes = video['statistics'].get('likeCount'),
                               Dislikes = video['statistics'].get('dislikeCount'),
                               Comments = video['statistics'].get('commentCount')
                              )
            all_video_stats.append(video_stats)
    return all_video_stats


# In[377]:


video_details = get_video_details(youtube, video_ids)


# In[378]:


video_data = pd.DataFrame(video_details)


# In[326]:


video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Dislikes'] = pd.to_numeric(video_data['Dislikes'])
video_data['Comments'] = pd.to_numeric(video_data['Comments'])


# In[327]:


video_data


# In[333]:


top10_videos = video_data.sort_values(by='Views',ascending=False).head(10)


# In[334]:


top10_videos


# In[335]:


ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)


# In[340]:


video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')


# In[341]:


video_data


# In[344]:


videos_per_month = video_data.groupby('Month',as_index = False).size()


# In[345]:


videos_per_month


# In[379]:


sort_order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# In[380]:


videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'],categories=sort_order, ordered=True)


# In[381]:


videos_per_month = videos_per_month.sort_index()


# In[382]:


ax2 = sns.barplot(x='Month', y='size', data = videos_per_month)


# In[360]:


video_data.to_csv('Video_Details(MrBeast).csv')


# In[ ]:




