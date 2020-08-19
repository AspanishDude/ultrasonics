#!/usr/bin/env python3

"""
up_playlist merger
Playlist merger modifier plugin for ultrasonics.

Designed when more than one input plugin is used, and duplicate playlists may be received.
Finds any duplicate playlist names, and then compares each song for duplicate matches.
Uses exact string matching first, for fixed data including ISRC and file path.
Then, uses fuzzy matching for title, artists, album, and date.
The output songs_dict will only contain one version of each playlist, with all unique songs inside.

XDGFX, 2020
"""

import copy

from ultrasonics import logs
from ultrasonics.tools.fuzzymatch import fuzzymatch

log = logs.create_log(__name__)

handshake = {
    "name": "playlist merger",
    "description": "combine input playlists with matching names using highly efficient fuzzy key-value matching.",
    "type": [
        "modifiers"
    ],
    "mode": [
        "playlists"
    ],
    "version": 0.1,
    "settings": [
        {
            "type": "string",
            "value": "This plugin will first attempt to remove all duplicate songs with identical fields - e.g. the same path or ISRC always denotes the same song. Then, it will attempt to match track name, artists, album, and date using fuzzy string matching."
        },
        {
            "type": "string",
            "value": "This means that the titles 'You & Me - Flume Remix', and 'You & Me (Flume Remix)' will likely be flagged ⚠️ as duplicates [with a score of 91]. However, 'You, Me, & the Log Flume Ride' probably won't 🎢 [the score was 67]. The fuzzyness of this matching is determined with the below setting. A value of 100 means the strings must be identical to pass as duplicates. A value of 0 means any string will pass as a duplicate, even if they are completely different. 👽"
        },
        {
            "type": "text",
            "label": "Fuzzy Ratio",
            "name": "fuzzy_ratio",
            "value": "Recommended: 85"
        }
    ]
}


def run(settings_dict, database, songs_dict):
    fuzzy_ratio = (settings_dict["fuzzy_ratio"]
                   or database["fuzzy_ratio"]) / 100

    # Find duplicate playlists.
    # If there are more than two duplicates, the playlist name will show up n-1 times in duplicate_playlists.
    seen = {}
    duplicate_playlists = []

    for item in songs_dict:
        name = item["name"]

        if name not in seen:
            seen[name] == 1
        else:
            if seen[name] > 0:
                duplicate_playlists.append(name)
            seen[name] += 1

    for duplicate in duplicate_playlists:
        playlists = [playlist["songs"]
                     for playlist in songs_dict if playlist["name"] == duplicate]

        playlist_a = playlists[0]
        playlist_b = playlists[1]

        output_playlist = copy.deepcopy(playlist_b)

        for song in playlist_a:
            duplicate = fuzzymatch.match(song, playlist_b, fuzzy_ratio)

            if not duplicate:
                output_playlist.append[song]

        # Replace two previous playlists with one new playlist

    return songs_dict


def builder(database):
    settings_dict = [
        {
            "type": "string",
            "value": "This plugin is required when there is one or more input plugin - otherwise the songs from the second input plugin will simply overwrite the first at the output stage."
        },
        {
            "type": "string",
            "value": "Here, 'Fuzzy Ratio' can be set to manually override the global setting for this specific applet. Otherwise, leave it blank to use the global setting."
        },
        {
            "type": "text",
            "label": "Fuzzy Ratio",
            "name": "fuzzy_ratio",
            "value": f"Currently: {database['fuzzy_ratio']} 👾"
        }
    ]

    return settings_dict
