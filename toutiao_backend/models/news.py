from typing import Optional

from sqlalchemy import DateTime, Integer, String, Index, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    # 根据数据库中的表可以知道，created_at和updated_at这个是news和news_category通用的，放进Base中就可以了
    # 自己私有的放进自己的模型类里面就行了

    created_at:Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )

    updated_at:Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

class Category(Base):
    __tablename__ = "news_category"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="分类id")
    name:Mapped[str]=mapped_column(String(50),unique=True,nullable=False,comment="分类名称")
    sort_order:Mapped[int]=mapped_column(Integer,default=0,nullable=False,comment="排序")

    def __repr__(self):
        return f"<Category(id={self.id},name={self.name},sort_order={self.sort_order})>"


class News(Base):
    __tablename__ = "news"
    #创建索引，提升查询速度
    __table_args__ = (
        Index("fk_news_category_idx","category_id"),#按分类id查询新闻是高频操作，所以设置索引，增加速度
        Index("idx_publish_time","publish_time")#按照发布时间排序，而不是全表排序，节省时间
    )
    id:Mapped[int] = mapped_column(Integer,primary_key=True,)
    title:Mapped[str]=mapped_column(String(50),nullable=False,comment="新闻标题")
    description:Mapped[Optional[str]]=mapped_column(String(255),nullable=False,comment="新闻简述")
    content:Mapped[str]=mapped_column(Text,nullable=False,comment="新闻内容")
    image:Mapped[Optional[str]]=mapped_column(String(255),comment="封面图片")
    author:Mapped[Optional[str]]=mapped_column(String(50),comment="作者")
    category_id:Mapped[int]=mapped_column(Integer,ForeignKey("news_category.id"))
    views:Mapped[int]=mapped_column(Integer,default=0,nullable=False,comment="浏览量")
    publish_time:Mapped[datetime]=mapped_column(DateTime,default=datetime.now,comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id},title='{self.title}',views={self.views})>'"
