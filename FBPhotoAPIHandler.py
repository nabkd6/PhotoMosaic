import requests
from FBJSONparse import *
import urllib.request
from key import APIKEY
import json

class FBPhotoAPIHandler():
    """Handles FB API requests to get individual photos."""
    #At time of creation, FB API did not allow to query photos directly.
    #Need to query user ALBUMS, and then query each album to get the photos.
    def __init__(self,
    access_token_name = 'access_token',
    access_token = APIKEY,
    initial_url = 'https://graph.facebook.com/v3.3/me/albums',
    base_url = 'https://graph.facebook.com/v3.3/',
    field_param = '/photos?fields=images',
    to_visit = [],
    album_data_list = [],
    all_image_sources = [],
    ):
        self.__access_token_name = 'access_token'
        self.__access_token = APIKEY
        self.__params = ((self.__access_token_name, self.__access_token),)
        self.__initial_url = initial_url
        self.__base_url = base_url
        self.__field_param = field_param
        self.__to_visit = to_visit
        self.__album_data_list = album_data_list
        self.__all_image_sources = []

    #Setters
    def set_access_token_name(self, token_name):
        self.__access_token_name = name
    def set_access_token(self, key):
        self.__access_token = key
    def set_initial_url(self,url):
        self.__initial_url = url
    def set_base_url(self,url):
        self.__base_url = url
    def set_field_param(self,param):
        self.__field_param = param
    def set_to_visit(self,visit_list):
        self.__to_visit = visit_list
    def set_album_data_list(self,album_item):
        self.__album_data_list.append(album_item)
    def set_all_image_sources(self,image_sources):
        self.__all_image_sources = image_sources

    #Getters
    def get_access_token_name(self):
        return self.__access_token_name
    def get_access_token(self):
        return self.__access_token
    def get_params(self):
        return self.__params
    def get_initial_url(self):
        return self.__initial_url
    def get_base_url(self):
        return self.__base_url
    def get_field_param(self):
        return self.__field_param
    def get_to_visit(self):
        return self.__to_visit
    def get_album_data_list(self):
        return self.__album_data_list
    def get_all_image_sources(self):
        return self.__all_image_sources


    def populate_to_visit(self):
        """Populates a list of requests 'to visit' from initial request
        to get the albums for a facebook user"""
        response = requests.get(self.__initial_url, params=self.__params)
        album_ids = album_parser(response.json())
        for item in album_ids:
            new_url = self.__base_url + item + self.__field_param
            self.__to_visit.append(new_url)

    def populate_album_data(self):
        """Visits albums to get individual photo information, and handles
        paging"""
        while self.__to_visit:
            url = self.__to_visit.pop()
            response = requests.get(url, params=self.__params)
            album_data = response.json()
            self.__album_data_list.append(album_data)
            if "next" in album_data['paging']:
                self.__to_visit.append(album_data['paging']['next'])

    def populate_all_image_sources(self):
        """Uses image_parser helper function to populate list of all image
        sources with "max" quality"""
        for item in self.__album_data_list:
            self.__all_image_sources +=(image_parser(item))

    def createimagedict(self):
        """Creates a dictionary: key = file count, val = image source
        Saves dictionary as JSON to avoid remaking API calls"""
        file_dict = {}
        file_counter = 0
        for image_source in self.__all_image_sources:
            key = str(file_counter)
            file_dict.update({key:image_source})
            file_counter+=1
        with open('all_image_sources.txt', 'w') as outfile:
            json.dump(file_dict, outfile)
