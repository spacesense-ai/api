## Python API support
Python utilities to interact with SpaceSense API

Find out more on how you can integrate Satellite Intelligence in your application at [SpaceSense.ai](https://www.spacesense.ai/)

To get a trial account, contact us at [contact@spacesense.ai](https://www.spacesense.ai/copy-of-solutions)

### Get Started
##### Step 1: Login
```python
from api.client import APIClient

cl = APIClient('username','password')
```
##### Step 2: Register Fields
- You can register a single polygon each time
```python
field_info = {
        "field_name":"field_56794",
        "label":["ndvi","ndwi","lai","savi","rgb","ndre","chi","smi","Farmer-34"],
        "geojson": {
                      "type":"Feature",
                      "properties":{
                
                      },
                      "geometry":{
                         "type":"Polygon",
                         "coordinates":[
                            [
                               [-121.1958,37.6683],
                               [-121.1779,37.6687],
                               [-121.1773,37.6792],
                               [-121.1958,37.6792],
                               [-121.1958,37.6683]
                            ]
                         ]
                      }
                    }

            }


cl.register_field(field_info)
```
output
```python
{   
    "message":"Field field_52494 is created",
    "username": "username",
    "geojson": {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -121.1958,
                        37.6683
                    ],
                    [
                        -121.1779,
                        37.6687
                    ],
                    [
                        -121.1773,
                        37.6792
                    ],
                    [
                        -121.1958,
                        37.6792
                    ],
                    [
                        -121.1958,
                        37.6683
                    ]
                ]
            ]
        }
    },
    "field_name": "field_52494",
    "label":['ndvi', 'ndwi', 'lai', 'savi', 'rgb', 'ndre', 'chi', 'smi', 'Farmer-34','username'],
    "area (ha)": '190.94',
}
```

#### Other Utilities

##### Update Field: update services for a field
- Make sure to include all existing and new services/labels. 'update' function replaces existing services and labels
```python
update = {
            "field_name":"field_52494",
            "label":["NDVI","SAVI","NDRE","Farmer-34"]
            }
cl.update_field(field_info=update)

```

##### Delete fields
- Remove registered fields
```python

cl.delete_field('field_52494')

```

##### Get Fields
- List all available fields. 
- You can check for available fields registered for a specific service or under a common custom label
```python
# to list all registered fields
cl.get_fields()

# to list all fields for a specific service
cl.get_fields(sedrvice_name='savi')

# to list all fields by a custom label
cl.get_fields(by_label='Farmer-34')

# also
cl.get_fields(by_label='Farmer-34',service_name="ndvi")

```

##### List Files
- To view all available files 
- As soon as a new Satellite Imagery is available, SpaceSense will create the insights for you. 
You can anytime view all available insights.
```python

cl.list_files(field_name='field_52494',service_name="smi")

#filter by date: "YYYY-MM-DD" or datetime.datetime(YYYY,MM,DD)
cl.list_files(field_name='field_52494',service_name="chi",by_date='2020-06-06')

#filter by month: "YYYY-MM" or datetime.datetime(YYYY,MM,01)
cl.list_files(field_name='field_52494',service_name="ndvi",by_month='2020-06')

```

##### Get / Download  Files
- Download Insights 
- Returns: Zip file in the format: 'fieldname_servicename_YYYYMMDD.zip'
```python

# get the latest available insight
cl.download(field_name='field_52494',service_name="ndwi")

# get the insight closest to a specific date
#filter by date: "YYYY-MM-DD" or datetime.datetime(YYYY,MM,DD)
cl.download(field_name='field_52494',service_name="ndre",by_date='2020-06-06', output_folder='/home/app/db')

```

