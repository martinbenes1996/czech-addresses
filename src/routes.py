
import functools
import json
import os
import re
import sys
import time
import urllib.request
# flask
import flask
from flask import render_template, request, abort
app = flask.Flask(__name__)

# ssl
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context
    
sys.path.append('.')
import offlineData as offline
import onlineData as online

def key_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == "abcd":
            return f(*args, **kwargs)
        time.sleep(3)
        return "Unauthorized.",401
    return decorated_function

@app.route("/")
@key_required
def index():
    #return "Hello, World!"
    return render_template("index.html")

@app.route("/posts/gps")
@key_required
def gps_posts():
    print(request.query_string)
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    posts = online.locate_posts((lat,lon))
    result = {"posts": posts}
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json')
    return response
    return result

# address api
#@app.route("/address/getCityCode/<string:cityName>/<int:regionId>")
#def cityName2rawName(cityName):
#    rawName = re.sub(r"(.*)( u .*)",
#                    r"\1",
#                    cityName)
#    return rawName

#@app.route("/address/getRegion/<int:cityCode>")

if __name__ == '__main__':
    app.run()