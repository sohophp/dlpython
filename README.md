# your downloader

youtube video downloador

- language: python
- framework: django

```bash

# 安装 mod_wsgi
$ sudo apt install apache2-dev
# https://modwsgi.readthedocs.io/en/master/user-guides/quick-installation-guide.html#cleaning-up-after-build
# LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

$ sudo apt install python3-pip
# 安装 venv
$ python3 -m pip install venv
$ python3 -m venv /usr/local/lib/venv
# 启用虚拟环境
$ source /usr/local/lib/venv/bin/activate
# 退出虚拟环境
$ deactivate

# 导出依赖包
# pip freeze >requirements.txt
# 安装依赖包
$ pip install -r requirements.txt

# 复制 static
$ python manage.py collectstatic
```