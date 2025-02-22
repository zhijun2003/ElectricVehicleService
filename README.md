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

# 规划目录结构

ElectricVehicleService/
├── Weixinfront/ # 微信小程序前端
│ ├── images/ # 全局图片资源
│ │ ├── menu/ # 菜单图标
│ │ ├── status/ # 状态图标
│ │ └── common/ # 公共图标
│ ├── pages/
│ │ ├── index/ # 主页
│ │ │ ├── index.js
│ │ │ ├── index.json
│ │ │ ├── index.wxml
│ │ │ └── index.wxss
│ │ └── ...其他页面
│ ├── utils/
│ │ ├── api.js # 封装网络请求
│ │ └── util.js # 通用工具函数
│ ├── app.js # 小程序入口
│ └── app.json # 全局配置
│
└── Djangoback/ # Django后端
├── apps/ # 业务应用目录
│ ├── user/ # 用户模块
│ │ ├── models.py # 用户模型
│ │ ├── serializers.py # DRF序列化器
│ │ ├── viewsets.py # 视图集
│ │ └── urls.py # 子路由
│ ├── charging/ # 充电模块
│ └── repair/ # 维修模块
│ └── statistics/ # 统计模块
├── djangoadmin/ # 项目配置
│ ├── settings/
│ │ ├── base.py # 基础配置
│ │ ├── dev.py # 开发环境
│ │ └── prod.py # 生产环境
│ └── urls.py # 主路由
├── utils/ # 公共工具
│ ├── permissions.py # 权限控制
│ └── middleware.py # 自定义中间件
├── manage.py
└── requirements.txt # 依赖文件