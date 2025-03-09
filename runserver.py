import os
import subprocess
import sys

DJANGO_DIR = r"D:\Workspace\ElectricVehicleService\Djangoback"


def run_command(cmd, cwd=None):
    """执行命令行指令（添加路径检查）"""
    try:
        # 添加虚拟环境路径检查
        venv_path = os.path.join(DJANGO_DIR, 'venv/Scripts/python.exe')
        if os.path.exists(venv_path):
            cmd = cmd.replace("python", f'"{venv_path}"')  # 使用绝对路径

        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        os.chdir(DJANGO_DIR)

        # 新增依赖检查
        if not os.path.exists("manage.py"):
            raise FileNotFoundError("Django项目根目录错误")

        # 添加数据库迁移
        run_command("python manage.py makemigrations")
        run_command("python manage.py migrate")

        print("正在启动开发服务器...")
        run_command("python manage.py runserver 0.0.0.0:8000")

    except Exception as e:
        print(f"启动失败: {str(e)}")
        sys.exit(1)