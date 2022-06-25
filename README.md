# your downloader

youtube video downloador

- language: python
- framework: django

### 安装python3

```bash
# 如果没有安装过python3
$ sudo apt install python3
# 查看版本
$ python3 --version
#> Python 3.8.10
```

### 安装 python venv 虚拟环境
```bash
# 安装 virtualenv  
$ sudo apt install python3-venv
# 创建虚拟环境
$ python3 -m venv ~/.local/lib/venvs/3.8
# 启用虚拟环境
$ source ~/.local/lib/venvs/3.8/bin/activate
# 如果要退出虚拟环境
# $ deactivate
# venv也可以用 pip 安装 virtualenv
# $ python3 -m pip install --user virtualenv
# $ virtualenv ~/.local/lib/venvs/3.8
# 进入项目目录
$ cd dlpython目录
# 安装依赖包
$ pip install -r requirements.txt
# 导出依赖包方法
# pip freeze >requirements.txt

```

### 安装 mod_wsgi

``` bash
$ sudo apt install libapache2-mod-wsgi-py3
```
mod_wsgi 编译安装方法

```bash
# 
# 文档网址
# https://modwsgi.readthedocs.io/en/master/user-guides/quick-installation-guide.html#cleaning-up-after-build
# 
# https://github.com/GrahamDumpleton/mod_wsgi/releases
# 下载最新版
$ wget https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/4.9.2.tar.gz
# 解压缩
$ tar -zxvf 4.9.2.tar.gz
$ cd mod_wsgi-4.9.2/
# 安装 apache2-dev
$ sudo apt install apache2-dev
# 查看 apxs 位置
$ which apxs
#> /usr/bin/apxs
# 查看 python3 位置
$ which python3
#> /usr/bin/python3
# 配置安装环境
$ ./configure --with-apxs=/usr/bin/apxs --with-python=/usr/bin/python3
# 编译
$ make
# 安装
$ sudo make install
# apache 启用 mod_wsgi
# LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
$ sudo a2enmod wsgi

```

### Apache 创建VirtualHost

```bash
$ cd /etc/apache2/sites-available
$ sudo vim xxx.com.conf
```


```bash
# xxx.com.conf
# 域名
Define var_domain xxx.com
# 项目目录
Define var_document_root /var/www/dlpython
# Python Virtual environment
Define var_venv /home/用户名/.local/lib/venvs/3.8

<VirtualHost *:80>
  ServerName ${var_domain}
  RewriteEngine on
  RewriteCond %{HTTPS} !=on
  RewriteRule ^(.*) https://%{SERVER_NAME}$1 [L,R]
</VirtualHost>

<VirtualHost *:443>
    ServerName ${var_domain}
    ServerAdmin xxx@xxx.com
    DocumentRoot ${var_document_root}

    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/xxx.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/xxx.com/privkey.pem

    Alias /static ${var_document_root}/static

    WSGIDaemonProcess ${var_domain} processes=2 threads=15 lang='en_US.UTF-8' locale='en_US.UTF-8' python-home=${var_venv} python-path=${var_document_root}

    WSGIProcessGroup ${var_domain}

    WSGIScriptAlias / ${var_document_root}/dlpython/wsgi.py

    <Directory ${var_document_root}/dlpython>
        Options FollowSymLinks
        DirectoryIndex disabled
        AllowOverride none
        <Files wsgi.py>
           Require all granted
        </Files>
    </Directory>

     <Directory ${var_document_root}/static>
           Require all granted
           DirectoryIndex disabled
     </Directory>

</VirtualHost>
```
```bash
#dlpython/dlpython/local_settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_DIRS = [
    # BASE_DIR / "static",
]

ALLOWED_HOSTS = ['*']
```

### 迁移数据库

```bash
# 迁移数据库
$ python manage.py migrate
# 创建管理账号
$ python manage.py createsuperuser
# sqlite文件需要写权限，项目目录也要写权限，不然会出现: attempt to write a readonly database
$ chmod 0777 db.sqlite3
$ chmod 0777 ../dlpython

```
### 重启 Apache 

```bash
# 重启 Apache 
$ sudo systemctl restart apache2
# 或者
# $ sudo /etc/init.d/apache2 restart
# $ sudo systemctl reload apache2
# $ sudo /etc/init.d/apache2 reload
# $ sudo apachectl reload
```

### 备注

```bash
# 复制 static
# $ python manage.py collectstatic
```