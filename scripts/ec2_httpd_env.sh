#!/bin/bash

apt-get update -y
apt-get install gcc -y
apt-get install git -y
apt-get install python-dev python-pip -y
apt-get install apache2 apache2-dev -y
apt-get install libmysqlclient-dev -y
apt-get install python-virtualenv -y

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

# Prepare the directory structure.
mkdir /var/www/site
mkdir /var/www/site/static
# Logs (this is a bad location for permanant logs).
touch /tmp/db.debug.log
chmod 777 /tmp/db.debug.log

cd ..
curl -s http://snowball.tartarus.org/wrappers/PyStemmer-1.3.0.tar.gz | tar xzf -
cd /PyStemmer-1.3.0
python setup.py install

cd /var/www/site
# Get the source code.
git clone https://github.com/zafoof/scalica-search.git depot
cd depot
git checkout master
pip install -r requirements.txt
#python web/scalica/rpc_search/index/index_service.py &
#python web/scalica/rpc_search/rpc_search/search_service.py &
./first_install.sh
cd db
./install_db.sh
cd ../../
source depot/env/bin/activate
mv depot/web/scalica/ scalica
cd scalica
python manage.py makemigrations micro
python manage.py migrate
python manage.py collectstatic --noinput

# Use the following config.
cat <<EOF > /etc/apache2/sites-available/scalica.conf
WSGIScriptAlias / /var/www/site/scalica/scalica/wsgi.py
WSGIDaemonProcess scalica python-path=/var/www/site/scalica:/var/www/site/depot/env/lib/python2.7/site-packages
WSGIProcessGroup scalica
WSGIApplicationGroup %{GLOBAL}
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
