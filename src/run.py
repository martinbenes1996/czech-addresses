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
    city_ids = set()
    for city,city_context in cities:
        city_ids.add(city_context.district_id)
        city_cnt += 1
    
    print("Districts:", len(city_ids))
    print("Cities:", city_cnt)