django服务器启动
# 基本启动（默认端口8000）
python run.py

# 指定端口和IP
python run.py --ip 0.0.0.0 --port 8080

# 带自动迁移的启动
python run.py --migrate

# 带调试模式的启动（需要安装额外包）
DEBUG=1 python run.py

运行前准备

# 在Djangoback目录执行
pip install -r requirements.txt
# 确认已安装的关键包：
✔ django~5.2
✔ mysqlclient==2.2.0
✔ django-cors-headers==4.3.0

# 登录MySQL创建数据库
mysql -u root -p
> CREATE DATABASE ev_charging;
> CREATE USER 'ev_user'@'localhost' IDENTIFIED BY 'ev_password';
> GRANT ALL PRIVILEGES ON ev_charging.* TO 'ev_user'@'localhost';

