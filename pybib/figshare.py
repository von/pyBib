"""Interface to figshare

https://docs.figshare.com/

Kudos: https://github.com/makkus/pigshare
"""

import hashlib
import os.path

import requests


FIGSHARE_BASE_URL = 'https://api.figshare.com/v2'


class Figshare:

    def __init__(self, token):
        """Create an interface to Figshare.

        Token is a Figshare Personal Token (not an OAuth token):
        https://help.figshare.com/article/how-to-get-a-personal-token
        """
        self.url = FIGSHARE_BASE_URL
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + token
        }
        self.session.params = {
            'limit': 1000  # Arbitrary default
        }

    def get(self, path, **kwargs):
        """Get from given path"""
        return self.session.get(self.url + path, **kwargs)

    def post(self, path, **kwargs):
        """Post to given path with given data"""
        return self.session.post(self.url + path, **kwargs)

    def put(self, path, **kwargs):
        """Post to given path with given data"""
        return self.session.put(self.url + path, **kwargs)

    def create_article(self, article):
        """Create an article from given dictionary and return it's URI"""
        response = self.post("/account/articles", json=article)
        json = response.json()
        if response.status_code != 201:
            raise Exception(json["message"])
        return json["location"]

    def reserve_doi(self, article_id):
        """Reserve a DOI for the given article id and return the DOI"""
        response = self.post(
            "/account/articles/{}/reserve_doi".format(article_id))
        json = response.json()
        if response.status_code != 200:
            raise Exception(json["message"])
        return json["doi"]

    def upload_new_file(self, article_id, file_path):
        """Upload a new file associated with the given article id"""
        data = {}
        hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        data['md5'] = hash.hexdigest()
        data['name'] = os.path.basename(file_path)
        data['size'] = os.path.getsize(file_path)

        response = self.post('/account/articles/{}/files'.format(article_id),
                             json=data)
        json = response.json()
        if response.status_code != 201:
            raise Exception(json["message"])
        location = json["location"]

        response = self.session.get(location)
        json = response.json()
        upload_url = json["upload_url"]

        response = self.session.get(upload_url)
        json = response.json()
        with open(file_path, 'rb') as file_input:
            for part in json["parts"]:
                size = part['endOffset'] - part['startOffset'] + 1
                response = self.session.put(
                    '{0}/{1}'.format(upload_url, part['partNo']),
                    data=file_input.read(size))
                if response.status_code != 200:
                    raise Exception(
                        "Error uploading file. "
                        "Status = {}".format(response.status_code))

        response = self.session.post(location)
        if response.status_code != 202:
            json = response.json()
            raise Exception(json["message"])
        return location
