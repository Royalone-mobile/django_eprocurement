# purchasemanager
## Python (Django) purchase and customer management app

This application is still under heavy development. If you use it, please submit issues in GitHub (https://github.com/mambojuice/purchasemanager)

#### Project layout

Path | Description
-----|------------
purchasemanager/ | Project root (created by django-admin startproject). Home to README.md and Django's manage.py script.
purchasemanager/attachments/ | FS location for attachment storage (located **OUTSIDE** the application root)
purchasemanager/db.sqlite3 | SQLite3 database file (located **OUTSIDE** the application root). Created when running 'python manage.py migrate'. Will not be present if you go straight to MySQL.
purchasemanager/purchasemanager/ | Application root
purchasemanager/purchasemanager/static/ | Static files (CSS, JS, etc)
purchasemanager/purchasemanager/wsgi.py | Python WSGI script for Apache integration


### Requirements
* pip (to install python packages)
* django

### Basic Installation
* This guide assumes Debian/Ubuntu is the running OS. Administrative rights are obtained using **sudo**.
* RPM-based systems should be similar. Windows is theoretically possible but untested.
* The application will be installed to **/opt/purchasemanager**
* Basic installation will get the application up and running, however it is not suitable for production use

1. Install pip
```bash
$ sudo apt-get install python-pip
```

2. Update pip to latest version (using sudo with pip requires the -H flag)
```bash
$ sudo -H pip install --upgrade pip
```

3. Install Django
```bash
$ pip install django
```

4. Download PurchaseManager from Github repo. Optionally, download the Zip file from https://github.com/mambojuice/purchasemanager/archive/master.zip
```bash
$ git clone https://github.com/mambojuice/purchasemanager --branch master
$ sudo cp -r purchasemanager /opt
$ cd /opt/purchasemanager
```

5. Edit the following lines of purchasemanager/settings.py to match your environment
```python
#  Put a random string at least 50 characters long here. This will keep hashed passwords safe.
SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()<>{}'

# Set to match system time
TIME_ZONE = 'UTC'
```

6. Create the application database
```bash
/opt/purchasemanager$ sudo python manage.py migrate
```

7. Create an admin user
```bash
/opt/purchasemanager$ sudo python manage.py create superuser
Username (leave blank to use 'root'): admin
Email address: admin@home.local
Password:
Password (again):
Superuser created successfully.
```

8. At this point, you should have enough configured to run the app using Python's development server. Run the following command and browse to http://localhost:8000
```bash
/opt/purchasemanager$ sudo python manage.py runserver 0.0.0.0:8000
```


### Using MySQL instead of SQLite3
1. Install MySQL client and Python MySQL driver
```bash
$ sudo apt-get install mysql-client
$ sudo -H pip install mysql-python
```

2. Create the MySQL database and user
```bash
$ mysql -u root -p [-h servername]
```
```sql
create database 'purchasemanager';
grant all on 'purchasemanager'.* to 'purchasemanager'@'%' identified by 'mysecretpassword';
exit;
```

4. Update purchasemanager/settings.py. Find the 'DATABASES' section, comment the sqlite database settings and uncomment the mysql settings.
```python
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Use settings below for local sqlite file

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#                 'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

# Use settings below for MySQL server (requires python-mysql)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'purchasemanager',
        'USER': 'purchasemanager',
        'PASSWORD': 'mysecretpassword',
        'HOST': 'servername',
        'PORT': '',
    }
}
```

### Using a production web server
It is highly recommended to use a 'real' web server for running purchasemanager. This example uses apache, however any wsgi-compatible server will work.

1. Install apache and wsgi module
```bash
$ sudo apt-get install apache2 libapache2-mod-wsgi
$ sudo a2enmod wsgi
```

2. Edit apache config to use wsgi.py included with purchasemanager and include static and attachments directories
```bash
$ sudo nano /etc/apache2/sites-enabled/000-default.conf
```

```apacheconf
# These lines must be outside of the VirtualHost directive
WSGIScriptAlias / /opt/purchasemanager/purchasemanager/wsgi.py
WSGIPythonPath /opt/purchasemanager

<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /opt/purchasemanager>
                Options Indexes MultiViews FollowSymLinks
                Require all granted
        </Directory>

        <Directory /opt/purchasemanager/purchasemanager>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

		# The real location of these directories can be moved if desired.
        # Remember to update /opt/purchasemanager/purchasemanager/settings.py to reflect changes here.
        Alias /static /opt/purchasemanager/purchasemanager/static
        Alias /attachments /opt/purchasemanager/attachments
</VirtualHost>
```

3. Restart apache and you should be in business!
```bash
$ sudo service apache2 restart
```
