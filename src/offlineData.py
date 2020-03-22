
import sys
sys.path.append(".")
import context
import db
import onlineData as online

def init():
    db.init()
    
def refresh_regions():
    regions = online.fetch_regions()
    db.set_regions(regions)
def refresh_cities():
    regions = db.get_regions()
    for region in regions:
        cities_generator = online.fetch_cities(region["id"])
        for cities,city_context in cities_generator:
            db.set_cities(cities, city_context)

def fetch_regions():
    return db.get_regions()
        
def fetch_cities(region_id=None):
    result = db.get_cities(region_id)
    return result

def print_statistics():
    cities = fetch_cities()
    city_cnt = 0
    region_ids,district_ids = set(),set()
    for city,city_context in cities:
        region_ids.add(city_context.region_id)
        district_ids.add(city_context.district_id)
        city_cnt += 1
    print("Offline statistics:")
    print("| Regions:", len(region_ids))
    print("| Districts:", len(district_ids))
    print("| Cities:", city_cnt)
    
    
    
    
