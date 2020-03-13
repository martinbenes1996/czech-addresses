
class RegionContext:
    def __init__(self):
        self.region_id = None
        self.region_name = None
    def __str__(self):
        return "<Region \"" + self.region_name + "\">"
class CityContext(RegionContext):
    def __init__(self):
        super().__init__()
        self.district_id = None
        self.district_name = None
        self.city_id = None
        self.city_name = None
    def __str__(self):
        return "<City \"" + self.city_name + "\">"
    
class StreetContext(CityContext):
    def __init__(self):
        super().__init__()
        self.city_part_id = None
        self.city_part_name = None
        self.street_id = None
        self.street_name = None
    def __str__(self):
        return "<Street \"" + self.street_name + "\">"
class AddressContext(StreetContext):
    def __init__(self):
        super().__init__()
        self.address_id = None
        self.address_name = None
    def __str__(self):
        return "<Address \"" + self.street_name + " " + self.address_name + "\">"
