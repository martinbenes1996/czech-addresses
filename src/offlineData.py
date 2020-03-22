
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
        
def fetch_cities(region_id):
    result = db.get_cities_by_region(region_id)
    print(result)
    
    
    
    
