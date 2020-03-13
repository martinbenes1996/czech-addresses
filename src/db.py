
import sqlalchemy
import sqlalchemy.orm.session as session

Session = None
Region,City = None,None

def init():
    engine = sqlalchemy.create_engine('mysql+mysqldb://cpost_agent:ceskaposta@db:3306/cpost?charset=utf8', pool_recycle=3600)
    inspector = sqlalchemy.inspect(engine)
    
    #print(inspector.get_schema_names())
    #print(inspector.get_table_names(schema="cpost"))
    #print(inspector.get_columns("city", schema="cpost"))
    
    global Session
    Session = session.sessionmaker(bind=engine)
    metadata = sqlalchemy.MetaData()
    # reflection
    # Region
    global Region
    Region = sqlalchemy.Table("region", metadata, autoload=True, autoload_with=engine)
    # City
    global City
    City = sqlalchemy.Table("city", metadata, autoload=True, autoload_with=engine)
#init()

def get_cities_by_region(region_id):
    global Session
    global City, Region
    
    session = Session()
    q = session.execute(sqlalchemy.sql.select([City]).join(Region).join(City.c["region_pk"] == Region.c["pk"]).select().where(region_id=region_id))
    results = q.fetchall()
    print(results)
    
    cities = [{
        'id': r.id,
        'name': r.name,
        'district_id': r.district_id,
        'district': r.district
    } for r in fetchall]
    session.close()
    
    return cities
    
def set_cities(city_context):
    global Session
    global City
    
    # ----- session -----
    session = Session()
    
    # insert/update cities
    q = session.execute(sqlalchemy.sql.select([City]))
    result = q.fetchall()
    print(result)
    for city in city_context:
        pass
        
        
        #insert_query = City.update().values(
        #    id=city_context.city_id,
        #    name=city_context.city_name,
        #    district_id=city_context.district_id
        #)
        #session.execute(insert_query)
    
    try:
        # commit changes
        session.commit()
    except Exception as e:
        # ERROR: rollback
        session.rollback()
        raise Exception("set_cities() failed: \"" + e.message + "\"")
    finally:
        # close
        session.close()
    # -------------------
    

def get_regions():
    global Session
    global Region
    
    session = Session()
    regions = [{'id': r.id, 'name': r.name} for r in session.query(Region).all()]
    session.close()

    return regions

def set_regions(regions):
    global Session
    global Region
    # ----- session -----
    session = Session()
    
    # remove all regions
    session.execute(Region.delete())
    # insert new regions
    for region in regions:
        insert_query = Region.insert().values(id=region.region_id,name=region.region_name)
        session.execute(insert_query)
    
    try:
        # commit changes
        session.commit()
    except Exception as e:
        # ERROR: rollback
        session.rollback()
        raise Exception("setRegions() failed: \"" + e.message + "\"")
    finally:
        # close
        session.close()
    # -------------------

    