# CLAUDE.md — zerorunner backend

## 行为规范

- 永远以简体中文回复

## 后端目录结构

```
backend/
├── main.py                        # FastAPI 应用入口
├── config.py                      # 全局配置（Pydantic BaseSettings，读取 .env）
├── autotest/                      # 主业务模块
│   ├── apis/                      # 路由控制器（按业务子目录组织）
│   │   ├── api_router.py          # 统一路由注册入口
│   │   ├── pc_autotest/           # PC 自动化控制器
│   │   ├── api/                   # API 自动化控制器
│   │   ├── ui/                    # UI 自动化控制器
│   │   └── system/                # 系统管理控制器
│   ├── models/                    # SQLAlchemy ORM 模型（含查询方法）
│   │   ├── base.py                # Base 基类（含 create_or_update、delete、pagination 等）
│   │   ├── pc_testcase_models.py  # PC用例
│   │   ├── pc_device_models.py    # PC执行设备
│   │   ├── pc_report_models.py    # PC报告（含动态分表）
│   │   ├── pc_plan_models.py      # PC测试计划
│   │   ├── pc_plan_report_models.py
│   │   ├── pc_picture_models.py   # PC素材 + 素材绑定
│   │   ├── api_models.py          # API 自动化模型
│   │   ├── ui_models.py           # UI 自动化模型
│   │   └── system_models.py       # 用户、文件等系统模型
│   ├── schemas/                   # Pydantic 数据校验模型
│   │   ├── base.py                # BaseSchema（exclude_none=True）
│   │   ├── step_data.py           # TStepData / TStepRequest（含 PC 步骤类型）
│   │   └── pc_autotest/           # PC 专属 Schema
│   ├── services/                  # 业务逻辑层
│   │   └── pc_autotest/           # PC 专属 Service
│   ├── db/                        # 数据库会话
│   ├── exceptions/                # 自定义异常
│   ├── init/                      # 应用初始化（路由注册、中间件、CORS 等）
│   └── utils/                     # 工具函数
│       └── response/
│           └── http_response.py   # 统一响应封装 partner_success()
├── zerorunner/                    # 核心测试执行引擎
│   ├── models/
│   │   ├── base.py                # 基础类型（MethodEnum、Url 等）
│   │   └── step_model.py          # 步骤模型（TStep、TStepRequest 判别联合）
│   └── steps/                     # 各类步骤执行器
├── celery_worker/                 # Celery 异步任务
│   ├── worker.py                  # Celery 应用实例
│   ├── base.py                    # run_async 工具
│   └── tasks/
│       ├── pc_picture.py          # PC素材定时清理任务
│       ├── ui_case.py
│       └── test_case.py
└── db_script/                     # SQL 建表脚本
    └── pc_picture_binding_backfill.sql
```

## 核心开发约定

### 分层职责
- **models/**：ORM 表定义 + 查询方法（`get_list`、`get_xxx_by_id` 等），不含业务逻辑
- **schemas/**：请求/响应的 Pydantic 校验模型，继承 `BaseSchema`
- **services/**：业务逻辑，调用 models，不直接操作 HTTP
- **apis/**：控制器，只做参数接收和调用 service，返回 `partner_success(data)`

### Model 基类（`autotest/models/base.py`）
所有表模型继承 `Base`，自带：
- 公共字段：`id`、`creation_date`、`created_by`、`updation_date`、`updated_by`、`enabled_flag`、`trace_id`
- 逻辑删除：`delete()` 默认设置 `enabled_flag=0`
- `create_or_update(params: dict)`：有 id 则 UPDATE，无 id 则 INSERT
- `pagination(stmt)`：统一分页，从请求体中自动读取 `page` / `pageSize`
- `get_result(stmt, first=False)`：查询结果转 dict

### Schema 基类（`autotest/schemas/base.py`）
- 继承 `BaseSchema`，`dict()` 默认 `exclude_none=True`
- 空字符串 `""` 会被 validator 转为 `None`

### 步骤模型（`zerorunner/models/step_model.py`）
- `TStep.request` 通过 `discriminator="request_type_"` 做判别联合
- 新增步骤类型必须在 `TStepRequest` Union 中注册，且 `Literal[request_type_]` 值不能重复
- PC 步骤类型继承 `TPcBaseRequest`，共有 18 种（mouse_*、keyboard_*、flow_*、pip_*）

### 响应格式
统一使用 `partner_success(data)` 返回，格式：
```json
{"code": 0, "msg": "success", "data": {...}, "success": true, "trace_id": "..."}
```

### PC 自动化模块路由前缀
| 路由前缀 | 控制器 |
|---|---|
| `/api/pc/devices` | PC执行设备 |
| `/api/pc/testcase` | PC用例 |
| `/api/pc/report` | PC执行报告（含 Agent 回传端点 `/saveReportStepDetail`）|
| `/api/pc/plan` | PC测试计划 |
| `/api/pc/planReport` | PC计划报告 |
| `/api/pc/picture` | PC素材管理 |
| `/api/pc/fm` | PC图片文件上传/下载 |

### PC Agent 协议
平台调用外部 PC Agent（不在本仓库内）：
- 健康检查：`GET http://{ip}:{port}/api/v1/ping`
- 执行用例：`POST http://{ip}:{port}/api/v1/pc_ui_case/execute`
- Agent 回传步骤结果到：`POST /api/pc/report/saveReportStepDetail`

### PC 素材绑定规则
- 保存用例时：先 `PcPictureBinding.clear_case_bindings(case_id)`，再 `bind_case_by_image_urls(urls, case_id)`
- 删除用例时：同步清理绑定
- 需扫描的图片字段：`image`、`dragImage`、`referenceImage`、`targetImage`、`trackImage`、`parentImage`

### 报告分表
PC 报告步骤明细按 `report_id % 10` 路由到 `pc_report_detail_0~9`，通过 `get_pc_report_detail_model(report_id)` 获取对应 Model 类。

## 新增模块的标准步骤

1. `schemas/<module>/` — 定义查询/入参/ID schema
2. `models/<module>_models.py` — 定义 ORM 模型 + 查询方法
3. `services/<module>/<feature>_service.py` — 业务逻辑
4. `apis/<module>/<feature>_controller.py` — 路由控制器
5. `apis/api_router.py` — 注册路由

## 注意事项

- Pydantic 版本为 **v1**（`BaseModel`、`validator`、`root_validator`、`Field`），不要使用 v2 语法
- SQLAlchemy 版本为 **2.x**，使用 `mapped_column`，查询使用 `select()`
- 异步框架：所有 DB 操作均为 `async/await`，session 通过 `g.zero_db_session` 或 `provide_async_session` 获取
- 不要在 model 层引入 service 层，避免循环导入
