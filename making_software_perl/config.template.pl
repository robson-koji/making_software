# If you will use one environment only, you need to fill the configuration file and save it as config.pl
# To use more than one environment, you must have one config for each environment and save each if own name.
# In this case you have to fill the file hosts.pl and set the name of each file according to it´s environment.



# Full path to making_software folder.
# The folder where you open making_sofware package.
# ie your home: '/home/your_name'
making_software_perl_dir => '/home/your_name',


# Apache user (www-data) executes create_project.pl
# You can create an specific folder owned by Apache user (www-data) to hold
# temp file during creation of the systems. Or you can just leave the original
# folder used by the Apache user to serve files, like /var/www.
#temp_dir => '/var/www',
temp_dir => '/var/www',



# Folder to deploy the code of the created system.
# This folder will be accessed via WSGI by Apache.
ultimate_dir => '/home/making_software/projects',


# This is the Django binary that starts Django projects
django_admin => '/usr/bin/django-admin',


# Postgres´ socket folder.
# /var/run/postgresql/.s.PGSQL.5432 or /tmp or elsewhere
postgres_host => '/var/run/postgresql/',


# Password to connect to postgres.
postgres_user => 'postgres',


# Password to connect to postgres.
postgres_pwd => '',


# Instance of Apache that will contain the systems created by Making Software.
# It is highly recommended to use one an specific instance for the systems created
# by Making Software, since the webserver is reloaded each time a system is created.
# If you have other system, like Making Software itself running at this same instance,
# it will stop on each realod of the web server.
apache_instance => 'apache2',


# For each system created, Making Software make the first request in order to not receive
# an apache error, due to reload.
subdomain_projetos => 'http://local_ip:port/',


# This is the domain that will be used in the Django site table.
# Maybe it can use the same variable defined above.
domain => 'local_ip:port',


# This is a weird behavior that shall be debuged.
# When executing the Django command "manage.py syncdb", a question requires an answer to
# create or not a master user.
# Some environments need the "echo no" answer, while other require an empty answer.
# So select the best for you use.
esdruxulo => 'echo no |',

