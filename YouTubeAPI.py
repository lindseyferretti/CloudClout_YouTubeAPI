# -*- coding: utf-8 -*-

# Sample Python code for youtube.guideCategories.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
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

    request = youtube.guideCategories().list(
        part="snippet",
        regionCode="US"
    )
    response = request.execute()
    print(json.dumps(response, indent=4))

    guide_categories = {} # maps guide category IDs to names
    channels = {} # maps guide category IDs to a list of channel IDs
    playlists = {} # maps channel IDs to uploaded playlist IDs
    videos = {} # maps playlist IDs to a list of uploaded videos
    tags = {} # maps video ID to a list of tags

    # Iterate through result, pulling out guideCategories (high-level channel
    # classifications)
    results = response["items"]
    for result in results:
        category_id = result["snippet"]["channelId"]
        category_name = result["snippet"]["title"]
        guide_categories[category_id] = category_name

    # For each guide category, pull a list of channels associated with that
    # guide category
    categories = guide_categories.keys()
    for category in categories:
        # Request channels with categoryId = category
        response = run_channel_request(youtube, None, category)
        next_page_token = "" # Just make something non-None so loops runs once

        # Create list of channel IDs from response
        channel_list = []
        while next_page_token is not None:
            results = response["items"]
            for result in results:
                channel_id = result["id"]
                channel_list.append(channel_id)

                # While we're on a channel ID, we'll pull its uploaded
                # videos playlist ID from the contentDetails
                playlist_id = result["contentDetails"]["relatedPlaylists"]["uploads"]
                playlists[channel_id] = playlist_id

                # Next, we'll request all the videos in the playlist
                uploads_response = run_playlist_items_request(youtube,
                                                              None,
                                                              playlist_id)
                uploads_next_page_token = ""

                # Create list of videos from response
                videos_list = []
                while uploads_next_page_token is not None:
                    video_results = uploads_response["items"]
                    for video_result in video_results:
                        video_id = video_result["contentDetails"]["videoId"]
                        videos_list.append(video_id)

                        # Last step: pull all the tags for each video
                        tags_response = run_tags_request(youtube, None,
                                                         video_id)

                        # Create list of tags from response (top 50 tags)
                        tags_list = tags_response["items"]["snippet"]["tags"]
                        tags[video_id] = tags_list

                    uploads_next_page_token = get_next_page_token(uploads_response)
                    uploads_response = run_playlist_items_request(youtube,
                                                                  uploads_next_page_token,
                                                                  playlist_id)
                videos[playlist_id] = videos_list
            next_page_token = get_next_page_token(response)
            response = run_channel_request(youtube, next_page_token, category)
        # Add list of channels for category to channels map
        channels[category] = channel_list


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
            maxResults=50
        )
    else:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
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


if __name__ == "__main__":
    main()
