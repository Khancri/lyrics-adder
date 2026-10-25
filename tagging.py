from mutagen.id3 import ID3, USLT, Encoding, ID3NoHeaderError
import re

def parse_lrc(lrc):
    out = []
    for line in lrc.splitlines():
        m = re.match(r'\[(\d+):(\d+(?:\.\d+)?)\](.*)', line)
        if m:
            ms = int((int(m[1]) * 60 + float(m[2])) * 1000)
            out.append((m[3].strip(), ms))
    return out


def patch_lyrics_mp3(file_path: str, synced_lyrics: str | None = None, plain_lyrics: str | None = None):
    if synced_lyrics == None and plain_lyrics == None:
        return
    track = ID3(file_path)
    try:
        track.delall('USLT')
    except ID3NoHeaderError:
        track = ID3()
    track.add(USLT(encoding=Encoding.UTF8, lang='eng', desc='', text=parse_lrc(synced_lyrics)))
    track.save
