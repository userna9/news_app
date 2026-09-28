
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news
from crud import news_cache
router=APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(db:AsyncSession=Depends(get_db), skip: int = 0, limit: int = 100):
    #先获取数据库里面的新闻分类数据 -> 先定义模型类 -> 封装查询数据的方法
    categories=await news_cache.get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"获取新闻分类成功",
        "data":categories
    }

#处理分页规则—>查询新闻列表->计算总量——>计算是否还有更多
@router.get("/list")
async def get_news_list(
        category_id:int =Query(...,alias="categoryId"),#与前端约定的参数是驼峰式命名，而这里用的小写，所以通过alias设置别名
        page:int=1,
        page_size:int =Query(10,le=100,alias="pageSize"),
        db:AsyncSession=Depends(get_db)
):
    offset=(page-1)*page_size
    news_list=await news.get_news_list(db,category_id,offset,page_size)
    total=await news.get_news_count(db,category_id)
    has_more=(offset+len(news_list)) < total
    return{
            "code":200,
            "message":"获取新闻列表成功",
            "data":{
                "list":news_list,
                "total":total,
                "hasMore":has_more
            }
        }

#获取新闻详情 +浏览量+1  +相关新闻
@router.get("/detail")
async def get_news_detail(news_id:int=Query(...,alias="id"),db:AsyncSession=Depends(get_db)):
    news_detail= await news.get_news_detail(db,news_id)
    #要查的新闻id不存在时报错
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")

    views_res=await news.increase_news_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404,detail="新闻不存在")

    related_news = await news.get_related_news(db,news_detail.category_id,news_detail.id)
    return{
            "code": 200,
            "message": "success",
            "data": {
                "id": news_detail.id,
                "title": news_detail.title,
                "content": news_detail.content,
                "image": news_detail.image,
                "author": news_detail.author,
                "publishTime": news_detail.publish_time,
                "categoryId": news_detail.category_id,
                "views": news_detail.views,
                "relatedNews": related_news
            }
    }
