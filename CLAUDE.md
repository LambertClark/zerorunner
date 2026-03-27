# CLAUDE.md — zerorunner 项目根目录

## 行为规范

- 永远以简体中文回复

## 项目简介

zerorunner 是一个自动化测试平台，支持 API 自动化、UI 自动化（Selenium）、PC 桌面自动化，以及代码覆盖率统计等能力。

## 顶层目录结构

```
zerorunner/
├── backend/          # Python 后端（FastAPI）
├── frontend/         # 前端（Vue）
├── static/           # 静态资源
├── docker-compose*.yml   # 各场景 Docker Compose 配置
├── zero-docker-file/ # Dockerfile 相关
└── zero-nginx-config/# Nginx 配置
```

## 启动方式

### 本地开发
```bash
# 后端
cd backend
pip install -r requirements
uvicorn main:app --host 127.0.0.1 --port 9101 --reload

# 或使用 gunicorn（生产）
gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8101
```

### Docker
```bash
# 启动基础依赖（MySQL + Redis）
docker-compose -f docker-compose-db-redis.yml up -d

# 启动完整应用
docker-compose up -d
```

## 环境变量

后端依赖 `backend/.env` 文件，参考 `backend/.env.example`：

| 变量名 | 说明 |
|---|---|
| `MYSQL_DATABASE_URI` | MySQL 异步连接串 |
| `REDIS_URI` | Redis 连接串 |
| `CELERY_BROKER_URL` | Celery Broker（一般同 Redis）|
| `CELERY_BEAT_DB_URL` | Celery Beat 数据库 |
| `FILE_BASE_URL` | PC图片素材对外访问 Base URL |

## 技术栈

- **后端**：Python 3.10+、FastAPI、SQLAlchemy 2.x（异步）、Pydantic v1、Celery 5、aiohttp、aiofiles
- **数据库**：MySQL（aiomysql 驱动）
- **缓存/队列**：Redis
- **前端**：Vue 3
