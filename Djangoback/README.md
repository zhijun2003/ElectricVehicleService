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
├── Weixinfront/                  # 微信小程序前端
│   ├── images/                   # 全局图片资源
│   │   ├── menu/                 # 菜单图标
│   │   ├── status/               # 状态图标
│   │   └── common/               # 公共图标
│   ├── pages/
│   │   ├── index/                # 主页
│   │   │   ├── index.js
│   │   │   ├── index.json
│   │   │   ├── index.wxml
│   │   │   └── index.wxss
│   │   └── ...其他页面
│   ├── utils/
│   │   ├── api.js               # 封装网络请求
│   │   └── util.js              # 通用工具函数
│   ├── app.js                   # 小程序入口
│   └── app.json                 # 全局配置
│
└── Djangoback/                  # Django后端
    ├── charging_station/        # 充电桩模块
    │   ├── models.py            # 数据模型
    │   ├── views.py             # 视图逻辑
    │   ├── serializers.py       # DRF序列化器
    │   ├── urls.py              # 子路由
    │   └── tests/               # 单元测试
    ├── user_management/         # 用户模块
    │   ├── models.py            # 用户扩展模型
    │   ├── auth.py              # 认证相关
    │   └── permissions.py       # 权限控制
    ├── statistics/              # 统计模块
    │   ├── analyzers/           # 数据分析器
    │   └── report_generators/   # 报表生成
    ├── djangoadmin/             # 主项目配置
    │   ├── settings/
    │   │   ├── base.py          # 基础配置
    │   │   ├── dev.py           # 开发环境
    │   │   └── prod.py          # 生产环境
    │   ├── urls.py              # 主路由
    │   └── wsgi.py
    ├── middleware/              # 自定义中间件
    │   ├── jwt_auth.py          # JWT认证
    │   └── request_logger.py    # 请求日志
    ├── scripts/                 # 部署脚本
    │   ├── deploy.sh
    │   └── migrate_db.sh
    ├── requirements.txt         # 依赖清单
    └── manage.py