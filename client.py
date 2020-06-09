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
        r = http.request('POST',f'{self._HOST_NAME}/user/login',fields={'username': username, 'password': password})
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
    @property
    def _header_json(self):
        return {"Authorization": f"Bearer {self._token}", 'Content-Type': 'application/json'}

    def _refresh_token(self):
        http = urllib3.PoolManager()
        r = http.request('POST',f'{self._HOST_NAME}/user/refresh_token',headers=self._header)
        if 'token' in json.loads(r.data):
            self._token = json.loads(r.data)['token']
        else:
            raise ValueError("Unexpected error")
    def register_field(self,field_info):
        """
        Registers a single polygon

        :param field_info: [dict]
        Example: field_info =
        {
        "field_name":"field_56794",
        "label":["ndvi","ndwi","lai","savi","rgb","ndre","chi","smi","Farmer-34"],
        "geojson":{
        "type": "FeatureCollection",
        "features": [
                        {
                          "type": "Feature",
                          "properties": {},
                          "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                              [
                                [
                                  -4.391269683837891,
                                  39.71808094723828
                                ],
                                [
                                  -4.388244152069092,
                                  39.71149505915214
                                ],
                                [
                                  -4.3865275382995605,
                                  39.7120727937937
                                ],
                                [
                                  -4.387707710266113,
                                  39.717800358315465
                                ],
                                [
                                  -4.391269683837891,
                                  39.71808094723828
                                ]
                              ]
                            ]
                          }
                    }
                ]
            }

        }
        """
        http = urllib3.PoolManager()
        json_encoded = json.dumps(field_info)
        r = http.request('POST', f'{self._HOST_NAME}/fields/register', headers=self._header_json, body=json_encoded)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data)
        else:
            return self._handle_error(r)

    def update_field(self,field_info):
        """
        Update services for a field and/or update custom label.

        :param labels: [list] include all services (existing and new) and any other custom label you want for this field.
        Examples: ["ndvi","custom_label"]
        """
        http = urllib3.PoolManager()
        json_encoded = json.dumps(field_info)
        r = http.request('POST', f'{self._HOST_NAME}/fields/update', headers=self._header_json, body=json_encoded)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data)
        else:
            return self._handle_error(r)

    def delete_field(self, field_name):
        """
        Delete a registered field

        :param field_name:[str]
        """
        http = urllib3.PoolManager()
        r = http.request('GET', f'{self._HOST_NAME}/fields/delete/{field_name}', headers=self._header)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data)
        else:
            return self._handle_error(r)

    def get_fields(self, service_name=None, by_label=None):
        """
        View all registered fields

        :param service_name:[str] filter by service. Example: "ndvi"
        :param by_label: [str] filter by custom label (defined at field registration)
        :return: [dict] fieldname,area(ha),[labels/services]
        """
        http = urllib3.PoolManager()
        if by_label is not None:
            body_args={'label':by_label}
            if service_name:
                r = http.request('POST', f'{self._HOST_NAME}/fields/list/{service_name}', headers=self._header,fields=body_args)
            else:
                r = http.request('POST',f'{self._HOST_NAME}/fields/list',headers=self._header,fields=body_args)
        else:
            if service_name:
                r = http.request('POST', f'{self._HOST_NAME}/fields/list/{service_name}', headers=self._header)
            else:
                r = http.request('POST',f'{self._HOST_NAME}/fields/list',headers=self._header)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data["message"])
        else:
            return self._handle_error(r)
    
    def is_field(self, field_name):
        """
        Checks if a field name is available in registred fields

        :param field_name:
        :return:[Boolean]
        """
        http = urllib3.PoolManager()
        r = http.request('GET',f'{self._HOST_NAME}/fields/check/{field_name}',headers=self._header)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data['available'])
        else:
            return self._handle_error(r)
    
    def list_files(self, field_name, service_name, by_ext=None, by_date=None, by_month=None):
        """
        Lists all available files for a field under a service

        :param field_name:[str]
        :param service_name:[str]
        :param by_ext:[str] 'json' or 'png'
        :param by_date:[str] or datetime format
        :param by_month:[str] or datetime format
        :return:
        """

        http = urllib3.PoolManager()
        body_args = {'field_name':field_name}
        service_name= service_name
        if by_ext is not None:
            body_args.update({'ext': by_ext})
        if by_date is not None:
            if isinstance(by_date, datetime.datetime):
                by_date = by_date.strftime('%Y-%m-%d')
            body_args.update({'date': by_date})
        if by_month is not None:
            if isinstance(by_month, datetime.datetime):
                by_month = by_month.strftime('%Y-%m')
            body_args.update({'month': by_month})
        r = http.request('POST',f'{self._HOST_NAME}/files/list/{service_name}',headers=self._header, fields=body_args)
        if r.status == 200:
            self._refresh_token()
            data = json.loads(r.data)
            return self._encapsulate_data(data)
        else:
            return self._handle_error(r)
    
    def download(self, field_name, service_name, by_ext=None, by_date=None, output_folder=None):
        """

        :param field_name:[str]
        :param service_name:[str]
        :param by_ext:[str] 'json' or 'png'
        :param by_date:[str] or datetime format
        :param output_folder:[str] path
        :return: zip file
        """
        http = urllib3.PoolManager()
        body_args = {'field_name':field_name}
        service_name = service_name
        if by_ext is not None:
            body_args.update({'ext': by_ext})
        if by_date is not None:
            if isinstance(by_date, datetime.datetime):
                by_date = by_date.strftime('%Y-%m-%d')
            body_args.update({'date': by_date})
        r = http.request('POST',f'{self._HOST_NAME}/files/get/{service_name}',headers=self._header, fields=body_args)
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
