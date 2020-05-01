"""
License: MIT
Copyright (c) 2020 - SpaceSense
www.spacesense.ai
"""
import os
import urllib3
import json
import datetime

class NDVIClient:
    _HOST_NAME = "http://api-spacesense.dt.r.appspot.com"

    def __init__(self, username, password):
        self.username = None
        self._token = None
        self._get_token(username, password)


    def _get_token(self, username, password):
        http = urllib3.PoolManager()
        r = http.request('POST',f'{self._HOST_NAME}/user/login',fields={'username': username, 'password':password})
        if 'token' in json.loads(r.data):
            self._token = json.loads(r.data)['token']
            self.username = username
        else:
            raise ValueError("Wrong credentials")
    
    @staticmethod
    def _handle_error(response):
        status = response.status
        data = json.loads(response.data)
        message = data.get('message')
        return {
            "message": message,
            "status": status
        }

    @staticmethod
    def _encapsulate_data(data):
        return {
            "message": data,
            "status": 200
        }


    @property
    def _header(self):
        return {"Authorization": f"Bearer {self._token}"}

    def _refresh_token(self):
        http = urllib3.PoolManager()
        r = http.request('POST',f'{self._HOST_NAME}/user/refresh_token',headers=self._header)
        if 'token' in json.loads(r.data):
            self._token = json.loads(r.data)['token']
        else:
            raise ValueError("Unexpected error")

    def get_fields(self):
        http = urllib3.PoolManager()
        r = http.request('POST',f'{self._HOST_NAME}/fields/list',headers=self._header)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data['fields'])
        else:
            return self._handle_error(r)
    
    def is_field(self, field_name):
        http = urllib3.PoolManager()
        r = http.request('GET',f'{self._HOST_NAME}/fields/check/{field_name}',headers=self._header)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data['available'])
        else:
            return self._handle_error(r)
    
    def list_files(self, field_name, by_ext=None, by_date=None):
        http = urllib3.PoolManager()
        body_args = {'field_name':field_name}
        if by_ext is not None:
            body_args.update({'ext': by_ext})
        if by_date is not None:
            if isinstance(by_date, datetime.datetime):
                by_date = by_date.strftime('%Y-%m-%d')
            body_args.update({'date': by_date})
        r = http.request('POST',f'{self._HOST_NAME}/files/list',headers=self._header, fields=body_args)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data)
        else:
            return self._handle_error(r)
    
    def download(self, field_name, by_ext=None, by_date=None, output_folder=None):
        http = urllib3.PoolManager()
        body_args = {'field_name':field_name}
        if by_ext is not None:
            body_args.update({'ext': by_ext})
        if by_date is not None:
            if isinstance(by_date, datetime.datetime):
                by_date = by_date.strftime('%Y-%m-%d')
            body_args.update({'date': by_date})
        r = http.request('POST',f'{self._HOST_NAME}/files/get',headers=self._header, fields=body_args)
        if r.status == 200:
            self._refresh_token()
            info = r.info()
            filename = info['Content-Disposition'].split('=')[-1]
            data = r.data
            if output_folder is not None:
                path = os.path.join(output_folder, filename)
            else:
                path = filename
            with open(path, 'wb') as f:
                f.write(data)
            return self._encapsulate_data(f"{filename} downloaded")
        else:
            return self._handle_error(r)
