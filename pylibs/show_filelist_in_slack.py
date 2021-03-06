# -*- coding: utf-8 -*-
import yaml
import requests
import json
from datetime import datetime

yaml_dict = yaml.load(open('/root/scripts/slack.yaml'), Loader=yaml.SafeLoader)
token = yaml_dict['slack_selftoken']
c_name = yaml_dict['slack_channel']
url = "https://slack.com/api/channels.list?token=" + token
headers = {"content-type": "application/json"}
extract_channel = (c_name)

r = requests.get(url,headers=headers)
data = r.json()
entries = [attr for attr in data['channels'] if attr['name'] in extract_channel]
entries = sorted( entries , key=lambda x:x['created'] )
print("  DATE of CREATED   CHANNELID NAME")
print("---------------------------------------------------")
for attr in entries:
    print(str(datetime.fromtimestamp(attr['created'])) + " " + attr['id'] + " " + attr['name'])
    url2 = "https://slack.com/api/files.list?token=" + token + "&channel=" + attr['id']
    headers2 = {"content-type": "application/json"}
    r2 = requests.get(url2 ,headers=headers2)
    json_data2 = r2.json()
    try:
        entries2 = json_data2['files']
        entries2 = sorted( entries2 , key=lambda x:x['created'] )
        for attr2 in entries2:
            print( "    " + str(datetime.fromtimestamp(attr2['created'])) + " " + attr2['id'] + " " + attr2['title'])
    except KeyError:
        print("No files.")
