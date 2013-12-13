from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns("",
    url(r"^email/$", views.email,
        {'interface_template': 'web_account_base.html',
         'my_account_email':'account_email'}, name="account_email"),
    
    url(r"^signup/$", views.signup,
        {'interface_template': 'web_account_base.html'}, name="account_signup"),
    
    url(r"^login/$", views.login,
        {"my_success_url":"fb_app_instrucoes",
         'interface_template': 'web_account_base.html',
         'my_account_login':'account_login'}, name="account_login"),
    
    url(r"^password/change/$", views.password_change,
        {"my_success_url":"account_change_password",
         "my_account_set_password":"account_set_password",
         'interface_template': 'web_account_base.html'}, name="account_change_password"),
    
    url(r"^password/set/$", views.password_set,
        {"my_success_url":"account_set_password",
         'interface_template': 'web_account_base.html'}, name="account_set_password"),

#    url(r"^password_delete/$", views.password_delete, name="acct_passwd_delete"),
#    url(r"^password_delete/done/$", "django.views.generic.simple.direct_to_template", {
#        "template": "account/password_delete_done.html",
#    }, name="acct_passwd_delete_done"),

    url(r"^logout/$", views.logout,
        {'my_account_logout':'account_logout',
         'interface_template': 'web_account_base.html'}, name="account_logout"),
    
    url(r"^confirm_email/(?P<key>\w+)/$", views.confirm_email,
        {'interface_template': 'web_account_base.html',
         'my_success_redirect': 'account_login',
         'my_account_confirm_email': 'account_confirm_email'}, name="account_confirm_email"),
    
    # password reset
    url(r"^password/reset/$", views.password_reset,
        {'interface_template': 'web_account_base.html'}, name="account_reset_password"),
    
    url(r"^password/reset/done/$", views.password_reset_done,
        {'interface_template': 'web_account_base.html'}, name="account_reset_password_done"),
    
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.password_reset_from_key,
        {'interface_template': 'web_account_base.html'}, name="account_reset_password_from_key"),
    
    url(r"^password/reset/key/done/$", views.password_reset_from_key_done,
        {'interface_template': 'web_account_base.html'}, name="account_reset_password_from_key_done"),


    # accounts para o fb_app
    url(r"^fb_app/email/$", views.email,
        {'interface_template': 'fb_app_account_base.html',
         'my_account_email':'fb_app_account_email'}, name="fb_app_account_email"),
    
    url(r"^fb_app/signup/$", views.signup,
        {'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_signup"),
    
    url(r"^fb_app/login/$", views.login,
        {"my_success_url":"fb_app_instrucoes",
         'interface_template': 'fb_app_account_base.html',
         'my_account_login':'fb_app_account_login'}, name="fb_app_account_login"),
    
    url(r"^fb_app/password/change/$", views.password_change, 
        {"my_success_url":"fb_app_account_change_password",
         "my_account_set_password":"fb_app_account_set_password",
         'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_change_password"),
    
    url(r"^fb_app/password/set/$", views.password_set, 
        {"my_success_url":"fb_app_account_set_password",
         'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_set_password"),
    
    url(r"^fb_app/logout/$", views.logout,
        {'my_account_logout':'fb_app_account_logout',
         'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_logout"),
    
    url(r"^fb_app/confirm_email/(?P<key>\w+)/$", views.confirm_email, 
        {'interface_template': 'fb_app_account_base.html',
         'my_success_redirect': 'fb_app_account_login',
         'my_account_confirm_email': 'fb_app_account_confirm_email'}, name="fb_app_account_confirm_email"),
    
    # password reset
    url(r"^fb_app/password/reset/$", views.password_reset, 
        {'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_reset_password"),
    
    url(r"^fb_app/password/reset/done/$", views.password_reset_done, 
        {'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_reset_password_done"),
    
    url(r"^fb_app/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.password_reset_from_key, 
        {'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_reset_password_from_key"),
    
    url(r"^fb_app/password/reset/key/done/$", views.password_reset_from_key_done, 
        {'interface_template': 'fb_app_account_base.html'}, name="fb_app_account_reset_password_from_key_done"),
)
