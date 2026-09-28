import json
from typing import Any

import redis.asyncio as redis


REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0

redis_client=redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,#Redis数据库编号0-15
    decode_responses=True#是否将字节数据解码为字符串
)

async def get_cache(key:str):
    try:#有可能成功有可能失败，所以使用try，except
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None

async def get_json_cache(key:str):
    try:
        data=await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取json格式缓存失败{e}")
        return None

#设置缓存setex(key,expire,value)
async def set_cache(key:str, value:Any,expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            value=json.dumps(value,ensure_ascii=False) #中文正常保存
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f"获取JSON缓存失败:{e}")
        return None



