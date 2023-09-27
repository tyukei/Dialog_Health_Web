import requests
import json


def send_request(data):
    url = 'https://us-central1-sic-poc1-verify.cloudfunctions.net/registAction'

    headers = {
        'Accept': 'application/json',
    }
    response = requests.post(url, headers=headers, json=data)
    
    try:
        return response.json(), None  # 成功した場合はJSONデータとエラーなし(None)を返す
    except json.JSONDecodeError:
        return None, response.text  # 失敗した場合はNoneとレスポンスのテキストを返す