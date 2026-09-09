from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.auth import get_current_user
from app.models import User

router = APIRouter()

def _article_to_dict(article):
    """将 ORM 文章对象转换为符合 ArticleOut 的字典"""
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "author": {
            "id": article.author.id,
            "username": article.author.username,
        },
        "tags": [tag.name for tag in article.tags],
        "created_at": article.created_at,
        "updated_at": article.updated_at,
    }

@router.post("/api/articles", response_model=schemas.ArticleOut, status_code=201)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_article = crud.create_article(db, article, author_id=current_user.id)
    return _article_to_dict(db_article)

@router.get("/api/articles", response_model=schemas.ArticleList)
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    articles, total = crud.get_articles(db, page, page_size)
    items = [_article_to_dict(art) for art in articles]
    return {"items": items, "total": total, "page": page, "page_size": page_size}

@router.get("/api/articles/{article_id}", response_model=schemas.ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return _article_to_dict(article)

@router.put("/api/articles/{article_id}", response_model=schemas.ArticleOut)
def update_article(
    article_id: int,
    article: schemas.ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = crud.get_article(db, article_id)
    if not existing:
        raise HTTPException(status_code=404, detail="文章不存在")
    if existing.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改该文章")
    updated_article = crud.update_article(db, article_id, article)
    return _article_to_dict(updated_article)

@router.delete("/api/articles/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = crud.get_article(db, article_id)
    if not existing:
        raise HTTPException(status_code=404, detail="文章不存在")
    if existing.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限删除该文章")
    crud.delete_article(db, article_id)
    return None