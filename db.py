from pymongo import MongoClient
import os 


MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_USERNAME = os.getenv('MONGO_USERNAME', 'admin')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'secretpass')
MONGO_DB = os.getenv('MONGO_DB', 'threat_db')
MONGO_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE', 'admin')



def get_coll():
    try:
      conn = MongoClient(MONGO_HOST, MONGO_PORT)
      return conn
    except Exception as e:
        return None
    

def insert_to_db(conn, danger_terr:list):
    try: 
        
        db = conn["terrorists"]
        coll = db["top_threats"]
        coll.insert_many(danger_terr)
        
    except Exception as e: 
        raise e
