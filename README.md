making_software
===============

This is a software to make software, where software means a web based system, in both ways.

With this software the user can deploy his or her own web based system without write a single line of code.

It works only in Linux distributions; and for the moment it has been tested on Debian/Ubuntu only.

Commiting to this project has just started, wait for more documents soon.

This project has two systems, separated layers which work together tied by a database.

Macro happy path diagram
========================
When you deploy your system, a completely independent system is created, without any external dependency. It is a 100% pure Python/Django system with it´s own database instance and a unique Apache virtual host appointment.

![Macro Diagram](making_software.png)


1st layer - Loopware folder 
===========================
This is a Python/Django web application.

Loopware is just a name, I will change in the future.

This website provides a web interface of the making software, where the end user can create his/her own system, just by adding, arranging, removing and editing visual components on a web browser.

I have used some 3rd part packages that I am distributing with my main package.

All of them have their own licenses included in the respective packages.
- allauth
- bsct
- django-fb-ifram-master
- wysiwyg_forms
- bootswatch
- django_admin_bootstrapped

Since it is a Django default application, you can install as usual.

I will documment settings file soon.



Database 
========
Database holds all data created on the 1st layer, and is readed by the 2nd layer.

Read db_sample.txt to install the sample DB provided for tests purpose.



2nd layer - making_software_perl folder
=======================================
This is a Perl standalone application.

This application reads data stored in the database and generates systems (web based applications) created by end users.

In order to install this application, you need of course to have Perl installed in you distribution.

You may need to install CPAN  modules required.

After download this package and unzip it wherever you want, follow instructions bellow to rightly set paths.


Install system module
---------------------
The Perl layer has one main class only, which holds data captured from database in a single object. This object has the options selected on the Python/Django web interface, and was stored on the database.

To install this class, go to Classes/Sistema and runs the executable script instala.


Configuring Perl application layer
----------------------------------
- hosts.template.pl

To use more than one environment,fill the Perl hash content of this file.

If you will use one environment only, forget this file.


- config.template.pl

To use more than one environment, you must have one config for each environment.

If you will use one environment only, you need to fill the configuration file and save it as config.pl
  
  

Executing Perl script
---------------------
The main script of the Perl layer is create_project.pl. It is called by a Django view at the first layer when the user triggers the creation of the system.
You can execute this manualy, it behaves exactly the same. 

Be carefull with the security alerts on running this script. I will document them soon.

To run this script you need to run as sudo from a directory owned by the same user wich runs Apache, because it will use this directory as a temporary directory to create files.

The outcome will be moved to the final directory.

perl /\<your Making Software home path\>/making_software/making_software_perl/create_project.pl \<id of the system\> \<your Making Software home path\>


If you want to read the concepts behind this project. Go to this paper:

http://robsonkoji.blogspot.com.br/2013/11/modeling-making-software.html



