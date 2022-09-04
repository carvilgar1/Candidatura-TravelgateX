import json

from enum import Enum

from urllib.request import urlopen

class RoomType(Enum):
    STANDARD = 'STANDARD'
    SUITE = 'SUITE'

#API endpoints
url_api_hoteles_atalaya = 'http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253'
url_api_resort_hoteles = 'http://www.mocky.io/v2/5e4e43272f00006c0016a52b'
url_rooms_information = 'https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036'
url_meal_plans_information = 'http://www.mocky.io/v2/5e4a7e282f0000490097d252'
url_available_regimens = 'http://www.mocky.io/v2/5e4a7dd02f0000290097d24b'

json_api_hoteles_atalaya = json.loads(urlopen(url_api_hoteles_atalaya).read()) #JSON formatted gotten from the previous urls are converted to Python object
json_api_resort_hoteles = json.loads(urlopen(url_api_resort_hoteles).read())
json_rooms_information = json.loads(urlopen(url_rooms_information).read())
json_meal_plans_information = json.loads(urlopen(url_meal_plans_information).read())
json_available_regimens = json.loads(urlopen(url_available_regimens).read())

def room_type_normalization(room_str) -> str:
    '''
    This function converts the string that contains room's information 
    into standardized Enum type of the company and returns a serialized value.
    '''
    if room_str in {'st', 'standard'}:
        return RoomType.STANDARD.value
    else:
        return RoomType.SUITE.value

def hotel_room_formatter(json_hotels) -> dict:
    '''
    This function blend the data from json_rooms_information, json_meal_plans_information and json_available_regimens to a unique 
    hotel JSON.

    @param json_hotels: Hotel dictionary where the room information is supposed to be injected
    @return: It returns a dictionary of hotels with their rooms associated
    '''
    for room_information in json_rooms_information['rooms_type']:
        for available_hotel in room_information['hotels']:
            room = dict()
            room['name'] = room_information['name']
            room['room_type']  = room_type_normalization(room_information['code'])
            room['meal_plan'] = 0
            room['price'] = 0
            for hotel in json_hotels['hotels']:
                if hotel['code'] == available_hotel:
                    if 'rooms' in hotel:
                        hotel['rooms'].append(room)
                    else:
                        hotel['rooms'] = [room]
    return json_hotels


def punto_uno() -> str:
    return json.dumps(hotel_room_formatter(json_api_hoteles_atalaya), indent=1)






