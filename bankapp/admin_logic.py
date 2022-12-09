from django.shortcuts import render, redirect, HttpResponse
from conix.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from .models import TotalAmountReturn, User,Invest, WidthrowInfo, WithdrowNotification, Wollate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import razorpay
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
import pytz
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

utc=pytz.UTC

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def registered_users(request):
    user = User.objects.all()
    return render(request, 'dashboard/registered_user.html', {'data':user})

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def registered_users(request):
    user = Invest.objects.filter(payment_status = 1)
    return render(request, 'dashboard/invested_user.html', {'data':user})


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def user_transection_detail(request, n):
    total_invest = 0
    total_amount = 0
    user = User.objects.get(id=n)
    invest = Invest.objects.filter(user = user)[::-1]
    for item in invest:
        total_invest = total_invest + int(item.invest_amount)
        total_amount = total_amount + int(item.percentage_amount)
    return render(request, 'dashboard/transection_detail.html', {'data':invest, 'total':total_invest, 'invest':total_amount})


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def deposit(request): 
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        user = request.POST.getlist('email')
        notification = request.POST.getlist('notification')
        amount_withdrow = request.POST.getlist('hmdot')

        for u, noti, aw  in zip(user, notification, amount_withdrow):
            userdata = User.objects.get(id = int(u))
            notification = WithdrowNotification.objects.get(id= int(noti))
            wal = TotalAmountReturn.objects.get(user = userdata)

            if wal.total_return >= float(aw):
                wal.total_widthrow = wal.total_widthrow + float(aw)
                wal.total_return = wal.total_return - float(aw)
                wal.save()
                notification.seen = True
                notification.send = True
                notification.save()
            else:
               notification.status = False
               notification.save()

        return render(request, 'dashboard/depositpayment.html')
    notification = WithdrowNotification.objects.filter(Q(send=False) and Q(status = True))
    for i in notification:
        i.seen = True
        i.save()
    return render(request, 'dashboard/depositpayment.html', {"noti":notification})

# @login_required(login_url='/login')
# @user_passes_test(lambda u: u.is_superuser)
# def successfulldepo(request):
    

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def user_pay_history(request):
    return render(request, 'dashboard/user_pay_history.html')


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def depositeoneuser(request, n):
    if request.method == "POST":
        user_id = int(request.POST.get('email'))
        notification_id = int(request.POST.get('notification'))
        #widthrow_id = int(request.POST.get('widthrow'))
        tawm = int(request.POST.get('tawm'))
        amount = float(request.POST.get('hmdot'))
        # import pdb; pdb.set_trace()
        userdata = User.objects.get(id = user_id)
        #info = WidthrowInfo.objects.get(id = int(widthrow_id))
        notification = WithdrowNotification.objects.get(id= notification_id)
        wal = TotalAmountReturn.objects.get(id = tawm)

        if wal.total_return >= float(amount):
            wal.total_widthrow = wal.total_widthrow + float(amount)
            wal.total_return = wal.total_return - float(amount)
            wal.save()
            notification.seen = True
            notification.send = True
            notification.save()
        else:
            notification.status = False
            notification.save()

    notification = WithdrowNotification.objects.filter(Q(send=False) and Q(status = True))[::-1]
    notif = WithdrowNotification.objects.get(id = n)
    user = User.objects.get(id = notif.user.id)
    tar = TotalAmountReturn.objects.get(user=user)
    data_new = {
        'user': user,
        'notification':notif,
        'total_amount_width':tar,
        'widthrow_amount': notif.amount_withdrow,
        'account_number': user.account_number,
        'bank_name': user.bank_name,
        'bank_branch': user.branch,
        'ifsc': user.ifsc_code
    } 
    print(data_new)
    return render(request, 'dashboard/depositeoneuser.html', {'data1':data_new, "noti":notification})
