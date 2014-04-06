#!/bin/sh

#
## Install CPAN Modules
#

# To default cpan answer all to yes.
export PERL_MM_USE_DEFAULT=1

cpan DBI
cpan DBD::SQLite
cpan Template


#
## Install Sistema Module
#

SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
PERLCLASS_PATH="$SCRIPT_PATH/making_software_perl/Classes/Sistema/"
#echo $PERLCLASS_PATH

(cd $PERLCLASS_PATH && perl Makefile.PL)
(cd $PERLCLASS_PATH && make)
(cd $PERLCLASS_PATH && make install)


#
## Setting config files
#

# This is used while operating more than one environment. 
cp making_software_perl/hosts.template.pl making_software_perl/hosts.pl


# Create ulitimate projects' directory
TMP_DIR='/home/making_software/tmp'
mkdir -p $TMP_DIR
chmod 777 $TMP_DIR

PROJECTS_DIR='/home/making_software/projects'
mkdir -p $PROJECTS_DIR
chmod 777 $PROJECTS_DIR


