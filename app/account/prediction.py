import requests, os, sys
import os
from decouple import config

model_id = config('model_id')
api_key = config('api_key')

image_path = sys.argv[1]
def license_plate_text_detection(image_path):
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id + '/LabelFile/'

    data = {'file': open(image_path, 'rb'),    'modelId': ('', model_id)}

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)

    js=response.json()
    templates=js['result']
    texts=list()
    try : 
        for template in templates:
            texts.append(template['prediction'][0]['ocr_text'])
    except Exception as e:
        texts=None
        print(e,"\n",template)

    return texts