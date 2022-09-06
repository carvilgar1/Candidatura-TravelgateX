from punto_uno import punto_uno
from punto_uno import MealPlan 
from punto_uno import RoomType

def punto_dos(budget):
    '''
    Find the best itinerary through a greedy algorithm that follows a heuristic that tries to maximize the 
    budget for the hotel in Malaga and finds any option that meets the requirements for the hotel in Cancun.

    @param budget: Budget specified by the client in the request to the endpoint.
    @return: JSON formatted dictionary that contains the best itinerary for the required budget.
    '''
    def price_predicate(nights_in_malaga,malaga_room, nights_in_cancun, cancun_room, total_budget) -> bool: 
        '''Returns true if the total price is within the budget limits and false otherwise'''
        return nights_in_malaga*malaga_room['price'] + nights_in_cancun*cancun_room['price'] <= total_budget
    
    json_hotel = punto_uno()
   
    json_malaga = next(filter(lambda hotel: hotel['city'] == 'Malaga', json_hotel['hotels']))
    json_cacun = next(filter(lambda hotel: hotel['city'] == 'Cancun', json_hotel['hotels']))
    
    best_combination = (None, )

    for malaga_room in json_malaga['rooms']:
        if not best_combination[0] == None:
            if not(best_combination[0]['price'] < malaga_room['price'] and malaga_room['room_type'] == RoomType.SUITE):
                continue
        for cancun_room in json_cacun['rooms']:
            if not(cancun_room['meal_plan'] == MealPlan.ACCOMMODATION_AND_BREAKFAST and cancun_room['room_type'] == RoomType.SUITE and 
                    price_predicate(3, malaga_room, 5, cancun_room, budget)):
                continue
            best_combination = (malaga_room, cancun_room)
            break
           

    json_malaga['rooms'] = best_combination[0]
    json_cacun['rooms'] = best_combination[1]

    return {'hotels' : [json_malaga, json_cacun]}
