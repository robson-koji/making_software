# If you will use one environment only, you need to fill the configuration file and save it as config.pl
# To use more than one environment, you must have one config for each environment and save each if own name.
# In this case you have to fill the file hosts.pl and set the name of each file according to it´s environment.


# For development environment, created systems will be temporarily deployed at
# the sama making_software_perl directory.
# If you have installed Making Software at your home dir, set you name here.
temp_dir => '/home/robson/projetos/making_software/making_software_perl',


# For production environment or an environment with Apache.
# Apache user (www-data) executes create_project.pl. In order to allow
# Apache to create folder, you can create an specific folder owned by Apache
# user (www-data) to hold temp file during creation of the systems.
# Or you can just leave the original folder used by the Apache user to serve files,
# like /var/www.
#temp_dir => '/var/www',


# Folder to deploy the code of the created system.
# This folder will be accessed via WSGI by Apache.
ultimate_dir => '/home/making_software/projects',


# This is the Django binary that starts Django projects
django_admin => '/usr/local/bin/django-admin.py',



# Instance of Apache that will contain the systems created by Making Software.
# It is highly recommended to use one an specific instance for the systems created
# by Making Software, since the webserver is reloaded each time a system is created.
# If you have other system, like Making Software itself running at this same instance,
# it will stop on each realod of the web server.
#apache_instance => 'apache2',


# For each system created, Making Software make the first request in order to not receive
# an apache error, due to reload.
subdomain_projetos => 'http://localhost:8001',


# This is the domain that will be used in the Django site table.
# Maybe it can use the same variable defined above.
domain => 'http://localhost:8001',


# This is a weird behavior that shall be debuged.
# When executing the Django command "manage.py syncdb", a question requires an answer to
# create or not a master user.
# Some environments need the "echo no" answer, while other require an empty answer.
# Select the best the case.
echo => 'echo no |',


### DATABASE ###

# Set the database you will use.
# Possible values are 'postgres' and 'sqlite'
database => 'sqlite',

# Password to connect to postgres.
db_user => 'db_user',


# Password to connect to postgres.
db_pwd => 'db_pwd',


# If you select postgres, set Postgres´ socket folder.
# /var/run/postgresql/.s.PGSQL.5432, /tmp or elsewhere
postgres_host => '/var/run/postgresql/',


