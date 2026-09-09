markdown
# 简易个人博客后端管理系统

基于 **FastAPI + SQLite + JWT** 的轻量级博客后端，提供用户注册登录、文章增删改查、分页查询、标签分类功能，并附带 **pytest 接口自动化测试**，覆盖常见正常、异常、越权、参数校验场景。前端采用原生 HTML/CSS/JS，实现基本交互。

## ✨ 功能特性

- 用户注册、登录（JWT 鉴权）
- 文章发布、编辑、删除、详情查看、分页列表
- 标签分类（文章可关联多个标签）
- 简单前端页面（登录、列表、新建/编辑文章）
- pytest + requests 接口自动化测试，覆盖：
  - 正常注册 / 登录
  - 密码错误 / 用户不存在
  - 未携带 Token 访问文章接口
  - 非法参数（缺少标题）
  - 越权操作（修改 / 删除他人文章）
  - 分页查询

## 🛠️ 技术栈

| 层次 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 数据库 | SQLite + SQLAlchemy ORM |
| 认证 | JWT（python-jose + passlib） |
| 前端 | HTML + CSS + 原生 JavaScript |
| 测试 | pytest + requests + httpx |

## 🚀 快速开始

### 环境要求

- Python 3.9+
- pip

```

### 安装依赖
```bash
git clone https://github.com/fuan-ukane/simple-blog-backend.git
cd simple-blog-backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 启动服务

```
uvicorn app.main:app --reload
```

访问地址：

- 前端首页：[http://localhost:8000](http://localhost:8000)
- API 文档：[http://localhost:8000/docs](http://localhost:8000/docs)

### 运行测试

```
pytest
```

📁 **项目结构**

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── database.py          # 数据库连接与初始化
│   ├── models.py            # SQLAlchemy 模型
│   ├── schemas.py           # Pydantic 请求/响应模型
│   ├── crud.py              # 数据库操作函数
│   ├── auth.py              # JWT 鉴权、密码哈希
│   └── routers/
│       ├── users.py         # 注册、登录路由
│       └── articles.py      # 文章 CRUD 路由
├── static/
│   ├── login.html
│   ├── index.html
│   ├── article.html
│   └── main.js
├── tests/
│   ├── conftest.py          # 测试夹具、内存数据库隔离
│   ├── test_auth.py         # 用户接口测试
│   └── test_articles.py     # 文章接口测试
├── requirements.txt
└── README.md
```

📝 **API 概览**

表格

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| POST | /api/register | 用户注册 | 否 |
| POST | /api/token | 登录获取 JWT | 否 |
| GET | /api/articles | 分页文章列表 | 否 |
| GET | /api/articles/{id} | 文章详情 | 否 |
| POST | /api/articles | 创建文章 | 是 |
| PUT | /api/articles/{id} | 更新文章 | 是（仅作者） |
| DELETE | /api/articles/{id} | 删除文章 | 是（仅作者） |

🧪 **测试覆盖场景**

- 正常流程：注册成功、登录成功、创建文章成功、分页查询正确
- 异常参数：缺少标题、重复注册、密码错误、用户不存在
- 鉴权校验：未携带 Token 返回 401
- 越权控制：非作者修改 / 删除文章返回 403
- 数据隔离：使用内存 SQLite 并为每个测试重建表，保证用例独立

📄 **许可证**
仅供学习交流使用。

👤 **作者**
GitHub: fuan-ukane
