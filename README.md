# your downloader

youtube video downloador

- language: python
- framework: django



### 安装虚拟环境
```bash
# 如果没有安装过python
$ sudo apt install python3
# 查看版本
$ python3 --version
#> Python 3.8.10
# 安装 virtualenv
# 也可以安装python3-venv: apt install python3.8-venv
# 如果安装了 python3-venv 那 virtualenv 命令改用 python3 -m venv 
$ python3 -m pip install --user virtualenv
# 创建python3.8的虚拟环境，因为现在 python3 --version 是3.8
$ virtualenv ~/.local/lib/venvs/3.8

```

### 安装 mod_wsgi
``` bash
$ sudo apt install libapache2-mod-wsgi-py3

```

```bash

# 安装 mod_wsgi
$ sudo apt install apache2-dev
# https://modwsgi.readthedocs.io/en/master/user-guides/quick-installation-guide.html#cleaning-up-after-build
# LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

$ sudo apt install python3-pip
# 安装 venv
# apt install python3.8-venv


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