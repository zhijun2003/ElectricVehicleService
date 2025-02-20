# Djangoback/run.py
import os
import sys
import argparse
from django.core.management import execute_from_command_line

def main():
    # 设置Django环境变量
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoadmin.settings")
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Run Django server')
    parser.add_argument('--port', type=int, default=8000, help='Port number')
    parser.add_argument('--ip', default='127.0.0.1', help='IP address')
    parser.add_argument('--migrate', action='store_true', help='Auto run migrations')
    args = parser.parse_args()

    # 自动执行数据库迁移
    if args.migrate:
        print("\n\033[32mApplying database migrations...\033[0m")
        execute_from_command_line([sys.argv[0], 'makemigrations'])
        execute_from_command_line([sys.argv[0], 'migrate'])

    # 启动开发服务器
    print(f"\n\033[34mStarting Django server at http://{args.ip}:{args.port}/\033[0m")
    execute_from_command_line([
        sys.argv[0], 
        'runserver', 
        f'{args.ip}:{args.port}',
        '--noreload'  # 可选关闭自动重载
    ])

if __name__ == '__main__':
    main()
