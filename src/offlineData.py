
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
        c = context.RegionContext()
        c.region_id = region["id"]
        c.region_name = region["name"]
        cities = online.fetch_cities(c)
        db.set_cities(cities)

def fetch_regions():
    regions = db.get_regions()
    for region in regions:
        c = context.RegionContext()
        c.region_id = region["id"]
        c.region_name = region["name"]
        yield c
def fetch_cities(region_id):
    result = db.get_cities_by_region(region_id)
    print(result)
    
    
    
    
