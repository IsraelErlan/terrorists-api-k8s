from pymongo import MongoClient
import os 

def get_coll():
    try: 
        conn = MongoClient(host = os.getenv('MONGO_HOST', 'localhost'),
                            port = os.getenv('MONGO_PORT', 27017),
                            )
        return conn["top_threat"]
    except Exception as e:
        raise e
    

def insert_to_db(coll, danger_terr:list):
    try: 
        coll.insert_many(danger_terr)
        coll.commit()
        coll.close()
    except Exception as e: 
        raise e
