import re
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from search import search
from nucleus_medTTS import *
from utils import stopword_removal

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, supports_credentials=True)


@app.route('/speech', methods=['GET', 'POST'])
# @cross_origin(origin='http://localhost:8080')
def speech(network=True):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        query = post_data["query"]
        print(query)        
        
        query = stopword_removal(query)
        print(query)

        res = search(query)
        print(len(res["response"]["docs"]))

        if network:
        # to nucleus_medTTS.py then return results 
            response_object["QNum"] = len(res["response"]["docs"])
            response_object["docs"] = network_search(res["response"]["docs"]) 
            return jsonify(response_object)
            # raise NotImplementedError

        else:
            # restructure json 
            response_object["QTime"] = res["responseHeader"]["QTime"]

            response_object["docs"] = {}
            # convert docs string to json
            for i in range(len(res["response"]["docs"])):
                response_object['docs'][i] = res["response"]["docs"][i]

            print(response_object['docs'])
            return jsonify(response_object)


# connction check route
@app.route('/ping', methods=['GET'])
@cross_origin(origin='*')
def ping_pong():
    return jsonify('pong!')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
