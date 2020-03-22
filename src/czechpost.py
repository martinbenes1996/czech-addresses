
import datetime
import json
import requests

hostname = 'https://b2c.cpost.cz'


# ssl
import ssl
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
class Tlsv1HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_TLSv1)
def _request(url, *args, **kwargs):
    s = requests.Session()
    s.mount(url, Tlsv1HttpAdapter())
    return s.get(url, *args, **kwargs, verify=False)

def get_regions():
    response = _request(hostname + '/services/Address/getRegionListAsJson')
    regions = sorted(response.json(), key=lambda i: int(i['id']))
    return regions

def get_districts(region_id):
    response = _request(hostname + '/services/Address/getDistrictListAsJson', params={"id": int(region_id)})
    districts = response.json()
    print(f"fetched {len(districts)} from region {region_id}")
    #print(districts)
    return districts

def get_cities(district_id):
    response = _request(hostname + '/services/Address/getCityListAsJson', params={"id": int(district_id)})
    cities = response.json()
    print(f"fetched {len(cities)} cities from district {district_id}")
    #print(cities)
    return cities

def get_city_parts(city_id):
    response = _request(hostname + '/services/Address/getCityPartListAsJson', params={"id": int(city_id)})
    cities = response.json()
    print(cities)
    return cities
def get_streets(city_part_id):
    response = _request(hostname + '/services/Address/getStreetListAsJson', params={"id": int(city_part_id)})
    streets = response.json()
    print(streets)
    return streets

def get_addresses(street_id=None, city_part_id=None):
    addresses_street, addresses_city_part = [],[]
    if street_id is not None:
        response_street = _request(hostname + '/services/Address/getNumberListAsJson', params={"idStreet": street_id})
        addresses_street = response_street.json()
    if city_part_id is not None:
        response_city_part = _request(hostname + '/services/Address/getNumberListAsJson', params={"idCityPart": city_part_id})
        addresses_city_part = response_city_part.json()
    print("street:", addresses_street)
    print("city part:", addresses_city_part)
    addresses = [*addresses_street, *addresses_city_part]
    print(addresses)
    return addresses

def parse_post_offices_filters(kwargs):
    filters = {
        "deliveryToPostOffice": False,
        "deliveryToHand": False,
        "sale": False, # sale of newspapers
        "copyService": False,
        "czechpoint": False,
        "atmCSOB": False,
        "stickerHighway": False,
        "westernUnion": False,
        "saturday": False, # opened on Saturdays
        "sundayAndHoliday": False, # opened on Sundays
        "shopingCenter": False, # in shopping center
        "parking": False,
        "extendedOpeningHours": False,
        "postalAgency": False, # service of insurance company
        "parcelService": False, # service of parcel service
    }
    custom_filters = {}
    for f in set(kwargs.keys()):
        if f == "language":
            if kwargs[f] in {"cs","en"}:
                custom_filters["language"] = kwargs[f]
            else:
                raise Exception("Unsupported language: \"" + kwargs[f] + "\"")
        elif f in set(filters.keys()):
            custom_filters[f] = str(int(bool(kwargs[f])))
        else:
            raise Exception("Unsupported filter: \"" + f + "\"")
    return custom_filters
def get_post_offices_by_post_code(post_code, **kwargs):
    filters = parse_post_offices_filters(kwargs)
    response = _request(hostname + '/services/PostOfficeInformation/v2/getDataAsJson', params={"postCode": post_code, **filters})
    post_offices = response.json()
    print(post_offices)
    return post_offices
def get_post_offices_by_city_name(city_name, **kwargs):
    filters = parse_post_offices_filters(kwargs)
    response = _request(hostname + '/services/PostOfficeInformation/v2/getDataAsJson', params={"place": city_name, **filters})
    post_offices = response.json()
    print(post_offices)
    return post_offices
def get_post_offices_by_district_id(district_id, **kwargs):
    filters = parse_post_offices_filters(kwargs)
    response = _request(hostname + '/services/PostOfficeInformation/v2/getDataAsJson', params={"idDistrict": district_id, **filters})
    post_offices = response.json()
    print(post_offices)
    return post_offices
def get_post_offices_by_gps(lat, lon, **kwargs): # to make it working call to ceska posta
    filters = parse_post_offices_filters(kwargs)
    def stringify_gps(x):
        degrees = int(x)
        minutes = int(abs(x-degrees)*60)
        seconds = round(abs(x-(degrees + minutes/60))*60,1)
        return f"{degrees}°{minutes}'{seconds}\""
    gps = f"{stringify_gps(lat)}N,{stringify_gps(lon)}E"
    print(gps)
    # 49°54'56.4"N,14°09'06.2"E
    response = _request(hostname + '/services/PostOfficeInformation/v2/getDataAsJson', params={"gps": gps, **filters})
    post_offices = response.json()
    return post_offices

def get_changes_from(date_from=None):
    if date_from is None:
        date_from = datetime.now()
    date_from = date_from.strftime("%Y-%m-%d %H:%M:%S")
    response = _request(hostname + '/services/PostOfficeInformation/getUpdatedPostAsJson', params={"date": date_from})
    print(response.text)
    
