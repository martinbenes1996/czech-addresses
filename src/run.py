#!/usr/bin/env python3

from datetime import datetime
import offlineData as offline
import onlineData as online

if __name__ == "__main__":
    
    online.init()
    offline.init()
    #offline.refresh_regions()
    offline.refresh_cities()
    
    
    #regions = offline.fetch_regions()
    #for region in regions:
    #    print(region)
    
    #cities = offline.fetch_cities(11)
    #for city in cities:
    #    print(city)