import base64
import json

import requests


def upload_file_to_github_drawing_bed(file_name, file_address):
    github_token = "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"
    url = "https://api.github.com/repos/Ike-li/Drawing_Bed/contents/pictures/" + file_name  # 用户名、库名、路径
    headers = {"Authorization": "token " + github_token}
    file = open(file_address, 'rb')
    fnb64 = base64.b64encode(file.read()).decode('utf-8')
    content = fnb64
    data = {
        "message": "message",
        "committer": {
            "name": "Ike-li",
            "email": "sinyercy@163.com"
        },
        "content": content
    }
    data = json.dumps(data)
    requests.put(url=url, data=data, headers=headers)
    # req = requests.put(url=url, data=data, headers=headers)
    # req.encoding = "utf-8"
    # re_data = json.loads(req.text)
    # print(re_data)
    print("添加成功")
