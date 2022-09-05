from punto_uno import punto_uno

from flask import Flask, jsonify

api = Flask(__name__)

@api.route('/punto_uno', methods=['GET'])
def get_standardized_hotels():
  return jsonify(punto_uno())

if __name__ == '__main__':
    api.run() 
    