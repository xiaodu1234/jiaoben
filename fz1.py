import asyncio
import time
import hashlib
import httpx
import logging
from fastapi import FastAPI
from pydantic import BaseModel

accessKey = '5ffb8e1291d9e89e69c15d960062b399'
secretKey = 'af9374aa576277d6ff7aef08dd4bd2da'
RobotId   = 228146


async def api(CMD):
    #http params
    params = {
        'version': '1.0',
        'access_key': accessKey,
        'method': 'CommandRobot',
        'args': f'[{RobotId},"{CMD}"]',
        'nonce': int(time.time() * 1000),
        }

    params['sign'] = hashlib.md5(f"{params['version']}|{params['method']}|{params['args']}|{params['nonce']}|{secretKey}".encode('utf-8')).hexdigest()

    async with httpx.AsyncClient() as client:
        for i in range(5):
            try:
                response = await client.get('https://www.fmz.com/api/v1',params=params)
                assert response.status_code == 200
                break
            except:
                print(f'ERR!  connect "www.fmz.com" filed , again times {i+1}!')
                await asyncio.sleep(2)
                continue
        return(response.json())


class Item(BaseModel):
    apikey: str
    exchange: str
    symbol:str
    side:str
    amount: int

webhook = FastAPI() #new webhook server

@webhook.post("/tv/") #set post url root
async def create_item(item: Item): #get webhook item
    print(item)
    logging.debug('debug 信息')
    if (item.apikey=='FMZ'):
        item_dict = item.dict()
        ret=await api(item_dict)
        if(ret['code']==0 and ret['data']['result']==True ):
            print ({'return':'ok'})
        else:
            print({'return':'error'})
            print(ret)
