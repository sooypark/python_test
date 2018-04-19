# -*- coding:utf-8 -*-
import urllib3
import json
import pprint
import pandas as df
import pickle

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "0c60dd4a-3135-40ee-b8a2-a62d1cb097bb"
analysisCode = "dparse"
text = "Wis은 자체 Qualification Data요청하지만자체 평가 여부는 확인되지 않았으며 Pack 평가 시 Issue "

requestJson = {
    "access_key": accessKey,
    "argument": {
        "text": text,
        "analysis_code": analysisCode
    }
}

http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)

print("[responseCode] " + str(response.status))
print("[responBody]")
data_file =(str(response.data, "utf-8"))
total_list = []
total_list.append(data_file)


# f = open('data.json', 'w', encoding='utf-8')
# f.write(data_file)



with open('data.json',encoding='utf-8') as data_file:
    data = json.load(data_file)

# pprint.pprint(data)
# pprint.pprint(data['return_object']['sentence'][0]['dependency'])

head = []
id = []
label = []
mod = []
text = []
weight = []

# print(type(data['return_object']['sentence'][0]['dependency']))

for data_dict in data['return_object']['sentence'][0]['dependency']:
    # print(type(data_dict))
    head.append(data_dict['head'])
    id.append(data_dict['id'])
    label.append(data_dict['label'])
    mod.append(data_dict['mod'])
    text.append(data_dict['text'])
    weight.append(data_dict['weight'])

# print(text)
frame  = df.DataFrame({'id' :id, 'head':head, 'label':label, 'mod' : mod, 'text':text, 'weight' : weight})

print(frame[frame['text'].str.contains("발생")==True])
# print(frame)
