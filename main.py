from fastapi import FastAPI, HTTPException, UploadFile
import pandas as pd 
import uvicorn
from pydantic import ValidationError
from models import Terrorist
from db import get_coll, insert_to_db

def read_csv(path):
    df = pd.read_csv(path)
    return df 

def sort_by_danger_rate(df: pd.DataFrame):
    df = df.sort_values(by='danger_rate', ascending=False)
    return df

def get_first_5(df: pd.DataFrame):
    return df.head(5)

def convert_df_to_dict(df: pd.DataFrame):
    return df.to_dict()


def get_list_5_danger_terrs(danger_terrs: dict):
    lst_terrs = []
    for i in range(len(danger_terrs["name"])):
        terr = Terrorist(name=danger_terrs["name"][i], location=danger_terrs["location"][i], danger_rate=danger_terrs["danger_rate"][i]).model_dump()
        lst_terrs.append(terr)
    return lst_terrs

def csv_to_list_of_danger_terrorists(csv):
    df = read_csv(csv)
    sorted_df = sort_by_danger_rate(df)
    five_d_terr = get_first_5(sorted_df)
    dict_terr = convert_df_to_dict(five_d_terr)
    lst = get_list_5_danger_terrs(dict_terr)
    return {"count": len(lst),"top": lst}


app = FastAPI()

@app.post('/top-threats')
def post_danger_terrorists(file: UploadFile): 
    try: 
        danger_list = csv_to_list_of_danger_terrorists(file.file)
        coll = get_coll()
        insert_to_db(coll, danger_list["top"])
        return danger_list
    except FileNotFoundError: 
        raise HTTPException(status_code=400, detail="No file provided")
    except TypeError: 
        raise HTTPException(status_code=400, detail="Invalid CSV file")
    ##
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=503, detail="Database unavailable")

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)

# r = csv_to_list_of_danger_terrorists('terrorists_data.csv')
# print( r)

# df = read_csv('terrorists_data.csv')
# df = sort_by_danger_rate(df)
# df = get_first_5(df)
# df = convert_df_to_dict(df)
# d = get_important_details(df)
# d = get_list_5_danger_terrs(d)
# print(d)
