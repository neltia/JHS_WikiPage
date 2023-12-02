import datetime
import json


# datetime 객체를 포맷에 맞게 문자열로 변환
def format_datetime(obj):
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    return obj


def conversed_json(data):
    dumped_json = json.dumps(data, default=format_datetime)
    result = json.loads(dumped_json)
    return result
