# RCLTool

backend

$ python manage.py makemigrations

$ python manage.py migrate

该 makemigrations 命令查找所有可用的模型，为任意一个在数据库中不存在对应数据表的模型创建迁移脚本文件。migrate 命令则运行这些迁移来自动创建数据库表

python manage.py runserver

frontend

npm run dev