
class CityContext:
    def __init__(self, region_id, district_id):
        self.region_id = int(region_id)
        self.district_id = int(district_id)
    def __str__(self):
        return f"<CityContext {self.region_id},{self.district_id}>"
    def int_or_None(self, identifier):
        try:
            return int(id)
        except:
            if identifier == None:
                return None
        raise Exception("id neither int nor None")
    
class StreetContext(CityContext):
    def __init__(self, region_id, district_id, city_id, city_part_id = None):
        super().__init__(region_id, district_id)
        self.city_id = int(city_id)
        self.city_part_id = int(city_part_id)
    def __str__(self):
        return f"<StreetContext {self.city_id},{self.city_part_id}>"
    
class AddressContext(StreetContext):
    def __init__(self, region_id, district_id, city_id, city_part_id=None, street_id=None):
        super().__init__(region_id, district_id, city_id, city_part_id)
        self.street_id = self.int_or_None(street_id)
    def __str__(self):
        return f"<Address {self.street_id},{self.city_id}>"
    def streetless(self):
        return self.street_id == None
