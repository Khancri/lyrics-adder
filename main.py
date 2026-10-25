from typing import TypeAliasType

import tagging
from os import path
import json
import urllib.request
import urllib.parse
import urllib.error
import argparse
import time

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument('filename')
parser.add_argument('-a', '--artist')
parser.add_argument('-t', '--title')
# parser.add_argument('-al', '--album')

def urlopen_retry(req, tries=4, delay=2):
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == tries - 1:
                raise
        except urllib.error.URLError:
            if i == tries - 1:
                raise
        time.sleep(delay * 2 ** i)

def fetch_lrclib(track_name, track_artist, track_duration: None | int = None):
    url = f'https://lrclib.net/api/get?track_name={urllib.parse.quote_plus(track_name)}&artist_name={urllib.parse.quote_plus(track_artist)}{f"&duration={track_duration}" if track_duration != None else ''}'
    print(url)
    req = urllib.request.Request(url, headers={"User-Agent": "lyrics-add v0.1 (https://github.com/khancri)"})
    return urlopen_retry(req, 3, 2)

def main(track_name, track_artist, file_path):
    req = fetch_lrclib(track_name, track_artist)
    print(type(req))
    print(req.decode())
    obj = json.loads(req.decode())
    print(obj)
    print(obj['plainLyrics'])
    tagging.patch_lyrics_mp3(file_path, obj['syncedLyrics'], obj['plainLyrics'])

if __name__ == '__main__':
    args = parser.parse_args()
    title = args.title or input('title: ')
    artist = args.artist or input('artist: ')
    path = path.expanduser(args.filename)
    print(title, artist)
    main(title, artist, path)

