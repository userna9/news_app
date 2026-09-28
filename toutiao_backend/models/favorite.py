from datetime import datetime
from sqlalchemy import UniqueConstraint, Index, ForeignKey, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

from models.news import News
from models.users import User

class Base(DeclarativeBase):
    pass

class Favorite(Base):
    __tablename__ = "favorite"
    __table_args__=(
        UniqueConstraint('user_id','news_id',name='user_news_unique'),#UniqueConstraint唯一索引,一条新闻只能被收藏一次
        Index('fk_favorite_user_id','user_id'),
        Index('fk_favorite_news_idx','news_id'),
    )

    id : Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,nullable=False,comment="收藏ID")
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey(User.id),nullable=False,comment="用户ID")
    news_id:Mapped[int]=mapped_column(Integer,ForeignKey(News.id),nullable=False,comment="新闻ID")
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow(),nullable=False,comment="收藏时间")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id},created_at={self.created_at})>"