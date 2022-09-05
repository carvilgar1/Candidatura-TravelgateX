import json

from enum import Enum

from urllib.request import urlopen


class RoomType(str, Enum):
    STANDARD = 'STANDARD'
    SUITE = 'SUITE'

class MealPlan(str, Enum):
    FULL_BOARD = 'FULL_BOARD'
    HALF_BOARD = 'HALF_BOARD'
    ACCOMMODATION_ONLY = 'ACCOMMODATION_ONLY'
    ACCOMMODATION_AND_BREAKFAST = 'ACCOMMODATION_AND_BREAKFAST'

#API endpoints
url_api_hoteles_atalaya = 'http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253'
url_api_resort_hoteles = 'http://www.mocky.io/v2/5e4e43272f00006c0016a52b'
url_rooms_information = 'https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036'
url_meal_plans_information = 'http://www.mocky.io/v2/5e4a7e282f0000490097d252'
url_available_regimens = 'http://www.mocky.io/v2/5e4a7dd02f0000290097d24b'

#JSON formatted gotten from the previous urls are converted to Python object
json_api_hoteles_atalaya = json.loads(urlopen(url_api_hoteles_atalaya).read()) 
json_api_resort_hoteles = json.loads(urlopen(url_api_resort_hoteles).read())
json_rooms_information = json.loads(urlopen(url_rooms_information).read())
json_meal_plans_information = json.loads(urlopen(url_meal_plans_information).read())
json_available_regimens = json.loads(urlopen(url_available_regimens).read())

def room_type_normalization(room_str) -> RoomType:
    '''
    This function converts the string that contains room's information 
    into standardized Enum type of the company.
    '''
    if room_str in {'st', 'standard'}:
        return RoomType.STANDARD
    else:
        return RoomType.SUITE

def meal_plans_normalization(meal_plan_str) -> MealPlan:
    '''
    This function converts the string that represents a meal plan
    into standardized Enum type of the company.
    '''
    if meal_plan_str == 'pc':
        return MealPlan.FULL_BOARD
    elif meal_plan_str == 'mp':
        return MealPlan.HALF_BOARD
    elif meal_plan_str == 'sa':
        return MealPlan.ACCOMMODATION_ONLY
    else:
        return MealPlan.ACCOMMODATION_AND_BREAKFAST

def atalaya_hotel_standardization() -> None:
    '''
    This function takes the data provided by url_rooms_information, iterates over it
    and creates a temporary dictionary with room information and meal plans (provided by json_meal_plans_information). Finally, the new
    dictionary is embedded along with the rest of the hotel information.
    '''
    for room_information in json_rooms_information['rooms_type']:
        for available_hotel in room_information['hotels']:
            room = dict()
            room['name'] = room_information['name']
            room['room_type']  = room_type_normalization(room_information['code'])
            room['meal_plans'] = [{'name': meal_plans_normalization(meal_plan['code']), 'price': room_price['price']} 
                #Meal plans, whose hotel matches the hotel of the room being formatted, are filtered
                for meal_plan in json_meal_plans_information['meal_plans'] if available_hotel in meal_plan['hotel']
                #This second filter selects the meal plans whose room_type match with current room
                for room_price in meal_plan['hotel'][available_hotel] if room['room_type'] == room_type_normalization(room_price['room'])
                ]
            
            for hotel in json_api_hoteles_atalaya['hotels']:
                if hotel['code'] == available_hotel:
                    if 'rooms' in hotel:
                        hotel['rooms'].append(room)
                    else:
                        hotel['rooms'] = [room]


def hotel_resort_standardization() -> None:
    '''
    This function inserts the missing information about meal plans of hotel resort API, which
    is found in url_available_regimens variable, to meet with company's API standard.
    '''
    for hotel in json_api_resort_hoteles['hotels']:
        for room in hotel['rooms']:
            room['room_type']  = room_type_normalization(room['code'])
            del room['code']
            for meal_plan in json_available_regimens['regimenes']:
                if meal_plan['hotel'] == hotel['code'] and room['room_type'] == room_type_normalization(meal_plan['room_type']):
                    if 'meal_plans' in meal_plan:
                        room['meal_plans'].append( {'name': meal_plans_normalization(meal_plan['code']), 'price': meal_plan['price']} )
                    else:
                        room['meal_plans'] = [ {'name': meal_plans_normalization(meal_plan['code']), 'price': meal_plan['price']} ]

def punto_uno() -> dict:
    '''
    This function returns the standardized JSON demanded by the Company.
    It also create a local file with .json extension.
    '''
    atalaya_hotel_standardization()
    hotel_resort_standardization()
    json_api_hoteles_atalaya['hotels'].extend(json_api_resort_hoteles['hotels'])
    with open('punto_uno.json', 'w+') as f:
        f.write(json.dumps(json_api_hoteles_atalaya, indent=1))
    return json_api_hoteles_atalaya






