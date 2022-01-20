from fastapi import FastAPI
import uvicorn
import pandas as pd
from sqlalchemy import create_engine
from pydantic import BaseModel

class UserDetails(BaseModel):
    name: str

app = FastAPI()

engine = create_engine('postgresql://postgres:anirudh@db:5432/anirudhdb')

@app.post('/add_user')
def add_user(item:UserDetails):
    try:
        sql = f"""insert into users (name,isactive,recordcreatedtimestamp)
        values('{item.name}','Y',now()::timestamp)"""
        engine.execute(sql)
        return {'status':'success','data':'Adding user succesful'}
    except Exception as error:
        return {'status':'success', 'data':str(error)}

@app.post('/deactivate_user')
def deactivate_user(item: UserDetails):
    try:
        sql = f"""update users set isactive='N',recordmodifiedtimestamp=now()::timestamp
        where name='{item.name}'"""
        engine.execute(sql)
        return {'status':'success','data':'Deactivating user succesful'}
    except Exception as error:
        return {'status':'success', 'data':str(error)}

@app.post('/activate_user')
def activate_user(item:UserDetails):
    try:
        sql = f"""update users set isactive='Y',recordmodifiedtimestamp=now()::timestamp where name='{item.name}'"""
        engine.execute(sql)
        return {'status':'success','data':'Activating user succesful'}
    except Exception as error:
        return {'status':'success', 'data':str(error)}

@app.post('/list_active_users')
def list_active_users():
    try:
        sql = f"""select * from users where isactive='Y'"""
        res = engine.execute(sql)
        df = pd.DataFrame(res.fetchall(), columns=res.keys())
        result = df.to_dict('records')
        return {'status':'success','data':result}
    except Exception as error:
        return {'status':'success', 'data':str(error)}

if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)