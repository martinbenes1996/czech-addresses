#!/usr/bin/env python3

#import offlineData as offline
#import onlineData as online

if __name__ == "__main__":
    
    online.init()
    offline.init()
    #offline.refresh_regions()
    #offline.refresh_cities()
    
    #regions = offline.fetch_regions()
    #for region in regions:
    #    print(region)
    
    #offline.print_statistics()
    
    for post in online.get_tetcice():
        print(post["attributes"]["name"])