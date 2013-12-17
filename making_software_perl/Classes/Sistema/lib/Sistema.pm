package Sistema;

use 5.010001;
use strict;
use warnings;
use DBI;
use Error qw(:try);
use Sys::Hostname;



sub new {
	my $class = shift;
    my $id = shift;
    my $making_software_dir = shift;
    
	my $self = {};
	bless $self, $class;
    $self->db_connection($making_software_dir);
	$self->initialize($id);
	return $self;
}



#
## Metodos de classe
#
sub db_connection {
	my $self = shift;
    my $making_software_dir = shift;
    
    my $host = hostname; # Get local hostname
    my %hosts = do "$making_software_dir/making_software/making_software_perl/hosts.pl"; # Get configured hosts if any
    my %config; # Get configuration file
    my $prod;
    unless (%hosts){
        %config = do "$making_software_dir/making_software/making_software_perl/config.pl";    
    }
    else{
        foreach my $key (keys %hosts) {
            if ( $host eq $hosts{$key}->[0] ){
                %config = do "$making_software_dir/making_software/making_software_perl/$hosts{$key}->[1]";    
                $prod = '1' if $key eq 'prod';
            }
        }
    }
    $self->{'dbh_making_software'} = DBI->connect("dbi:Pg:dbname=making_software;host=$config{postgres_host}",
                            $config{postgres_user},$config{postgres_pwd}, {AutoCommit => 0, RaiseError => 1});
}

# Na inicializacao jah define o objeto a ser trabalhado, nao fazendo sentido portanto
# criar uma classe Sistema.
# Foi feito assim mais para testar e para deixar o codigo organizado.
sub initialize {
	my $self = shift;
    my $id = shift;

    $self->{'atributos'} = &RecuperaSistema($self, $id);
    $self->{'elementos'} = &GetApp($self);
    $self->{'usuario'} = &RecuperaUsuario($self, $id);
    
    #print $self->{'atributos'}->{'id'}, "\n";
    #exit;
    #print $self->{'sistema'}->{'id'}, "\n\n\n";

    return $self;        
}

sub GetApp{
    my ($self) = @_;
    my $elementos = &RecuperaElementos($self);

    my @elementos;
    foreach (@$elementos){
        # Due to elemento models inheritance.
        my $id_field_name = 'extendmodels_ptr_id';
        
        my $app_name = "_".$_->{$id_field_name}."_".$_->{nome};
    
        # somente caracteres ascii
        $app_name =~ s/[^!-~\s]//g;
        $app_name =~ s/\s+/_/g;
        $app_name = lc($app_name);
        
        # Insere nome da app na referencia de array dos elementos
        $_->{app_name} = $app_name;
        
        # Insere forms na referencia de array dos elementos
        my $forms = &RecuperaForm($self, $_->{$id_field_name});
        $_->{forms} = $forms;
        
        push @elementos, $_ if $forms;
    }    
    return \@elementos;
}
    
    
    
sub RecuperaRelacionamentos{
    my ($self, $sistema, $elemento) = @_;
    return;
    
    my $query = "SELECT * FROM relacionamentos_relacionamentos WHERE sistema_id = ? AND elemento_id = ? OR elemento_id is NULL";

	if ($self->{'dbh_making_software'}) {
	   my $sth = $self->{'dbh_making_software'}->prepare($query);
	   $sth->execute($sistema, $elemento);

       return $sth->fetchall_arrayref({});
       #return $sth->fetchrow_hashref;
       #my $loh = $sth_m->fetchall_arrayref({});
       
	   $sth->finish;
    }
	else {
	   print "Cannot connect to Postgres server: $DBI::errstr\n";
	   print " db connection failed\n";
	}
}


=pod
my $perms = &RecuperaPermissoes_de_Grupos('', 1);
for my $keys (%$perms){
    print $keys, "\n";
}
=cut

sub RecuperaPermissoes_de_Grupos{
    my ($self, $elemento_id) = @_;
    
    my $query = "SELECT * FROM elemento_elemento_grupo_permissoes WHERE elemento_id = ?";

	if ($self->{'dbh_making_software'}) {
        my $sth = $self->{'dbh_making_software'}->prepare($query);
        $sth->execute($elemento_id);

        my $array_ref = $sth->fetchall_arrayref();
        $sth->finish;
        
        my %perms;
        foreach (@$array_ref){
            $perms{add_} = 1 if $_->[2] == 1;
            $perms{view_} = 1 if $_->[2] == 2;
            $perms{change_} = 1 if $_->[2] == 3;
            $perms{delete_} = 1 if $_->[2] == 4;
        }
        return \%perms;
    }
	else {
	   print "Cannot connect to Postgres server: $DBI::errstr\n";
	   print " db connection failed\n";
	}
}
   
   
   
sub RecuperaPermissoes_de_Todos{
    return;
    my ($self, $elemento_id) = @_;
    
    my $query = "SELECT * FROM elemento_elemento_todos_permissoes WHERE elemento_id = ?";

	if ($self->{'dbh_making_software'}) {
        my $sth = $self->{'dbh_making_software'}->prepare($query);
        $sth->execute($elemento_id);

        my $array_ref = $sth->fetchall_arrayref();
        $sth->finish;
        
        my %perms;
        foreach (@$array_ref){
            $perms{add_} = 1 if $_->[2] == 1;
            $perms{view_} = 1 if $_->[2] == 2;
            $perms{change_} = 1 if $_->[2] == 3;
            $perms{delete_} = 1 if $_->[2] == 4;
        }
        return \%perms;
    }
	else {
	   print "Cannot connect to Postgres server: $DBI::errstr\n";
	   print " db connection failed\n";
	}
}

#
## Metodos de instancia
#
sub ProjectName{
    my ($self) = @_;
    
    my $project_name = $self->{atributos}->{slug};
    return $project_name;
}

=pod
my $forms = &RecuperaForm('', '9');
foreach (@$forms){
    print $_->{name}, "\t", $_->{fields}->{label}, "\t", $_->{fields}->{choices}->{label}, "\n";
    
}
=cut
sub RecuperaForm{
	my ($self, $elemento_id) = @_;

    # Pegando somente os FORMS que tem fields com label.
    # Senao nao retorna nada.
	my $query = "SELECT * FROM wysiwyg_forms_form
                    LEFT OUTER JOIN wysiwyg_forms_field
                        ON wysiwyg_forms_field.form_id = wysiwyg_forms_form.id
                    LEFT OUTER  JOIN wysiwyg_forms_choice
                        ON wysiwyg_forms_choice.field_id = wysiwyg_forms_field.id
                    WHERE wysiwyg_forms_form.elemento_id = ?
                    AND wysiwyg_forms_field.label IS NOT NULL";
                    
                    
                    

	if ($self->{'dbh_making_software'}) {
	   my $sth = $self->{'dbh_making_software'}->prepare($query);
       $sth->execute($elemento_id);
	   my $ref = $sth->fetchall_arrayref();

        # DB para Hash
        # Primeiro eh preciso executar o SELECT para ver o que estah retornando, eh uma referencia de array, armazenada em $ref.
        # Como eh um LEFT OUTER JOIN, tem tres tabelas.
        # Form contem field que contem choice.
        # O loop abaixo monta uma referencia de hash (forms) com hash (fields) com hash (choices).
        # Por enquanto sistema gera somente um form para cada elemento do sistema,
        # mas a estrutura abaixo estah preparada para receber mais de um form por elemento.
        my $forms;
        my $fields;
        my $choices;
        foreach(@$ref) {

            my $idx_choices;
            if ($_->[16]) {
                
                #print "asdf\n";
                #print $_->[18], "\t", $_->[19], "\t", $_->[20], "\n";
                #print "asdf\n\n\n";
                
                 $choices->{$_->[7]}{$_->[20]}{slug} = $_->[18];
                 $choices->{$_->[7]}{$_->[20]}{label} = $_->[19];
                 $choices->{$_->[7]}{$_->[20]}{position} = $_->[20];
                 $idx_choices++;
            }

            $fields->{$_->[0]}{$_->[13]}{choices} = $choices->{$_->[7]};
            $fields->{$_->[0]}{$_->[13]}{id} = $_->[7];
            $fields->{$_->[0]}{$_->[13]}{slug} = $_->[9];
            $fields->{$_->[0]}{$_->[13]}{label} = $_->[10];
            $fields->{$_->[0]}{$_->[13]}{help_text} = $_->[11];
            $fields->{$_->[0]}{$_->[13]}{type} = $_->[12];
            $fields->{$_->[0]}{$_->[13]}{position} = $_->[13];
            $fields->{$_->[0]}{$_->[13]}{required} = $_->[14];
            $fields->{$_->[0]}{$_->[13]}{widget} = $_->[15];
             
            $forms->{$_->[0]}{fields} = $fields if $fields->{$_->[0]}{$_->[13]}{label};
            $forms->{$_->[0]}{name} = $_->[4];
            $forms->{$_->[0]}{description} = $_->[6];
        }
        return $forms;
        
        $sth->finish;
    }
	else {
	   print "Cannot connect to Postgres server: $DBI::errstr\n";
	   print " db connection failed\n";
	}
}



#
## Metodos de acesso ao banco
#
sub RecuperaSistema{
	my ($self, $id) = @_;
	my $query = "SELECT * FROM sistema_sistema WHERE id = ?";

	if ($self->{'dbh_making_software'}) {
	   my $sth = $self->{'dbh_making_software'}->prepare($query);
	   $sth->execute($id);

       return $sth->fetchrow_hashref;
       
	   $sth->finish;
    }
	else {
	   print "Cannot connect to Postgres server: $DBI::errstr\n";
	   print " db connection failed\n";
	}
}


sub RecuperaElementos{
	my ($self) = @_;
	my $query = "SELECT * FROM elemento_elemento WHERE sistema_id = ?";
    
    my @elementos;
	if ($self->{'dbh_making_software'}) {
	   my $sth = $self->{'dbh_making_software'}->prepare($query);
	   $sth->execute($self->{'atributos'}->{id});
       return $sth->fetchall_arrayref({});
       
#       return $sth->fetchall_arrayref();

	   $sth->finish;
    }
	else {
	   print "Cannot connect to Postgres server: $DBI::errstr\n";
	   print " db connection failed\n";
	}
}

sub RecuperaUsuario{
	my ($self, $id) = @_;
    my $query = "SELECT * FROM auth_user
                    WHERE EXISTS
                        (
                        SELECT 1
                        FROM sistema_sistema
                        WHERE auth_user.id = sistema_sistema.created_by_id
                        AND sistema_sistema.id = ?
                        )";

	if ($self->{'dbh_making_software'}) {
	   my $sth = $self->{'dbh_making_software'}->prepare($query);
	   $sth->execute($id);
       return $sth->fetchrow_hashref;
       
	   $sth->finish;
    }
	else {
	   print "Cannot connect to Postgres server: $DBI::errstr\n";
	   print " db connection failed\n";
	}
}


1;
