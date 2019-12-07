import os.path
import urllib.request
import json

file_path = "./Photos/"

def downloadfiles():
    with open("all_image_sources.txt") as json_file:
        data = json.load(json_file)
        for key in data:
            file_name = file_path + key + ".jpg"
            download = urllib.request.urlretrieve(data[key], file_name)
