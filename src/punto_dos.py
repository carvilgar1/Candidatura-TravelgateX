from punto_uno import punto_uno
from punto_uno import MealPlan 
from punto_uno import RoomType

NIGHTS_IN_MALAGA = 3
NIGHTS_IN_CANCUN = 5
ROOM_TYPE = RoomType.SUITE

def price_calculator(nights_in_malaga,malaga_room, nights_in_cancun, cancun_room) -> int: 
        '''Returns the total cost of the itinenary. If no itinenary then returns 0'''
        if malaga_room == None:
            return 0
        return nights_in_malaga*malaga_room['price'] + nights_in_cancun*cancun_room['price']

def find_best_itinerary_algorithm(json_malaga, json_cancun, budget):
    '''
    Find the best itinerary through a greedy algorithm that follows a heuristic that tries to maximize the 
    budget for the hotel in Malaga and finds any option that meets the requirements for the hotel in Cancun.

    @param budget: Budget specified by the client in the request to the endpoint.
    @return: JSON formatted dictionary that contains the best itinerary for the required budget.
    '''
    price_predicate = lambda price: price <= budget

    best_combination = (None, None)

    for malaga_room in json_malaga['rooms']:
        if malaga_room['room_type'] == ROOM_TYPE:
            if not best_combination[0] == None:
                #Lets try to find a preliminar valid path from starting point. function returns a (null, null) tuple if cant find a valid solution, this
                #is the duty of this if statement.
                if not(best_combination[0]['price'] < malaga_room['price']):
                        continue
            else:
                for cancun_room in json_cancun['rooms']:
                    if not(cancun_room['meal_plan'] == MealPlan.ACCOMMODATION_AND_BREAKFAST and cancun_room['room_type'] == ROOM_TYPE and 
                            price_predicate(price_calculator(NIGHTS_IN_MALAGA, malaga_room, NIGHTS_IN_CANCUN, cancun_room))):
                        continue
                    best_combination = (malaga_room, cancun_room)
                    break
    return best_combination

def punto_dos(budget):
    json_hotel = punto_uno()
   
    json_malaga = next(filter(lambda hotel: hotel['city'] == 'Malaga', json_hotel['hotels']))
    json_cancun = next(filter(lambda hotel: hotel['city'] == 'Cancun', json_hotel['hotels']))

    best_combination = find_best_itinerary_algorithm(json_malaga, json_cancun, budget)
    json_malaga['rooms'] = best_combination[0]
    json_cancun['rooms'] = best_combination[1]

    return {'nights_in_malaga': NIGHTS_IN_MALAGA, 'nights_in_cancun': NIGHTS_IN_CANCUN, 
                'total_price': price_calculator(NIGHTS_IN_MALAGA, best_combination[0], NIGHTS_IN_CANCUN, best_combination[1]), 'hotels' : [json_malaga, json_cancun]}
