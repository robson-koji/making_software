#!/usr/bin/perl

use 5.010000;
use strict;
use warnings;
use Sistema;
use Template;
use Sys::Hostname;
use HTML::Entities;


# $making_software_home - location of making_software_perl
# It is used to find the configuration files hosts.pl and config.pl
# And is used to find all the templates that ultimate create the system.
my ($projeto_id, $making_software_home) = @ARGV;

my $host = hostname; # Get local hostname
my %config; # Get configuration file
my %hosts = do "$making_software_home/making_software/making_software_perl/hosts.pl"; # Get configured hosts if any
my $prod;

unless (%hosts){
    %config = do "$making_software_home/making_software/making_software_perl/config.pl";    
}
else{
    foreach my $key (keys %hosts) {
        if ( $host eq $hosts{$key}->[0] ){
            %config = do "$making_software_home/making_software/making_software_perl/$hosts{$key}->[1]";    
            $prod = '1' if $key eq 'prod';
        }
    }
}


# Set environment variables
# They can get direct from the hash %config
my $temp_dir = $config{temp_dir};
my $dir_definitivo = $config{ultimate_dir};
my $django_admin = $config{django_admin};
my $postgres_host = $config{postgres_host};
my $postgres_pwd = $config{postgres_pwd};
my $postgres_user = $config{postgres_user};
my $apache_instance = $config{apache_instance};
my $subdomain_projetos = $config{subdomain_projetos}; 
my $domain = $config{domain};
my $virtual_host_string = $config{virtual_host_string};
my $echo = $config{echo};


# Sistema
my $sistema = Sistema->new("$projeto_id", $making_software_home);
my $project_name = $sistema->ProjectName();
my @elementos_organizados =  (sort { $a->{posicao_menu} <=> $b->{posicao_menu} } @{$sistema->{elementos}});# sort menu as set by user


# Call functions to create the system.
&CriaDB($project_name);
print ">>> Database has been created<br>\n";

&CriaProjeto($project_name);
print ">>> Project has been created<br>\n";

&CopiaDefaultApps($project_name);
print ">>> Default apps get cloned<br>\n";

&EditaSettings_py($project_name);
print ">>> Settings has been edited<br>\n";

&SyncDB($project_name);
print ">>> Database is synchronized<br>\n";

&SetSuperUser($project_name); #Django's auth system superuser
print ">>> Admin user has been created<br>\n";

&StartApps($project_name); # Inicializa arquivos de configuracao
print ">>> Applications get started<br>\n";

&EditaUrls_py($sistema); # Inclui as apps
print ">>> Controller layer has been set<br>\n";

&EditaBase_html($sistema); # Edita a barra de menu, menu e rodapeh
print ">>> Templates has been configured<br>\n";

&EditaSettings_py($project_name, $sistema); # Inclui as apps
print ">>> Applications added to the project<br>\n";

&SyncDB($project_name);
print ">>> Database has been synchronized once again<br>\n";

&Edita_tabela_django_site($sistema, $project_name);
print ">>> Site has been created<br>\n";

&CriaPgsEstaticas($project_name);
print ">>> Static pages have been created<br>\n";

&MvDirDefinitivo($project_name); # Move projeto para dir definitivo
print ">>> System physically moved<br>\n";

&SetFakeData($project_name); #Django's auth system superuser
print ">>> Mock data for tests set<br>\n";


&Runserver($project_name);
print ">>> Webserver is set, up and running<br>\n";

#&ConfigApache($project_name);
#print ">>> Webserver is set, up and running<br>\n";

exit;

sub Runserver{
    my ($project_name) = @_;
    system("python $dir_definitivo/$project_name/manage.py runserver localhost:8001 &");
}    


#
## Filesystem handling only
#
sub MvDirDefinitivo{
    my ($project_name) = @_;
    
    system("rm -rf $dir_definitivo/$project_name");       
    system("mv $temp_dir/$project_name $dir_definitivo");
    system("chmod -R 777 $dir_definitivo/$project_name");
}

sub CopiaDefaultApps{
    my ($project_name) = @_;
    
    #print "Copiando Default Apps<br>\n";
    system ("cp -r $making_software_home/making_software/making_software_perl/default_apps/* $temp_dir/$project_name/");
    
    # In production use only one allauth for all systems
    if ($prod) {
        system ("rm -rf $temp_dir/$project_name/allauth");
    }
}
    
    
#
## Apache configuration
#
sub ConfigApache{
    my ($project_name) = @_;
    
    &Configura_VirtualHosts($project_name);
    return;

    sub Configura_VirtualHosts{
        my ($project_name) = @_;

        #print "Gravando Apache VirtualHosts: $project_name<br>\n";
        my $file = "/etc/".$apache_instance."/sites-available/default";
        open VIRTUALHOSTS, "< $file" or die "Can't open $file : $!";
        my @virtualhosts = <VIRTUALHOSTS>;
        my $virtualhosts = "@virtualhosts";
        
        # para nao cadastrar virtual host igual.
        if ($virtualhosts =~ /WSGIProcessGroup $project_name/g) {
            return;
        }
        close VIRTUALHOSTS;

        # Get the new virtual host appointment
        my $output = &Template_VirtualHosts($project_name);

        # Include the string that will be substituted    
        $output = $virtual_host_string."\n".$output;
        
        # clean up end of lines
        $output = &LimpaFimDeLinha($output);

        # Substitute the old string with the new virtual host
        # appointment
        $virtualhosts =~ s/$virtual_host_string/$output/g; 
        
        open VIRTUALHOSTS, "> $file" or die "Can't open $file : $!";
        print VIRTUALHOSTS $virtualhosts, "\n";                
        close VIRTUALHOSTS;
        print $output, "\n\n\n";
        
        my $reload_command = "/etc/init.d/".$apache_instance;
        system("$reload_command reload");
        sleep(2);
        system("/usr/bin/wget -O - $subdomain_projetos/$project_name >/dev/null 2>&1 ");
        return;
        
        sub Template_VirtualHosts{
            my ($project_name) = @_;
    
            my $output = '';
            my $vars = {virtualhosts => {
                                        root_folder => $dir_definitivo,
                                        project_name => $project_name
                                      }
                        };
            
            my $template_local = "$making_software_home/making_software/making_software_perl/templates/virtualhosts";
            my $template = Template->new(ABSOLUTE => 1,);
            $template->process($template_local, $vars, \$output)
                || die "Template process failed: ", $template->error(), "\n";
            return $output;
        }  
    }
}


    


#
## Perl Template Toolkit files generation only
## It should be noted that Perl TT is used along the other functions too.
## But these basicaly use Perl TT only
#
sub EditaBase_html{
    my ($sistema) = @_;
    
    # Gerando dois base.html. Um para cada interface web (web e fb_app)
    my @bases = ('web', 'fb_app');
    foreach (@bases){
        my $html_file = $_."_base.html";

        my $output = &Template_Base_html($sistema, $html_file);
        $output = &LimpaFimDeLinha($output);
    
        #print "Gravando base.html do projeto<br>\n";
        my $file = "$temp_dir/$project_name/templates/$html_file";
        #my $file = "$temp_dir/$project_name/templates/base.html";
        open BASE_HTML_WRITE, "> $file" or die "Can't open $file : $!";
        print BASE_HTML_WRITE $output, "\n";
    }
    
    sub Template_Base_html{
        my ($sistema,$html_file) = @_;

        my $output = '';
        my $vars = {base => {
                                    logotipo =>  $sistema->{atributos}->{logotipo},
                                    sistema =>  $sistema->{atributos}->{nome},
                                    template => $sistema->{atributos}->{template},
                                    apps =>  \@elementos_organizados, 
                                  }
                    };
        
        my $template_local = "$making_software_home/making_software/making_software_perl/templates/$html_file";
        my $template = Template->new(ABSOLUTE => 1,);
        $template->process($template_local, $vars, \$output)
            || die "Template process failed: ", $template->error(), "\n";
        return $output;
    }
    
    


    # Gerando dois base.html para a aplicacao allauth.
    # Um para cada interface web (web e fb_app)
    my @bases_account = ('web_account', 'fb_app_account');
    foreach (@bases_account){
        my $html_file = $_."_base.html";

        my $output = &Template_Account_Base_html($sistema, $html_file);
        $output = &LimpaFimDeLinha($output);
    
        #print "Gravando base.html do allauth<br>\n";
        my $file = "$temp_dir/$project_name/templates/$html_file";
        #my $file = "$temp_dir/$project_name/templates/base.html";
        open ACCOUNT_BASE_HTML_WRITE, "> $file" or die "Can't open $file : $!";
        print ACCOUNT_BASE_HTML_WRITE $output, "\n";
    }
    
    sub Template_Account_Base_html{
        my ($sistema,$html_file) = @_;

        my $output = '';
        my $vars = {base => {
                                    logotipo =>  $sistema->{atributos}->{logotipo},
                                    sistema =>  $sistema->{atributos}->{nome},
                                    slug => $sistema->{atributos}->{slug},
                                  }
                    };
        
        my $template_local = "$making_software_home/making_software/making_software_perl/templates/$html_file";
        my $template = Template->new(ABSOLUTE => 1,);
        $template->process($template_local, $vars, \$output)
            || die "Template process failed: ", $template->error(), "\n";
        return $output;
    }     
}





sub EditaSettings_py{
    my ($project_name, $sistema) = @_;
    my $file = "$temp_dir/$project_name/$project_name/settings.py";
    
    # Atualizar variavel abaixo com dados do settings.py original
    # que precisam ser copiadas.
    my %original_settings_py_data;
    &GetSettings_pyOriginalData($file, \%original_settings_py_data);
    
    my $output = &Template_Settings_py(\%original_settings_py_data, $project_name, $sistema);
    $output = &LimpaFimDeLinha($output);

    #print $output, "\n\n";
    
    # Gravando settings.py
    #print "Gravando settings.py<br>\n";
    open SETTINGS_PY_WRITE, "> $file" or die "Can't open $file : $!";
    print SETTINGS_PY_WRITE $output, "\n";
    
    return;
    
    sub Template_Settings_py{
        my ($original_settings_py_data, $project_name, $sistema) = @_;
        
        # Se nao vier, manda aspas pra nao dar bosta.
        #$apps = '""' unless $apps;
        
        my $output = '';
        my $vars = {settings => {
                                    admins_nome => '' ,
                                    admins_email =>  '' , 
                                    allowed_hosts =>  '', 
                                    email_host =>  '', 
                                    db_name =>  $project_name, 
                                    db_user =>  $postgres_user, 
                                    db_pass =>  $postgres_pwd,
                                    postgres_host => $postgres_host,
                                    project_name =>  $project_name, 
                                    secret_key => $original_settings_py_data->{secret_key},
                                    apps =>   \@{$sistema->{elementos}}, 
                                    root_folder => $dir_definitivo,
                                    hash_config => \%config,
                                  }
                    };
        
        my $template_local = "$making_software_home/making_software/making_software_perl/templates/settings.py";
        my $template = Template->new(ABSOLUTE => 1,);
        $template->process($template_local, $vars, \$output)
            || die "Template process failed: ", $template->error(), "\n";
        return $output;
    }
    
    sub GetSettings_pyOriginalData{
        my ($file, $original_settings_py_data) = @_;
        # Nao consegui fazer o open, read, truncate, write com +>
        # Entao abrindo duas vezes.
        open SETTINGS_PY_READ, "< $file" or die "Can't open $file : $!";
        my @settings_py = <SETTINGS_PY_READ>;
        ($original_settings_py_data->{secret_key}) = "@settings_py" =~ /SECRET_KEY\s+\=\s+\'(.+?)\'/gi;
        
        #print "secret_key\t", $original_settings_py_data->{secret_key}, "\n";
        
        close SETTINGS_PY_READ;
    }    
}

sub EditaUrls_py{
    my ($sistema) = @_;

    my $output = &Template_Urls_py($sistema);
    $output = &LimpaFimDeLinha($output);

    #print "Gravando urls.py do projeto<br>\n";
    my $file = "$temp_dir/$project_name/$project_name/urls.py";
    open URLS_PY_WRITE, "> $file" or die "Can't open $file : $!";
    print URLS_PY_WRITE $output, "\n";

    
    sub Template_Urls_py{
        my ($sistema) = @_;

        my $output = '';
        my $vars = {urls => {
                                    apps =>  \@{$sistema->{elementos}}, 
                                  }
                    };
        
        my $template_local = "$making_software_home/making_software/making_software_perl/templates/project_urls.py";
        my $template = Template->new(ABSOLUTE => 1,);
        $template->process($template_local, $vars, \$output)
            || die "Template process failed: ", $template->error(), "\n";
        return $output;
    }      
}



#
## Each menut item of the system created by the user is a Django app.
## These functions performs a loop to create each of these app
## It configures models.py, views.py, admin.py and sql to create M2M fields
#
sub StartApps{
    my ($project_name) = @_;
    # Elementos
    my @apps;
    
    #Desregistra apps default no admin soh se for a primeira app
    # Qquer coisa ver o templates/admin.py
    my $idx = '0';
    
    # Esse array eh para nao gravar manytomany nos dois models, dah pau.
    my @manytomany;
        
    foreach (sort { $a->{posicao_menu} <=> $b->{posicao_menu} } @{$sistema->{elementos}}){
        my $relacionamentos = $sistema->RecuperaRelacionamentos($projeto_id, $_->{id});
        my $slug = $_->{slug};
        my $app_nickname = $_->{nome};
        my $subtitulo = $_->{descricao_curta};
        my $app_desc = $_->{descricao_completa};
        my $app_name = $_->{app_name};
        my $forms = $_->{forms};
        my $access_control = $_->{visibilidade};
        my $validade = $_->{validade};
        my $qt_elementos = $_->{qt_elementos};

        # Permissoes de todos
        # Checa permissao de grupo e permissao de sessao especifica contra permissao de todos.
        # Caso tenha mais de um tipo de permissao, prevalece a permissao para todos.
        my $todos_perms = $sistema->RecuperaPermissoes_de_Todos($_->{id});
        
        # Permissoes de grupo
        my $group_perms = '';
        if ($_->{grupo}) {
            $group_perms = $sistema->RecuperaPermissoes_de_Grupos($_->{id});

            for my $keys (%$group_perms){
                #delete($group_perms->{$keys}) if $todos_perms->{$keys};
                $group_perms->{$keys} = '' if $todos_perms->{$keys};
                #print "\n\n$app_nickname-------------------\t $keys\n";
            }
        }
        
        
        # Monta o hash de permissoes concedidas aa uma sessao especifica.
        # Chave do hash eh quem ganha a permissao e valor eh a permissao para o objeto especifico.
        # Quem ganha a permissao eh o reverso do FK. (owner do FK)
        my %permissoes;
#=pod        
        if ($_->{permission_create_id}){
            $permissoes{$_->{permission_create_id}}{'add_'.$slug}     =  'add_'.$slug      unless $todos_perms->{add_}
        }
        if ($_->{permission_read_id}){
            $permissoes{$_->{permission_read_id}}{'view_'.$slug}      =  'view_'.$slug     unless $todos_perms->{view_}
        }
        if ($_->{permission_update_id}){
            $permissoes{$_->{permission_update_id}}{'change_'.$slug}  =  'change_'.$slug   unless $todos_perms->{change_}
        }
        if ($_->{permission_delete_id}){
            $permissoes{$_->{permission_delete_id}}{'delete_'.$slug}  =  'delete_'.$slug   unless $todos_perms->{delete_}
        }
#=cut

                       
        # Em caso de relacionamentos M2M, essa sub deixa soh um para nao dar pau na criacao
        # das tabelas. Cria soh de um lado.
        $relacionamentos = &TrataM2M($relacionamentos, $_, \@manytomany) if $relacionamentos;

        if ($forms) {
            # Primeiro inicializar as aplicacoes
            &StartApp($project_name, $app_name, $slug);
            # Depois configura urls.py, models.py, admin.py, sql_files
            &ConfiguraAppsArquivos($project_name, $app_name, $forms, $app_desc, $idx, $app_nickname, $slug, $subtitulo, $access_control, $relacionamentos, $validade, $qt_elementos, $_, \%permissoes, $group_perms, $todos_perms);
        }        
        $idx++
    }    
    
    sub TrataM2M{
        my ($relacionamentos, $elemento, $manytomany) = @_;
        my @manytomany = @$manytomany;
        my $slug = $elemento->{slug};
        my $nome = $elemento->{nome};
        #my $validade = $elemento->{validade};
        
        #print "\t\t----NOME: $nome\n";
        foreach (@$relacionamentos){
            my $relacionamento = $_;
            # Se vier em branco, objeto estah relacionado ao Usuario
            #print "\t\tRelacionamentos: ", $relacionamento->{elemento_id} , "\t",  $relacionamento->{tipo_relacionamento} , "\t",  $relacionamento->{relates_to_id}, "\n\n";
                           
            #print "\n\n\n\n $relacionamento->{elemento_id} \t  $relacionamento->{relates_to_id} \t $slug \n\n\n";

            $relacionamento->{relates_to_id} = 'User' unless $relacionamento->{relates_to_id};
            #$relacionamento->{related_slug}  = $nome unless $relacionamento->{related_slug};
            foreach (@manytomany){
                #print "-----------\t", $relacionamento->{relates_to_id} , "\t",  $_->[0], "\t", $relacionamento->{related_slug} , "\n\n";
                if ($slug eq $_->[1] && $relacionamento->{relates_to_id} eq $_->[0] &&  $relacionamento->{tipo_relacionamento} eq $_->[2]) {
                    # mudando esse cara para nao gerar a tabela m2m nos dois modelos relacionados.
                    $relacionamento->{tipo_relacionamento} = '-1' 
                }
                # Pega o nome da app relacionada.
            }
            foreach (@{$sistema->{elementos}}){
                if ($relacionamento->{relates_to_id} eq $_->{slug}) {
                    $relacionamento->{related_slug} = $_->{nome};
                    $relacionamento->{validade} = $_->{validade};
                    
                    # Se o objeto nao for criado pelo admin nem pelo staff, o objeto eh privado e de uso somente do usuario
                    # que criou.
                    # Qdo eh criado pelo admin ou pelo staff, a listagem e o detalhe eh publico. Para nao ser,
                    # precisa excluir a url de visualizacao. Tem uma vulnerabilidade, por enquanto fica assim.
                    unless ($_->{visibilidade}) {
                        $relacionamento->{visibilidade} = "created_by_id = self.request.user ,";   
                    }
                }
            }
            push @manytomany, [$slug, $relacionamento->{relates_to_id}, $relacionamento->{tipo_relacionamento}, $nome ];
        }
        # Repete isso aqui pq tem elemento que nao possui relacionamento entao nao preenche dentro do loop acima.
        #push @manytomany, [$slug, '', '', $nome ];
        return $relacionamentos;
    }    
    sub ConfiguraAppsArquivos{
        my ($project_name, $app_name, $forms, $app_desc, $idx, $app_nickname, $slug,$subtitulo, $access_control, $relacionamentos, $validade, $qt_elementos, $elemento, $permissoes, $group_perms, $todos_perms) = @_;        
        my $output = &Template_Apps_Urls_py($project_name, $slug, $access_control);
        $output = &LimpaFimDeLinha($output);

        #print "Gravando urls.py da App: $app_name\n";
        my $file = "$temp_dir/$project_name/$slug/urls.py";
        open APP_URLS_PY_WRITE, "> $file" or die "Can't open $file : $!";
        print APP_URLS_PY_WRITE $output, "\n";

        &Configura_Models_py($project_name, $forms, $app_name, $app_nickname, $slug, $relacionamentos, $validade, $qt_elementos, $elemento);
        &ConfiguraSqlFile($project_name, $forms, $app_name, $slug);
        &Configura_Views_py($project_name, $forms, $app_desc, $slug,$subtitulo, $relacionamentos, $validade, $qt_elementos, $access_control, $elemento, $permissoes, $group_perms, $todos_perms);
        &Configura_Admin_py($project_name, $app_name, $idx, $forms, $slug, $relacionamentos, $validade);


        # Cria tabela M2M para "MultipleChoiceField"
        # No Configura_Models_py foi criada com as outras tabelas, a tabela dos choices para M2M.
        # Agora tem o mecanismo que popula os campos com os valores definidos pelo usuario no Making Software.
        # O mecanismo estah descrito aqui: https://docs.djangoproject.com/en/dev/howto/initial-data/
        # No item Providing initial SQL data
        sub ConfiguraSqlFile{
            my ($project_name, $forms, $app_name, $slug) = @_;
            # Forms
            foreach my $form_id (keys %$forms){
                #print $form_id, "\t",  $forms->{$form_id}->{name}, "\n";
                # Fields
                if ($forms->{$form_id}->{fields}) {
                    #print "\t", "Dados dos Campos:\n";
                    foreach my $field_pos (keys %{$forms->{$form_id}->{fields}{$form_id}}){
                        #print "FIELD TYPE:\t", $forms->{$form_id}->{fields}{$form_id}{$field_pos}{type}, "\n";
                        next unless $forms->{$form_id}->{fields}{$form_id}{$field_pos}{type} eq 'ManyToManyField';
                        #print "Achou MultipleChoiceField\n";                        

                        my $field_slug = $forms->{$form_id}->{fields}{$form_id}{$field_pos}{slug};
                        
                        #print $form_id, "\t", $field_pos, "\t", $field_slug, "\n";
                        #print $forms->{$form_id}->{fields}->{$form_id}{$field_pos}->{choices}, "\n";

                        if ($forms->{$form_id}->{fields}->{$form_id}{$field_pos}->{choices}) {
                            #my $field_id = ((keys %{$forms->{$form_id}->{fields}->{$form_id}{$field_pos}->{choices}})[0]);
                            #print $form_id, "\t", $field_pos, "\n";
                            
                            # https://docs.djangoproject.com/en/dev/howto/initial-data/
                            # Providing initial SQL data
                            # Cria SQL file para popular tabela M2M de MultipleChoiceField
                            my $output = &CriaSqlFile($forms->{$form_id}->{fields}->{$form_id}{$field_pos}{choices}, $app_name, $field_slug, $slug);
                            $output = &LimpaFimDeLinha($output);
                            
                            #print "Gravando sql_file.py da App: $app_name<br>\n";
                            system ("/bin/mkdir -p $temp_dir/$project_name/$slug/sql/");
                            
                            $forms->{$form_id}->{fields}->{$form_id}{$field_pos}{label} =~ s/\s+/_/gi;
                            my $sql_file_name = 'choices_'.lc($forms->{$form_id}->{fields}->{$form_id}{$field_pos}{slug}).'.sql';
                            my $file = "$temp_dir/$project_name/$slug/sql/$sql_file_name";
                            open SQL_FILE_WRITE, "> $file" or die "Can't open $file : $!";
                            print SQL_FILE_WRITE $output, "\n";                
                            #print $output, "\n\n\n";
                        }
                    }
                }
            }
            return;

            sub CriaSqlFile{
                my ($choices, $app_name, $field_slug, $slug) = @_;
                #print "Acessando template para criacao do SQL File\n";

                my $output = '';
                my $vars = {sql => {
					slug => $slug,
                                        field_slug => $field_slug,
                                        choices => $choices,
                                        app_name =>  $app_name, 
                                    }
                            };

                my $template_local = "$making_software_home/making_software/making_software_perl/templates/sql_file.sql";
                my $template = Template->new(ABSOLUTE => 1,);
                $template->process($template_local, $vars, \$output)
                    || die "Template process failed: ", $template->error(), "\n";
                return $output;
            }
        }
    
        sub Template_Apps_Urls_py{
            my ($project_name, $slug, $access_control) = @_;
    
            my $output = '';
            my $vars = {urls => {
                                    slug => $slug,
                                    project_name =>  $project_name,
                                    access_control => $access_control,
                                }
                        };
            
            my $template_local = "$making_software_home/making_software/making_software_perl/templates/apps_urls.py";
            my $template = Template->new(ABSOLUTE => 1,);
            $template->process($template_local, $vars, \$output)
                || die "Template process failed: ", $template->error(), "\n";
            return $output;
        }            

        sub Configura_Admin_py{
            my ($project_name, $app_name, $idx, $forms, $slug, $relacionamentos, $validade) = @_;

            foreach my $form_id (keys %$forms){
                my $output = &Template_Admin_py($app_name, $idx, $forms->{$form_id}->{fields}{$form_id}, $slug, $relacionamentos, $validade);
                $output = &LimpaFimDeLinha($output);
                    
                #print "Gravando admin.py da App: $app_name<br>\n";
                my $file = "$temp_dir/$project_name/$slug/admin.py";
                open ADMIN_PY_WRITE, "> $file" or die "Can't open $file : $!";
                print ADMIN_PY_WRITE $output, "\n";                
                #print $output, "\n\n\n";
            }
            return;


            sub Template_Admin_py{
                my ($app_name, $idx, $fields, $slug, $relacionamentos, $validade) = @_;
                $fields = &Get_Fields($fields, $relacionamentos, $validade);
        
                my $output = '';
                my $vars = {admin => {
                                            slug => $slug,
                                            fields => $fields,
                                            idx => $idx,
                                            app_name => $app_name
                                          }
                            };
                
                my $template_local = "$making_software_home/making_software/making_software_perl/templates/admin.py";
                my $template = Template->new(ABSOLUTE => 1,);
                $template->process($template_local, $vars, \$output)
                    || die "Template process failed: ", $template->error(), "\n";
                return $output;
            }
            
            sub Get_Fields{
                my ($fields, $relacionamentos, $validade) = @_;
                
=pod
                my $string;
                foreach my $keys (keys %{$fields}){
                    unless ($fields->{$keys}->{widget} eq "Textarea" ||
                                $fields->{$keys}->{widget} eq "FileInput" ||
                                $fields->{$keys}->{widget} eq "CheckboxSelectMultiple" ||
                                $fields->{$keys}->{widget} eq "Select" 
                                
                                ) {
                        $string .= "\"".$fields->{$keys}->{slug}."\""."\,";
                    }
                }
                return $string;
=cut                
                
                my $string = "\"id\"\, \"created_by\"\, ";
                foreach my $keys (sort keys %{$fields}){
                    unless ($fields->{$keys}->{widget} eq "Textarea" ||
                                $fields->{$keys}->{widget} eq "FileInput" ||
                                $fields->{$keys}->{widget} eq "CheckboxSelectMultiple" ||
                                $fields->{$keys}->{widget} eq "Select" 
                                ) {
                        $string .= "\"".$fields->{$keys}->{slug}."\""."\, ";
                        #print $form_id, "\t", $keys, "\t", $string, "\n\n";
                    }
                    # Funcao para pegar o nome qdo for checkbox.
                    # https://docs.djangoproject.com/en/1.3/ref/models/instances/#django.db.models.Model.get_FOO_display
                    if ($fields->{$keys}->{widget} eq "Select"){
                        $string .= "\"get_".$fields->{$keys}->{slug}."_display\"\, ";
                    }
                }
                # Funcao para pegar o nome qdo for fk, 1tom e m2m.
                #http://stackoverflow.com/questions/4564086/django-display-content-of-a-manytomanyfield
                foreach (@$relacionamentos){
                    if ($_->{tipo_relacionamento} == 1){
                        my $relates_to_id = $_->{relates_to_id};
                        $relates_to_id = "User" unless $relates_to_id;
                        $string .= "\"".$relates_to_id."\"\, ";
                    }
                    elsif ($_->{tipo_relacionamento} == 2){
                        my $relates_to_id = $_->{relates_to_id};
                        $relates_to_id = "User" unless $relates_to_id;
                        $string .= "\"".$relates_to_id."\"\, ";
                    }
                    if ($_->{tipo_relacionamento} == 3){
                        my $relates_to_id = $_->{relates_to_id};
                        $relates_to_id = "User" unless $relates_to_id;                
                        $string .= "\"".$relates_to_id."_m2m_reverso\"\, ";
                    }
                }
                #print "-------\t", $string, "\n\n\n";
                
                $string .= "\"validade_check\""."\, " if $validade;

                return $string;
                
            }
        }
        
        sub Configura_Views_py{
            my ($project_name, $forms, $app_desc, $slug, $subtitulo, $relacionamentos, $validade, $qt_elementos, $access_control, $elemento, $permissoes, $group_perms, $todos_perms) = @_;

            foreach my $form_id (keys %$forms){
                my $output = &Template_Views_py($app_desc, $slug,$subtitulo, $relacionamentos, $validade, $qt_elementos, $access_control, $elemento, $permissoes, $group_perms, $todos_perms);
                
                
                #print "Gravando views.py da App: $app_name<br>\n";
                my $file = "$temp_dir/$project_name/$slug/views.py";
                open VIEWS_PY_WRITE, "> $file" or die "Can't open $file : $!";
                
                $output = &LimpaFimDeLinha($output);
                
                print VIEWS_PY_WRITE $output, "\n";                
                #print $output, "\n\n\n";
            }
            #print "\n\n\n";
            return;


            sub Template_Views_py{
                my ($app_desc, $slug,$subtitulo, $relacionamentos, $validade, $qt_elementos, $access_control, $elemento, $permissoes, $group_perms, $todos_perms) = @_;
        
                #$app_desc  = encode_entities($app_desc);
                $app_desc =~ s/\R/<br>/g;
		

                my $output = '';
                my $vars = {views => {
                                            slug => $slug,
                                            app_desc => $app_desc,
                                            subtitulo => $subtitulo,
                                            relacionamentos => $relacionamentos,
                                            validade => $validade,
                                            access_control => $access_control,
                                            elemento => $elemento,
                                            permissoes => $permissoes,
                                            group_perms => $group_perms,
                                            todos_perms => $todos_perms,
                                            qt_elementos => $qt_elementos,
                                          }
                            };
                
                my $template_local = "$making_software_home/making_software/making_software_perl/templates/views.py";
                my $template = Template->new(ABSOLUTE => 1,);
                $template->process($template_local, $vars, \$output)
                    || die "Template process failed: ", $template->error(), "\n";
                return $output;
            }  
        }

        
        sub Configura_Models_py{
            my ($project_name, $forms, $app_name, $app_nickname, $slug, $relacionamentos, $validade, $qt_elementos, $elemento) = @_;

            # Forms
            foreach my $form_id (keys %$forms){
                my $output = &Template_Models_py($app_name, $forms->{$form_id}->{name}, $forms->{$form_id}->{fields}{$form_id}, $app_nickname, $form_id, $slug, $relacionamentos, $validade, $qt_elementos, $elemento);

                #print "Gravando models.py da App: $app_name<br>\n";
                my $file = "$temp_dir/$project_name/$slug/models.py";
                open MODELS_PY_WRITE, "> $file" or die "Can't open $file : $!";
                
                $output = &LimpaFimDeLinha($output);
                
                # Precisa pegar o ultimo unicode e passar para o final.
                # O ultimo unicode eh considerado como sendo o valor dos campos m2m qdo existem.
                # Essa operacao joga o primeiro para o final
                my ($first_unicode) = $output =~ /(def\s+__unicode__\(\s*self\s*\)\:\n\s+.+?\))/;
                $output = $output."\n\n    ".$first_unicode;
                
                print MODELS_PY_WRITE $output, "\n";                
                #print $output, "\n\n\n";
            }
            #print "\n\n\n";
            return;

            sub Template_Models_py{
                my ($app_name, $form_name, $fields, $app_nickname, $form_id, $slug, $relacionamentos, $validade, $qt_elementos, $elemento) = @_;
                my $stripped_form_name = $form_name =~ s/\s+/_/g;
                my $output = '';
                my $vars = {models => {
                                            slug => $slug,
                                            form_id => $form_id,
                                            app_nickname => $app_nickname, 
                                            app_name => $app_name,
                                            form_name => $form_name,
                                            stripped_form_name => $stripped_form_name,
                                            fields =>  $fields,
                                            relacionamentos => $relacionamentos,
                                            validade => $validade,
                                            qt_elementos => $qt_elementos,
                                            elemento => $elemento,
                                          }
                            };
                
                my $template_local = "$making_software_home/making_software/making_software_perl/templates/models.py";
                my $template = Template->new(ABSOLUTE => 1,);
                $template->process($template_local, $vars, \$output)
                    || die "Template process failed: ", $template->error(), "\n";
                return $output;
            }  
        }
    }
    
    sub StartApp{
        my ($project_name, $app_name, $slug) = @_;
        #print "StartApp: $app_name<br>\n";
        system("python $project_name/manage.py startapp $slug");
        
        #print "Movendo App \"$app_name\" para diretorio do projeto \"$project_name\"<br>\n";
        system("mv $slug $project_name/");
        
        # Para cada app, cria uma pasta no diretorio media
        system ("/bin/mkdir -p $temp_dir/$project_name/media/$slug");
        system ("/bin/chown www-data $temp_dir/$project_name/media/$slug");
    }    
}


    

#
## Django commands
## startproject, manage.py
#
sub CriaProjeto{
    my ($project_name) = @_;
    
    #print "Excluindo Projeto<br>\n";
    system ("rm -rf $temp_dir/$project_name/");

    #print "Criando Projeto<br>\n";
    system ("$django_admin startproject $project_name");
    
    
    #print "Configurando WSGI<br>\n";
    &Configura_WSGI_py($project_name); 

    # Movendo o decorators.py para a pasta da app com o nome do projeto.
    system("cp $making_software_home/making_software/making_software_perl/templates/decorators.py $temp_dir/$project_name/$project_name/");
    
    sub Configura_WSGI_py{
        my ($project_name) = @_;

        my $output = &Template_WSGI_py($project_name);
        $output = &LimpaFimDeLinha($output);
        
        #print "Gravando wsgi.py do Projeto: $project_name<br>\n";
        my $file = "$temp_dir/$project_name/$project_name/wsgi.py";
        open WSGI_PY_WRITE, "> $file" or die "Can't open $file : $!";
        print WSGI_PY_WRITE $output, "\n";                
        #print $output, "\n\n\n";
        return;


        sub Template_WSGI_py{
            my ($project_name) = @_;
    
            my $output = '';
            my $vars = {wsgi => {
                                        project_name => $project_name, 
                                        url_base => $dir_definitivo
                                      }
                        };
            
            my $template_local = "$making_software_home/making_software/making_software_perl/templates/wsgi.py";
            my $template = Template->new(ABSOLUTE => 1,);
            $template->process($template_local, $vars, \$output)
                || die "Template process failed: ", $template->error(), "\n";
            return $output;
        }  
    }    
    
    
        
}

sub SyncDB{
    my ($project_name) = @_;

    ## syncdb
    #print "Sincronizando DB<br>\n";
    # o "echo no" eh para responder a pergunta de criacao de usuario master.
    #system ("/usr/bin/python echo no | $temp_dir/$project_name/manage.py syncdb");
    system ("chmod -R 755 $temp_dir/$project_name/manage.py");
    system ("/usr/bin/python $echo $temp_dir/$project_name/manage.py syncdb");
    ##system ("/usr/bin/python $temp_dir/$project_name/manage.py syncdb");
}


sub Edita_tabela_django_site{
    my ($sistema, $project_name) = @_;

    # Cria arquivo json
    # Executa comando 'manage.py loaddata site.json',
    # que inclue nome e dominio do sistema criado na tabela django_site.
    my $output = &Django_Site($sistema);
    $output = &LimpaFimDeLinha($output);

    system ("/bin/mkdir -p $dir_definitivo/$project_name/fixtures/");
    
    my $file = "$dir_definitivo/$project_name/fixtures/site.json";
    open SITE_JSON_WRITE, "> $file" or die "Can't open $file : $!";
    print SITE_JSON_WRITE $output, "\n";
    close SITE_JSON_WRITE;

    system("python $dir_definitivo/$project_name/manage.py loaddata $dir_definitivo/$project_name/fixtures/site.json");

    
    sub Django_Site{
        my ($sistema) = @_;

        my $output = '';
        my $vars = {django_site => {
                                sistema => $sistema->{atributos}->{nome},
                                domain => $domain,
                            }
                    };
        
        my $template_local = "$making_software_home/making_software/making_software_perl/templates/site.json";
        my $template = Template->new(ABSOLUTE => 1,);
        $template->process($template_local, $vars, \$output)
            || die "Template process failed: ", $template->error(), "\n";
        return $output;
    }     
}





#
## Database handling only
## Should go to a module
#
sub CriaDB{
    my ($project_name) = @_;
    use DBI;
    use Error qw(:try);

    print "\n\n\n $postgres_user \t $project_name \n\n\n";
    my $dbh_projeto = DBI->connect("DBI:Pg: ;host=$postgres_host",
                                            $postgres_user, $postgres_pwd, {RaiseError => 1});   
    
    #print "Excluindo DB<br>\n";
    $dbh_projeto->do( qq(DROP DATABASE IF EXISTS $project_name) );

    #print "Criando DB<br>\n";
    $dbh_projeto->do( qq(CREATE DATABASE $project_name) );

    # Grava usuario no DB do seu projeto
    return 1;
}

sub SetFakeData{
    my ($project_name) = @_;
    use DBI;
    use Error qw(:try);

    my $dbh_projeto = DBI->connect("DBI:Pg:dbname=$project_name ;host=$postgres_host",
                                            $postgres_user, $postgres_pwd, {RaiseError => 1});    
    
    my @username = ('bbb','ccc');
    
    foreach(@username){
        &Cadastra($_);
    }

    sub Cadastra{
        my ($username) = @_;
        my $senha = 'pbkdf2_sha256$10000$WMdA9sv15M7q$ublzLqjA/OqPwBwENrdLqtqUTNQffywLAYFHNCYJMuw=' ;
                
        $sistema->{usuario}->{first_name} = "asdf" ; 
        $sistema->{usuario}->{last_name} = "asdf"; 
        $sistema->{usuario}->{email} = 'asdf@asdf.com'; 
        $sistema->{usuario}->{is_superuser} = 'False';
        $sistema->{usuario}->{is_staff} = 'False';
        $sistema->{usuario}->{is_active} = 'TRUE';
    
        my $query = "INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
    
        if ($dbh_projeto) {
           my $sth = $dbh_projeto->prepare($query);
           $sth->execute($senha,
                                    $sistema->{usuario}->{last_login},
                                    $sistema->{usuario}->{is_superuser},
                                    $username,
                                    $sistema->{usuario}->{first_name},
                                    $sistema->{usuario}->{last_name},
                                    $sistema->{usuario}->{email},
                                    $sistema->{usuario}->{is_staff},
                                    $sistema->{usuario}->{is_active},
                                    $sistema->{usuario}->{date_joined});
           $sth->finish;
        }
        else {
           #print "Cannot connect to Postgres server: $DBI::errstr\n";
           #print " db connection failed<br>\n";
        }
    }


    # Inserindo grupos
    system ("/bin/mkdir -p $dir_definitivo/$project_name/fixtures/");
    my @fake_yaml; 
    #my @fake_yaml = ('fake_groups.yaml', 'fake_papeis.yaml', 'fake_conhecimentos.yaml', 'fake_tecnologias.yaml', 'fake_projetos.yaml');
    
    foreach (@fake_yaml){
        system("cp $making_software_home/making_software/making_software_perl/templates/fake/$_ $dir_definitivo/$project_name/fixtures/");
        system("python $dir_definitivo/$project_name/manage.py loaddata $dir_definitivo/$project_name/fixtures/$_");
    }
    
}


sub SetSuperUser{
    my ($project_name) = @_;
    use DBI;
    use Error qw(:try);

    my $dbh_projeto = DBI->connect("DBI:Pg:dbname=$project_name ;host=$postgres_host",
                                            $postgres_user, $postgres_pwd, {RaiseError => 1});    
    
    $sistema->{usuario}->{first_name} = " " unless $sistema->{usuario}->{first_name}; 
    $sistema->{usuario}->{last_name} = " " unless $sistema->{usuario}->{last_name}; 
    $sistema->{usuario}->{email} = " " unless $sistema->{usuario}->{email}; 
    $sistema->{usuario}->{is_superuser} = 'TRUE';
    $sistema->{usuario}->{is_staff} = 'TRUE';
    $sistema->{usuario}->{is_active} = 'TRUE';

    my $query = "INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";


	if ($dbh_projeto) {
	   my $sth = $dbh_projeto->prepare($query);
	   $sth->execute($sistema->{usuario}->{password},
                                $sistema->{usuario}->{last_login},
                                $sistema->{usuario}->{is_superuser},
                                $sistema->{usuario}->{username},
                                $sistema->{usuario}->{first_name},
                                $sistema->{usuario}->{last_name},
                                $sistema->{usuario}->{email},
                                $sistema->{usuario}->{is_staff},
                                $sistema->{usuario}->{is_active},
                                $sistema->{usuario}->{date_joined});
       
       my $query_set_site = "INSERT INTO django_site (domain, name) VALUES (?, ?)" ;
	   my $sth_set_site = $dbh_projeto->prepare($query_set_site);
	   
       $sth_set_site->execute('exemplo.com', 'exemplo.com');
       
	   $sth_set_site->finish;
    }
	else {
	   #print "Cannot connect to Postgres server: $DBI::errstr\n";
	   #print " db connection failed<br>\n";
	}
}


sub CriaPgsEstaticas{
    my ($project_name) = @_;
    my $boas_vindas = $sistema->{atributos}->{boas_vindas};
    my $instrucoes = $sistema->{atributos}->{instrucoes};
    
    # Criando duas paginas
    &GravaFlatPages($project_name, '/fb_app/bem-vindo/',$boas_vindas, 'flatpages/fb_app_default.html' );
    &GravaFlatPages($project_name, '/fb_app/instrucoes/',$instrucoes, 'flatpages/fb_app_default.html' );        
    &GravaFlatPages($project_name, '/bem-vindo/',$boas_vindas, '');
    &GravaFlatPages($project_name, '/instrucoes/', $instrucoes, '');

    sub GravaFlatPages{
        my ($project_name, $url, $conteudo, $template_name) = @_;
        use DBI;
        use Error qw(:try);
    
        my $enable_comments = 0;
        #my $template_name = '';
        my $registration_required = 0;
        $registration_required = 1 if $url eq '/instrucoes/';

        my $dbh_projeto = DBI->connect("DBI:Pg:dbname=$project_name ;host=$postgres_host",
                                            $postgres_user, $postgres_pwd, {RaiseError => 1});    
        
        my $query = "INSERT INTO django_flatpage (url, title, content, enable_comments, template_name, registration_required )
                        VALUES (?, ?, ?, ?, ?, ?) RETURNING id";

        my $query2 = "INSERT INTO django_flatpage_sites(flatpage_id, site_id) VALUES (?, ?)";
    
    
        if ($dbh_projeto) {
            # Primeiro cria registro na tabela flatpage
            my $sth = $dbh_projeto->prepare($query);
            $sth->execute( $url, $sistema->{atributos}->{nome}, $conteudo, 0, $template_name, $registration_required);
            my $id = $sth->fetchrow_hashref();
            my $flatpage_id = $id->{"id"};
        	$sth->finish;           
        
            # Depois cria registro na tabela de relacionamento flatpage_id x site_id
            # Atencao no SITE_ID cravado como 1
            my $sth2 = $dbh_projeto->prepare($query2);
            $sth2->execute($flatpage_id, '1');
            $sth2->finish;           
        }
        else {
           #print "Cannot connect to Postgres server: $DBI::errstr\n";
           #print " db connection failed<br>\n";
        }
        return 1;
    }    
        
}







sub LimpaFimDeLinha{
    my ($output) = @_;                
    my $LF = "\012";
    my $CR = "\015";
    
    
    $output =~ s/$CR+//g;
    $output =~ s/u'$CR/u'/g;
    
    $output =~ s/$LF+/$LF/g;
    $output =~ s/$LF\s+$LF+/$LF/g;
    
    # Retira multiplas quebra de linha
    $output =~ s/\s+\R(?:\s*\R)+/\n/g;
    
    # Inclui de volta os LF, para nao ferrar a visualizacao em alguns dispositivos, como no shell.
    $output =~ s/$CR/$LF/g;
    
    
    $output =~ s/^(class\s)/\n\n\n$1/mg;
    $output =~ s/^(\s+class\s)/\n$1/mg;
    $output =~ s/^(\s+def\s)/\n$1/mg;
    
    return $output;
}