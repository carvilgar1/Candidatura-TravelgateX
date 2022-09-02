import json
from urllib.request import urlopen

#API endpoints
url_api_hoteles_atalaya = 'http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253'
url_api_resort_hoteles = 'http://www.mocky.io/v2/5e4e43272f00006c0016a52b'
url_rooms_information = 'https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036'
url_meal_plans_information = 'http://www.mocky.io/v2/5e4a7e282f0000490097d252'
url_available_regimens = 'http://www.mocky.io/v2/5e4a7dd02f0000290097d24b'

json_api_hoteles_atalaya = json.loads(urlopen(url_api_hoteles_atalaya).read())
json_api_resort_hoteles = json.loads(urlopen(url_api_resort_hoteles).read())
json_rooms_information = json.loads(urlopen(url_rooms_information).read())
json_meal_plans_information = json.loads(urlopen(url_meal_plans_information).read())
json_available_regimens = json.loads(urlopen(url_available_regimens).read())



