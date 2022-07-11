# A Diary 后端项目

这是 A Diary 项目的后端仓库，使用 Flask 编写。

## 运行

-   在根目录创建密钥文件 `secret.key`
-   安装依赖：`pip3 install -r requirements.txt`
-   创建或更新数据库文件：`alembic revision --autogenerate -m "First run"` 和 `alembic upgrade head`
-   运行：`python3 app.py`
