# Zafoogle for Scalica

## First installation:

** Install required packages. **
    $ sudo apt-get update; sudo apt-get install mysql-server libmysqlclient-dev python-dev python-virtualenv
(Mysql appserver password is already created)

    $ ./first_install.sh

** Install the proper databases **
- $ cd db
- $ ./install_db.sh
(password is foobarzoot)
- $ cd ..

** Sync the database **
- $ source ./env/bin/activate
- $ cd web/scalica
- $ python manage.py makemigrations micro
- $ python manage.py migrate

** Download the following **
- cd ../.. 
- python -m pip install grpcio
python -m pip install grpcio-tools
python -m pip install redis
curl -s http://snowball.tartarus.org/wrappers/PyStemmer-1.0.1.tar.gz | tar xzf -


** After the first installation, from the project's directory **
** Run the server: **
$ source ./env/bin/activate
$ cd web/scalica
$ python manage.py runserver

python
>>> import nltk
>>> nltk.download('stopwords')

## Access the site at http://localhost:8000/micro
