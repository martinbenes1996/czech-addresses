#!/usr/bin/env python3

from datetime import datetime
import offlineData as offline
import onlineData as online

if __name__ == "__main__":
    
    online.init()
    offline.init()
    #offline.refresh_regions()
    #offline.refresh_cities()
    
    
    #regions = offline.fetch_regions()
    #for region in regions:
    #    print(region)
    
    cities = offline.fetch_cities()
    city_cnt = 0
    region_ids,district_ids = set(),set()
    for city,city_context in cities:
        region_ids.add(city_context.region_id)
        district_ids.add(city_context.district_id)
        city_cnt += 1
    print("Regions:", len(region_ids))
    print("Districts:", len(district_ids))
    print("Cities:", city_cnt)