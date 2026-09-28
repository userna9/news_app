
import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user

from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security

#根据用户名查数据库
async def get_user_by_username(db:AsyncSession,username:str):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalars().one_or_none()

#创建用户
async def create_user(db:AsyncSession,user_data:UserRequest):
    #先密码加密处理再新增用户
    hashed_password=security.get_hash_password(user_data.password)
    user=User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)#刷新一下数据库
    return user


#生成Token
async def create_token(db:AsyncSession,user_id:int):
        #生成token，设置过期时间->查询当前用户有没有token->有，更新/无，添加
    token=str(uuid.uuid4())
    expires_at= datetime.now() + timedelta(days=7)
    query=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at

    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token


async  def authenticate_user(db:AsyncSession,username:str,password:str):
    user=await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None
    return user

#根据token有效性
async def get_user_by_token(db:AsyncSession,token:str):
    query=select(UserToken).where(UserToken.token==token)
    result=await db.execute(query)
    db_token= result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now(): #无token或者过期
        return None

    query=select(User).where(User.id==db_token.user_id)
    result=await db.execute(query)
    return result.scalar_one_or_none()


#更新用户信息
async def update_user(db:AsyncSession,user_name:str,user_data:UserRequest):
    #没有设置值的不更新
    query=update(User).where(User.username==user_name).values(**user_data.model_dump(exclude_unset=True,exclude_none=True))
    result=await db.execute(query)
    await db.commit()

    if result.rowcount==0:
        raise HTTPException(status_code=404,detail="用户不存在")

    updated_user=await get_user_by_username(db,user_name)
    return updated_user

async def change_password(db:AsyncSession,user:User,old_password:str,new_password:str):

    #验证旧密码->输入新密码->加密
    if not security.verify_password(old_password,user.password):
        return False

    hashed_new_pwd=security.get_hash_password(new_password)
    user.password=hashed_new_pwd
    db.add(user)#由sqlalchemy真正接管确保commit能真正提交，避免session过期或关闭导致不能提交的问题
    await db.commit()
    await db.refresh(user)
    return True