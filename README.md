# A Diary 后端项目

[![GitHub license](https://img.shields.io/github/license/a-diary/backend.svg)](https://github.com/a-diary/backend/blob/master/LICENSE)
![Language](https://img.shields.io/badge/language-python-3572A5.svg)

这是 A Diary 项目的后端仓库，使用 Flask 编写。

## 运行

- 在根目录创建密钥文件：`python3 -c "from utils import random_string; print(random_string(64, True))" > secret.key`
- 安装依赖：`pip3 install -r requirements.txt`
- 使用环境变量配置数据库（推荐使用 postgresql，其余数据库未经过测试）：`export MODE=production` `export DB_TYPE=postgresql` `export DB_HOST=localhost:5432` `export DB_USER=postgres` `export DB_PASSWORD=postgres` `export DB_DB=adiary`（如果你想要使用 SQLite 作为数据库，可指定 `export MODE=development` 和 `export DEBUG=FALSE`）
- 创建或更新数据库迁移文件：`flask db init` `flask db migrate` 和 `flask db upgrade`
- 运行开发服务器：`python3 app.py`
