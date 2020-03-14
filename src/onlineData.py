
import sys
sys.path.append(".")
import czechpost as cpost
import context

def init():
    pass

def fetch_regions():
    regions = cpost.get_regions()
    for r in regions:
        region = {'id': r['id'], 'name': r['name']}
        yield region
        
def get_region_name(region_id):
    for region in fetch_regions():
        if region.region_id == int(region_id):
            return region.region_name
    raise Exception("Unknown region: \"" + str(region_id) + "\"")

def get_district_name(region_id, district_id):
    for district in cpost.get_districts(region_id):
        if int(district["id"]) == int(district_id):
            return district["name"]
    raise Exception("Unknown district: \"" + str(district_id) + "\"")

def fetch_cities(region_id):
    districts = cpost.get_districts(region_id)
    for district in districts:
        cities = cpost.get_cities(district["id"])
        for city in cities:
            city_context = context.CityContext(region_id, int(district["id"]))
            yield {"id": int(city["id"]), "name": city["name"]}, city_context
            
def fetch_streets(street_context):
    if street_context.region_name is None:
        street_context.region_name = get_region_name(street_context.region_id)
    if street_context.district_name is None:
        street_context.district_name = get_district_name(street_context.region_id, street_context.district_id)
    city_parts = cpost.get_city_parts(street_context.city_id)
    for city_part in city_parts:
        streets = cpost.get_streets(city_part["id"])
        for street in streets:
            c = context.StreetContext()
            c.region_id = street_context.region_id
            c.region_name = street_context.region_name
            c.district_id = street_context.district_id
            c.district_name = street_context.district_name
            c.city_id = street_context.city_id
            c.city_name = street_context.city_name
            c.city_part_id = int(city_part["id"])
            c.city_part_name = city_part["name"]
            c.street_id = int(street["id"])
            c.street_name = street["name"]
            yield c


        
    