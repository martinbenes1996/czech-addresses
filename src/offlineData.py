
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
        cities = online.fetch_cities(region["id"])
        for city,city_context in cities:
            db.set_city(city, city_context)

def fetch_regions():
    regions = db.get_regions()
    for region in regions:
        print(region)
        
def fetch_cities(region_id):
    result = db.get_cities_by_region(region_id)
    print(result)
    
    
    
    
