import base64
import hashlib
import hmac
import os
import time

import requests

def execute():
    audio_absolute_path = './video000.wav'

    access_key = '51c1b46567d00a81aa1bc5fe9298c55e'
    access_secret = 'wnZxwgZ9ASgy6nAJE0MBf0lelv5a624mvhq4aWxe'
    requrl = "http://identify-eu-west-1.acrcloud.com/v1/identify"

    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    string_to_sign = http_method + "\n" + http_uri + "\n" + access_key + "\n" + data_type + "\n" + signature_version + "\n" + str(
        timestamp)

    sign = base64.b64encode(hmac.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'),
                                        digestmod=hashlib.sha1).digest()).decode('ascii')

    files = [
        ('sample', ('test.mp3', open(audio_absolute_path, 'rb'), 'audio/mpeg'))
    ]
    data = {'access_key': access_key,
            'sample_bytes': os.path.getsize(audio_absolute_path),
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': data_type,
            "signature_version": signature_version}

    response = requests.post(requrl, files=files, data=data)
    print(response.json())
    return response.json()

execute()