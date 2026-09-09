from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db
from app.auth import get_current_user
from app.models import User

router = APIRouter()

@router.post("/api/articles", response_model=schemas.ArticleOut, status_code=201)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_article(db, article, author_id=current_user.id)

@router.get("/api/articles", response_model=schemas.ArticleList)
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    articles, total = crud.get_articles(db, page, page_size)
    # 转换 tags 为字符串列表
    items = []
    for art in articles:
        art_dict = schemas.ArticleOut.from_orm(art).dict()
        art_dict['tags'] = [tag.name for tag in art.tags]
        items.append(art_dict)
    return {"items": items, "total": total, "page": page, "page_size": page_size}

@router.get("/api/articles/{article_id}", response_model=schemas.ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    art = crud.get_article(db, article_id)
    if not art:
        raise HTTPException(status_code=404, detail="没有找到文章")
    art_dict = schemas.ArticleOut.from_orm(art).dict()
    art_dict['tags'] = [tag.name for tag in art.tags]
    return art_dict

@router.put("/api/articles/{article_id}", response_model=schemas.ArticleOut)
def update_article(
    article_id: int,
    article: schemas.ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    art = crud.get_article(db, article_id)
    if not art:
        raise HTTPException(status_code=404, detail="没有找到文章")
    if art.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="您没有权限更新这篇文章")
    updated_art = crud.update_article(db, article_id, article)
    art_dict = schemas.ArticleOut.from_orm(updated_art).dict()
    art_dict['tags'] = [tag.name for tag in updated_art.tags]
    return art_dict

@router.delete("/api/articles/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    art = crud.get_article(db, article_id)
    if not art:
        raise HTTPException(status_code=404, detail="没有找到文章")
    if art.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="您没有权限更新这篇文章")
    crud.delete_article(db, article_id)
    return None