import requests
from datetime import datetime, timezone, timedelta


headers = {
    "Accept": "application/json",
    "X-APIKEY": < api_key >
}


def live(type, org):
    querystring = {"status": "live", "type": type, "org": org}
    url = "https://holodex.net/api/v2/live"
    response = requests.get(url, headers=headers, params=querystring).json()
    return response


def get_live(response):
    result_str = ''
    count = 1
    for json_data in response:
        title = json_data["title"]
        try:
            start_actual = datetime.fromisoformat(json_data["start_actual"].replace(
                "Z", "+00:00")).astimezone(timezone(timedelta(hours=8)))
        except KeyError:
            # holodex在新直播刚开的时候可能不包含start_actual字段
            start_actual = datetime.fromisoformat(json_data["start_scheduled"].replace(
                "Z", "+00:00")).astimezone(timezone(timedelta(hours=8)))
        # 计算直播时长
        current_time = datetime.now(timezone(timedelta(hours=8)))
        live_duration = current_time - start_actual
        hours = live_duration.seconds // 3600
        minutes = (live_duration.seconds % 3600) // 60
        seconds = live_duration.seconds % 60
        result = "{}: {} 已经直播的时间: {}:{}:{}\n".format(count,
                                                     title, hours, minutes, seconds)
        count = count + 1
        result_str += result
    return result_str


def get_live_info(count, response):
    video_id = response[count]['id']
    return video_id
