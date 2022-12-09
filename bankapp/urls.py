from django.urls import path, include
from . import views
from . import admin_logic

urlpatterns = [
    path('',views.index, name='index'),
    path('register',views.registration, name='register'),
    path('login',views.login, name='login'),
    path('user_dashboard',views.user_dashboard, name='user_dashboard'),
    path('logout',views.logout1, name='logout'),
    path('update_profile/<int:n>',views.update_profile, name='update_profile'),
    path('invest',views.invest, name='invest'),
    path('success/', views.payu_success, name = 'success'),
    path('failure/', views.payu_failure, name = 'failure'),
    path('investdetail/', views.investdetail, name = 'investdetail'),
    path('referal/', views.referal, name = 'referal'),
    path('wallet/', views.wallet, name = 'wallet'),
    path('test/', views.test, name = 'test'),
    path('balance/<int:n>', views.balance, name = 'balance'),
    path('registered-users/', admin_logic.registered_users, name = 'registered_users'),
    path('transection-detail/<int:n>', admin_logic.user_transection_detail, name = 'transection_detail'),
    path('deposite', admin_logic.deposit, name = 'deposite'),
    path('test1', views.test1, name = 'test1'),
    path('widthrow', views.trandetail, name = 'widthrow'),
    path('walletaddress', views.walletaddress, name = 'walletaddress'),
    path('userwithdrow', views.userwithdrow, name = 'userwithdrow'),
    path('withdrowreport', views.withdrowreport, name = 'withdrowreport'),
    path('gatewayinvoice', views.gatewayinvoice, name = 'gatewayinvoice'),
    path('transferutility', views.transferutility, name = 'transferutility'),
    path('transferwallet', views.transferwallet, name = 'transferwallet'),
    path('user_pay_history', admin_logic.user_pay_history, name = 'user_pay_history'),
    path('depositeoneuser/<int:n>', admin_logic.depositeoneuser, name = 'depositeoneuser'),
]
