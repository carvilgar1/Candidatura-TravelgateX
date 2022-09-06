from punto_uno import punto_uno

from punto_dos import punto_dos

from flask import Flask, jsonify

api = Flask(__name__)

@api.route('/hotelList', methods=['GET'])
def get_standardized_hotels():
  return jsonify(punto_uno())

@api.route('/itineraryCancun/<int:budget>', methods=['GET'])
def get_itinerary(budget):
  return jsonify(punto_dos(budget))

if __name__ == '__main__':
    api.run() 
    