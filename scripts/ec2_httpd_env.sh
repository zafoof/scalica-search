#!/bin/bash

apt-get update -y
apt-get install gcc -y
apt-get install git -y
apt-get install python-dev python-pip -y
apt-get install apache2 apache2-dev -y
apt-get install libmysqlclient-dev -y

export DEBIAN_FRONTEND=noninteractive
apt-get -q -y install mysql-server -y

mkdir /home/ubuntu/tmp
chmod -R 777 /home/ubuntu/tmp

# In working dir
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.4.13.tar.gz
tar xzvf 4.4.13.tar.gz
cd mod_wsgi-4.4.13/
./configure
make
make install
# Enable the module
sh -c "echo 'LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so' > /etc/apache2/mods-available/wsgi.load"
a2enmod wsgi
service apache2 restart
make clean

#install a virtualenv
pip install virtualenv
mkdir /var/www/site
mkdir /var/www/site/static

touch /tmp/db.debug.log
chmod 777 /tmp/db.debug.log

cd /var/www/site
virtualenv --system-site-packages .
source ./bin/activate
pip install Django==1.8
pip install MySQL-python==1.2.5
pip install django-debug-toolbar==1.3.2

# Get the python source files/ Git or tarball
git clone http://23.236.49.28/git/scalica.git depot
cd depot
git checkout httpd
cd db
./install_db.sh
cd ../../
mv depot/web/scalica/ scalica
cd scalica
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Use the following config.
cat <<EOF > /etc/apache2/sites-available/scalica.conf
WSGIScriptAlias / /var/www/site/scalica/scalica/wsgi.py
WSGIDaemonProcess scalica python-path=/var/www/site/scalica:/var/www/site/lib/python2.7/site-packages
WSGIProcessGroup scalica
<Directory /var/www/site/scalica/scalica>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>

Alias /static/ /var/www/site/static/
<Directory /var/www/site/static>
  Require all granted
</Directory>

EOF
a2ensite scalica
service apache2 reload
# We should be able to serve now.
