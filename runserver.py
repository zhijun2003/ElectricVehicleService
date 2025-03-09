@echo off
REM 进入Django后端目录
cd D:\Workspace\ElectricVehicleService\Djangoback

REM 激活虚拟环境（如有）
REM call venv\Scripts\activate

REM 安装依赖
REM pip install -r requirements.txt

REM 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

REM 启动开发服务器
python manage.py runserver 0.0.0.0:8000
