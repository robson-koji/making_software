#!/bin/sh

#
## Install CPAN Modules
#

# To default cpan answer all to yes.
export PERL_MM_USE_DEFAULT=1

cpan DBI
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
