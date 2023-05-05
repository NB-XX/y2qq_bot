import subprocess
import streamlink


def start_live(url):
    streams = streamlink.streams('https://www.youtube.com/watch?v='+url)
    if 'best' in streams:
        push_m3u8_to_rtmp(streams['best'].url)
    print('获取失败')


def push_m3u8_to_rtmp(m3u8_url):
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', m3u8_url,
        '-c', 'copy',
        '-f', 'flv',
        < rtmp >
    ]

    try:
        subprocess.call(ffmpeg_cmd)
    except KeyboardInterrupt:
        pass
