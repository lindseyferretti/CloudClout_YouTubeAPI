# -*- coding: utf-8 -*-

# Sample Python code for youtube.guideCategories.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import sys
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    category_id = sys.argv[1]
    print(category_id)
    channels_to_tags = get_data(category_id)
    dump_to_json(channels_to_tags, category_id)


def channelID_to_name(youtube, channelID):
    request = youtube.channels().list(
        part="snippet",
        id=channelID
    )
    response = request.execute()
    return response["items"][0]["snippet"]["title"] 


def run_channel_request(youtube, next_page_token, category):
    if next_page_token is None:
        request = youtube.channels().list(
            part="contentDetails",
            categoryId=category,
            maxResults=50
        )
    else:
        request = youtube.channels().list(
            part="contentDetails",
            categoryId=category,
            maxResults=50,
            pageToken=next_page_token
        )
    response = request.execute()
    return response


def run_playlist_items_request(youtube, next_page_token, playlist_id):
    if next_page_token is None:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=25
        )
    else:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=25,
            pageToken=next_page_token
        )
    response = request.execute()
    return response


def run_tags_request(youtube, next_page_token, video_id):
    if next_page_token is None:
        request = youtube.videos().list(
            part="snippet",
            id=video_id,
            maxResults=50
        )
    else:
        request = youtube.videos().list(
            part="snippet",
            id=video_id,
            maxResults=50,
            pageToken=next_page_token
        )
    response = request.execute()
    return response


def get_next_page_token(response):
    try:
        next_page_token = response["nextPageToken"]
    except:
        next_page_token = None
    return next_page_token


def aggregate_tags(tags, channel_names):
    aggregate_tags = {}
    for channel in tags:
        tag_dict = tags[channel]
        middle_man_dict = {}
        max_tags = {}
        index = 0
        middle_man_dict["title"] = channel_names[channel]
        while index < 10 and len(tag_dict) > 0:
            max_tag = max(tag_dict, key=lambda k: tag_dict[k])
            max_tags[max_tag] = tag_dict[max_tag]
            tag_dict.pop(max_tag)
            index += 1
        middle_man_dict["tags"] = max_tags
        aggregate_tags[channel] = middle_man_dict
    return aggregate_tags


def get_data(category):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secrets.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    channels = {}  # maps guide category IDs to a list of channel IDs
    playlists = {}  # maps channel IDs to uploaded playlist IDs
    videos = {}  # maps playlist IDs to a list of uploaded videos
    tags = {}  # maps channel ID to dict of tags => num of occurrences
    channel_names = {} # maps channel IDs to their readable names
    
    # For guide category, pull a list of channels associated with that
    # guide category
    # Request channels with categoryId = category
    response = run_channel_request(youtube, None, category)

    # Create list of channel IDs from response
    # Only taking top 50 channels returned
    channel_list = []
    results = response["items"]
    for result in results:
        channel_id = result["id"]
        channel_names[channel_id] = channelID_to_name(youtube, channel_id)
        channel_list.append(channel_id)

        # While we're on a channel ID, we'll pull its uploaded
        # videos playlist ID from the contentDetails
        playlist_id = result["contentDetails"]["relatedPlaylists"][
            "uploads"]
        playlists[channel_id] = playlist_id

        # Next, we'll request all the videos in the playlist
        uploads_response = run_playlist_items_request(youtube, None,
                                                      playlist_id)

        # Create list of videos from response
        # Only going to use the 25 most recent uploads (no pagination)
        videos_list = []
        video_results = uploads_response["items"]
        for video_result in video_results:
            video_id = video_result["contentDetails"]["videoId"]
            videos_list.append(video_id)

            # Last step: pull all the tags for each video
            tags_response = run_tags_request(youtube, None, video_id)
            snippet = tags_response["items"][0]["snippet"]

            # Create list of tags from response (top 50 tags)
            # Note that every now and then a video has no tags
            if channel_id in tags:
                tag_dict = tags[channel_id]
            else:
                tag_dict = {}
                tags[channel_id] = tag_dict
            try:
                tags_list = snippet["tags"]
                for tag in tags_list:
                    if tag in tag_dict:
                        tag_dict[tag] += 1
                    else:
                        tag_dict[tag] = 1

            except KeyError:
                print("No tags for this video")
        videos[playlist_id] = videos_list
    # Add list of channels for category to channels map
    channels[category] = channel_list
   
    # Aggregate tags per channel ID into lists of top 10 tags
    aggregated_tags = aggregate_tags(tags, channel_names)
    return aggregated_tags


def dump_to_json(channels_to_tags, category_id):
    json_text = json.dumps(channels_to_tags, indent=4)
    print(json_text)

    json_file = open(category_id + ".txt", "w")
    json_file.write(json_text)
    json_file.close()


if __name__ == "__main__":
    main()
    
