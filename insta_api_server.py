from flask import Flask, request, jsonify, make_response,render_template
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import datetime
import json
import requests

class API():
    @staticmethod
    def find_between(s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
    @staticmethod
    def get_page_content(url):
        headers = {'Accept-Encoding': 'identity'}

        page = ""
        try:
            page = requests.get(url,headers=headers)
        except:
            print "Error with GET Request"

        return page.content

    @staticmethod
    def get_json_from_source(text):
        split_text = text.split('\n')
        json_string = {}
        for line in split_text:
            if "script" in line and 'sharedData' in line:
                json_string = line

        json_output = API.find_between(json_string,'window._sharedData = ',';</script>')

        try:
            json_output = json.loads(json_output)
        except:
            print "Error loading json"

        return json_output

    @staticmethod
    def extract_insta_data_from_json(insta_json):
        # If user is public
        user_info = insta_json.get('entry_data').get('ProfilePage')[0].get('user')
        return user_info

    app = Flask('insta-api-server')

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    INSTAGRAM_ENDPOINT = "https://instagram.com/"

    mongo_config = {
        'host': 'localhost',
        'port': 27017
    }

    mongo = MongoClient(mongo_config['host'],int(mongo_config['port']))

    @app.template_filter()
    def datetimefilter(value, format='%Y/%m/%d %H:%M'):
        """convert a datetime to a different format."""
        return value.strftime(format)

    app.jinja_env.filters['datetimefilter'] = datetimefilter

    def __init__(self):
        pass


    @staticmethod
    @app.route('/api/v1.0/instapi/<user>', methods=['GET'])
    def get_instapi(user):
        try:
            html = API.get_page_content(API.INSTAGRAM_ENDPOINT+user)
            insta_json = API.get_json_from_source(html)
            consolidated_data = API.extract_insta_data_from_json(insta_json)
        except:
            print "Unable to get user, or user does not exist"
            consolidated_data = {
                'status':"User does not exist"
            }
        return jsonify({'result': consolidated_data})
    @staticmethod
    @app.route("/")
    def template_test():
        return render_template('template.html', my_string="Wheeeee!",
                               my_list=[0, 1, 2, 3, 4, 5], title="Index", current_time=datetime.datetime.now())

    @staticmethod
    @app.route("/home")
    def home():
        return render_template('template.html', my_string="Foo",
                               my_list=[6, 7, 8, 9, 10, 11], title="Home", current_time=datetime.datetime.now())

    @staticmethod
    @app.route("/about")
    def about():
        return render_template('template.html', my_string="Bar",
                               my_list=[12, 13, 14, 15, 16, 17], title="About", current_time=datetime.datetime.now())

    @staticmethod
    @app.route("/contact")
    def contact():
        return render_template('template.html', my_string="FooBar"
                               , my_list=[18, 19, 20, 21, 22, 23], title="Contact Us",
                               current_time=datetime.datetime.now())

    @staticmethod
    @app.errorhandler(404)
    @cross_origin()
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    def run(self,debug=False,port=5000):
        self.app.run(port=port, debug=debug,host='0.0.0.0', threaded=True)


ab = API()
ab.run(True)
