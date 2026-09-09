from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import users, articles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple Blog API", version="1.0.0")

app.include_router(users.router)
app.include_router(articles.router)

# 挂载静态文件
app.mount("/", StaticFiles(directory="static", html=True), name="static")