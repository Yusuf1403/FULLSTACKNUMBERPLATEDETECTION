import requests, os, sys
import os
model_id = "76d3f43f-2f79-4a06-8e8b-8b69f6f362a9"
api_key = "94c1a798-c97f-11ed-8134-82d459a7ac52"

image_path = sys.argv[1]
def license_plate_text_detection(image_path):
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id + '/LabelFile/'

    data = {'file': open(image_path, 'rb'),    'modelId': ('', model_id)}

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)

    js=response.json()
    templates=js['result']
    return templates