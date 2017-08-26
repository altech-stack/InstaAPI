from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

import json
import requests

class API():

    def __init__(self):
        pass


    @staticmethod
    @app.route('/api/v1.0/instapi', methods=['GET'])
    def get_instapi():
        print "lol"
        results = {}
        results['output'] = 'Success'
        return jsonify({'result': results})


    @staticmethod
    @app.errorhandler(404)
    @cross_origin()
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    def run(self,debug=False,port=5000):
        self.app.run(port=port, debug=debug,host='0.0.0.0', threaded=True)


ab = API()
ab.run(True)
