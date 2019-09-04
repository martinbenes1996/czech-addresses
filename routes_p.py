
import urllib.request
import json
import os

# ssl
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

import re

# flask
from flask import Flask
from flask import render_template, abort
app = Flask(__name__)

# psc
import sys
sys.path.insert(0, './static')
import psc



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/osobni/<int:pagenum>")
def tax_private(pagenum):
    if pagenum < 1 or pagenum > 3:
        abort(404)
    
    # regions
    regions = {}
    if pagenum == 1:
        regions = address_getRegions()

    return render_template("tax_private.html", pagenum=pagenum, regions=regions)

@app.route("/firemni/<int:pagenum>")
def tax_business(pagenum):
    return render_template("tax_business.html", pagenum=pagenum)

@app.route("/profile")
def show_profile():
    return render_template("profile.html", username="Foo")


# address api
@app.route("/address/getCityCode/<string:cityName>/<int:regionId>")
@app.route("/address/getCityCode/<string:cityName>")
def address_getCityCode(cityName, regionId=None):
    rqarg = urllib.urlencode({'cityOrPart' : cityName})
    rqurl = 'https://b2c.cpost.cz/services/PostCode/getDataAsJson?' + rqarg
    jsonCities = urllib.request.urlopen(rqurl).read()
    print(jsonCities)
    return jsonCities

@app.route("/address/getPostName/<int:cityCode>")
def address_getPostName(cityCode):
    try:
        return psc.cities[cityCode]
    except:
        abort(404)

def cityName2rawName(cityName):
    rawName = re.sub(r"(.*)( u .*)",
                    r"\1",
                    cityName)
    return rawName

@app.route("/address/getRegion/<int:cityCode>")
def address_getRegion(cityCode):
    postName = address_getPostName(cityCode)
    cityName = address_getCityName(cityCode)
    rawName = cityName2rawName(cityName)

    rqarg = 'cityOrPart='+urllib.parse.quote_plus(cityName)
    rqurl = 'https://b2c.cpost.cz/services/PostCode/getDataAsJson?' + rqarg
    cities = json.loads( urllib.request.urlopen(rqurl).read() )

    rqarg = 'cityOrPart='+urllib.parse.quote_plus(rawName)
    rqurl = 'https://b2c.cpost.cz/services/PostCode/getDataAsJson?' + rqarg
    cities += json.loads( urllib.request.urlopen(rqurl).read() )

    idDistrict = None
    print(cityName, ":", cityCode)
    for city in cities:
        print(city['name'], ":", city['postCode'])
        if int(city['postCode']) == cityCode:
            idDistrict = int(city['idRegion'])
            break
    print(idDistrict)
    if not idDistrict:
        abort(404)

    regions = address_getRegions()
    print(regions)
    for region in regions:
        districts = address_getDistricts(region['id'])
        print(districts)
        for district in districts:
            if int(district['id']) == idDistrict:
                return json.dumps(region)
    abort(404)

@app.route("/address/getCityName/<int:cityCode>")
def address_getCityName(cityCode):
    postName = address_getPostName(cityCode)
    cityName = re.sub(r"(Výdejní místo )(.*)",
                    r"\2",
                    postName)
    cityName = re.sub(r"(.*)( [0-9]+)",
                    r"\1",
                    cityName)
    return cityName

@app.route("/address/check/<int:cityCode>/<string:streetName>/<string:houseNumber>")
def address_checkAddress(cityCode, streetName, houseNumber):
    cityName = address_getCityName(cityCode)
    rawName = cityName2rawName(cityName)

    rqarg = 'cityOrPart='+urllib.parse.quote_plus(cityName)
    rqurl = 'https://b2c.cpost.cz/services/PostCode/getDataAsJson?' + rqarg
    cities = json.loads( urllib.request.urlopen(rqurl).read() )
    rqarg = 'cityOrPart='+urllib.parse.quote_plus(rawName)
    rqurl = 'https://b2c.cpost.cz/services/PostCode/getDataAsJson?' + rqarg
    cities += json.loads( urllib.request.urlopen(rqurl).read() )

    regionId = None
    for city in cities:
        if int(city['postCode']) == cityCode:
            regionId = city['idRegion']
            break
    if not regionId:
        abort(404)
    
    rqarg = 'id='+str(regionId)
    rqurl = 'https://b2c.cpost.cz/services/Address/getCityListAsJson?' + rqarg
    cities = json.loads( urllib.request.urlopen(rqurl).read() )

    cityId = None
    for city in cities:
        if city['name'] == cityName or city['name'] == rawName:
            cityId = city['id']
            break
    if not cityId:
        abort(404)

    print("city ID:", cityId)

    rqarg = 'id='+str(cityId)
    rqurl = 'https://b2c.cpost.cz/services/Address/getCityPartListAsJson?' + rqarg
    cityparts = json.loads( urllib.request.urlopen(rqurl).read() )

    for part in cityparts:
        rqarg = 'id='+str(part['id'])
        rqurl = 'https://b2c.cpost.cz/services/Address/getStreetListAsJson?' + rqarg
        streets = json.loads( urllib.request.urlopen(rqurl).read() )

        print(streets)

        for street in streets:
            print(street["name"], streetName)
            if street['name'] == streetName:
                print("street:", street["id"])

                rqurl = 'https://b2c.cpost.cz/services/Address/getNumberListAsJson?idStreet=' + str(street['id'])
                houses = json.loads( urllib.request.urlopen(rqurl).read() )

                for house in houses:
                    print("House number:", house["name"])
                    if house['name'] == houseNumber:
                        return "OK"
                    elif len(house['name'].split('/')) > 1:
                        if house['name'].split('/')[1] == houseNumber:
                            return "OK"

    abort(404)
    
@app.route("/address/getRegions")
def address_getRegions():
    jsonRegions = urllib.request.urlopen('https://b2c.cpost.cz/services/Address/getRegionListAsJson').read()
    return sorted(json.loads(jsonRegions), key=lambda i: int(i['id']))

@app.route("/address/getDistricts/<int:regionId>")
def address_getDistricts(regionId):
    jsonRegions = urllib.request.urlopen('https://b2c.cpost.cz/services/Address/getDistrictListAsJson?id='+regionId).read()
    return json.loads(jsonRegions)

@app.route("/address/getLocation/<int:cityCode>")
def address_getLocation(cityCode):
    d = { 'name' : address_getCityName(cityCode), 'region' : json.loads(address_getRegion(cityCode))['name'] }
    return json.dumps(d)


if __name__ == '__main__':
    app.run()