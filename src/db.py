
import sqlalchemy
import sqlalchemy.orm.session as session

import context

Region,City = None,None

class Session:
    SessionGenerator = None
    @classmethod
    def set_session_maker(cls, bind):
        cls.SessionGenerator = session.sessionmaker(bind=bind)
    def __init__(self):
        self.session = self.SessionGenerator()
    def __enter__(self):
        return self.session
    def _finilize(self):
        if self.session is None:
            return
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print("Commit error, rollback: " + e.message)
        self.session.close()
        self.session = None
    def __exit__(self, type, value, traceback):
        if type is not None:
            print("Error, rollback: " + value)
            self.session.rollback()
            self.session.close()
            self.session = None
        else:
            self._finilize()
    def __del__(self):
        self._finilize()
        
        
        

def init():
    engine = sqlalchemy.create_engine('mysql+mysqldb://cpost_agent:ceskaposta@db:3306/cpost?charset=utf8', pool_recycle=3600)
    inspector = sqlalchemy.inspect(engine)
    
    Session.set_session_maker(bind=engine)
    metadata = sqlalchemy.MetaData()
    # reflection
    # Region
    global Region
    Region = sqlalchemy.Table("region", metadata, autoload=True, autoload_with=engine)
    # City
    global City
    City = sqlalchemy.Table("city", metadata, autoload=True, autoload_with=engine)

def get_regions():
    with Session() as s:
        q = sqlalchemy.sql.select([Region])
        result = s.execute(q)
        while True:
            r = result.fetchone()
            if r is None:
                break
            yield {'id': r.id, 'name': r.name}

def get_cities_by_region(region_id):
    regions = []
    with Session() as s:
        q = sqlalchemy.sql.select([City]).where(City.c.region_id == region_id)
        result = s.execute(q)
        for r in result.fetchall():
            city = {'id': r.id, 'name': r.name}
            city_context = context.CityContext(r.region_id, r.district_id)
            yield (city, city_context)
        
def set_cities(cities, city_context):
    with Session() as s:
        q = sqlalchemy.sql.select([City]).where(
            sqlalchemy.and_(
                City.c.region_id == city_context.region_id,
                City.c.district_id == city_context.district_id
            )
        )
        result = s.execute(q)
        matches = result.fetchall()
        print([match for match in matches])
        exit(0)
        for i,match in enumerate(matches):
            if i > 0:
                print("Regions: multiple results")
                return
            if match is None:
                print("Insert", city["id"], city["name"])
                q = City.insert().values(
                    id=city["id"],
                    name=city["name"],
                    region_id=city_context.region_id,
                    district_id=city_context.district_id)
                s.execute(q)
            else:
                print("Update", match.id, match.name)
                print(dir(match))
                if match.id != city["id"]:
                    match.id = city["id"]
                if match.name != city["name"]:
                    match.name = city["name"]
                s.merge(match)
                
            
        
        #insert_query = City.update().values(
        #    id=city_context.city_id,
        #    name=city_context.city_name,
        #    district_id=city_context.district_id
        #)
        #session.execute(insert_query)
    


def set_regions(regions):
    # fetch online update and sort
    regions = sorted(regions, key=lambda i: i["id"])
    region_ids = set([region["id"] for region in regions])
    print("Set regions:")
    
    with Session() as s:
        # fetch current from db
        q = sqlalchemy.sql.select([Region])
        dbresults = sorted(s.execute(q).fetchall(), key=lambda i: i["id"])
        dbresult_ids = set([dbresult["id"] for dbresult in dbresults])
        
        # insert
        insert_ids,insert_cnt = region_ids-dbresult_ids,0
        for r in [r for r in regions if r["id"] in insert_ids]:
            q = Region.insert().values(**r)
            s.execute(q)
            insert_cnt += 1
        print("|", insert_cnt, "regions inserted.")
        # update
        update_ids,update_cnt = dbresult_ids-insert_ids,0
        for r in [r for r in regions if r["id"] in update_ids]:
            q = Region.update().where(Region.c.id == r["id"]).values(name=r["name"])
            s.execute(q)
            update_cnt += 1
        print("|", update_cnt, "regions updated.")