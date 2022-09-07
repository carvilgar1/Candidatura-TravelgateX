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
URL_API_HOTELES_ATALAYA = 'http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253'
URL_API_RESORT_HOTELES = 'http://www.mocky.io/v2/5e4e43272f00006c0016a52b'
URL_ROOMS_INFORMATION = 'https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036'
URL_MEAL_PLANS_INFORMATION = 'http://www.mocky.io/v2/5e4a7e282f0000490097d252'
URL_AVAILABLE_REGIMENS = 'http://www.mocky.io/v2/5e4a7dd02f0000290097d24b'


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

def atalaya_hotel_api_standardization() -> dict:
    '''
    This function takes the data provided by url_rooms_information, iterates over it
    and creates a temporary dictionary with room information and meal plans (provided by json_meal_plans_information). Finally, the new
    dictionary is embedded along with the rest of the hotel information.
    '''
    json_api_hoteles_atalaya = json.loads(urlopen(URL_API_HOTELES_ATALAYA).read()) 
    json_rooms_information = json.loads(urlopen(URL_ROOMS_INFORMATION).read())
    json_meal_plans_information = json.loads(urlopen(URL_MEAL_PLANS_INFORMATION).read())

    result = {'hotels' : []}
    for hotel in json_api_hoteles_atalaya['hotels']:
        formatted_hotel = dict()
        formatted_hotel['code'] = hotel['code']
        formatted_hotel['name'] = hotel['name']
        formatted_hotel['city'] = hotel['city']
        formatted_hotel['rooms'] = []
        for room_information in json_rooms_information['rooms_type']:
            for available_hotel in room_information['hotels']:
                if hotel['code'] == available_hotel:
                    for meal_plan in json_meal_plans_information['meal_plans']:
                        room = dict()
                        room['name'] = room_information['name']
                        room['room_type']  = room_type_normalization(room_information['code'])
                        
                        for room_price in meal_plan['hotel'][available_hotel]: 
                            if room['room_type'] == room_type_normalization(room_price['room']):
                                room['meal_plan']  = meal_plans_normalization(meal_plan['code'])
                                room['price']  = room_price['price']
                        formatted_hotel['rooms'].append(room)
        result['hotels'].append(formatted_hotel)
    return result

def resort_hotel_api_standardization() -> dict:
    '''
    This function inserts the missing information about meal plans of hotel resort API, which
    is found in url_available_regimens variable, to meet with company's API standard.
    '''
    json_api_resort_hoteles = json.loads(urlopen(URL_API_RESORT_HOTELES).read())
    json_available_regimens = json.loads(urlopen(URL_AVAILABLE_REGIMENS).read())
    
    result = {'hotels' : []}
    for hotel in json_api_resort_hoteles['hotels']:
        formatted_hotel = dict()
        formatted_hotel['code'] = hotel['code']
        formatted_hotel['name'] = hotel['name']
        formatted_hotel['city'] = hotel['location']
        formatted_hotel['rooms'] = []
        for regime in json_available_regimens['regimenes']:
            if regime['hotel'] == hotel['code']:
                room = dict()
                room['name'] = regime['name']
                room['room_type']  = room_type_normalization(regime['code'])
                room['meal_plan']  = meal_plans_normalization(regime['code'])
                room['price']  = regime['price']
                formatted_hotel['rooms'].append(room)
        result['hotels'].append(formatted_hotel)
    return result

def punto_uno() -> dict:
    '''
    This function returns the standardized JSON demanded by the Company.
    '''
    x = atalaya_hotel_api_standardization()
    y = resort_hotel_api_standardization()
    x['hotels'].extend(y['hotels'])
    return x






