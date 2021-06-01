from flask import Flask,request,jsonify
from flask_cors import CORS
import recommendation
from json import dumps

app = Flask(__name__)
CORS(app) 
        
@app.route('/dest', methods=['GET'])
def recommend_destinations():
        res = recommendation.results(request.args.get('title'))
        return dumps(res, indent=2)

if __name__=='__main__':
        app.run(port = 5000, debug = True)
