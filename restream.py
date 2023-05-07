import subprocess
import yt_dlp


def start_live(video_id, user_key):
    try:
        ydl = yt_dlp.YoutubeDL()
        info_dict = ydl.extract_info(
            'https://www.youtube.com/watch?v='+video_id, download=False)
        m3u8 = info_dict['formats'][0]['url']
        push_m3u8_to_rtmp(m3u8, user_key)
    except Exception as e:
        print(e)


def push_m3u8_to_rtmp(m3u8_url, user_key):
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', m3u8_url,
        '-c', 'copy',
        '-f', 'flv',
        f'rtmp://qqgroup.6721.livepush.ilive.qq.com/trtc_1400526639/{user_key}'
    ]

    try:
        subprocess.call(ffmpeg_cmd)
    except Exception as e:
        return e
