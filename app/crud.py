from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash
from typing import List, Optional

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_article(db: Session, article: schemas.ArticleCreate, author_id: int):
    tags = []
    for tag_name in article.tags:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)
    db_article = models.Article(
        title=article.title,
        content=article.content,
        author_id=author_id,
        tags=tags
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(models.Article)
    total = query.count()
    articles = query.order_by(models.Article.id.desc()).offset((page-1)*page_size).limit(page_size).all()
    return articles, total

def update_article(db: Session, article_id: int, article: schemas.ArticleUpdate):
    db_article = get_article(db, article_id)
    if not db_article:
        return None
    update_data = article.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == 'tags':
            # 处理标签
            tags = []
            for tag_name in value:
                tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
                if not tag:
                    tag = models.Tag(name=tag_name)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                tags.append(tag)
            db_article.tags = tags
        else:
            setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int):
    db_article = get_article(db, article_id)
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article