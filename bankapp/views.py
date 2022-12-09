import imp
from django.shortcuts import render, redirect, HttpResponse
from .models import User,Invest, WithdrowNotification, Wollate, WidthrowInfo, WalletAddress, WalletAmount, TotalInvest, TotalAmountReturn
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import razorpay
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone
# from datetime import datetime, timedelta, timezone, tzinfo
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from .currency_convertor import CurrencyRates
from paywix.payu import Payu
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pandas as pd

# Create your views here.


payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

payu = Payu(merchant_key, merchant_salt, surl, furl, mode)



def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login')
def user_dashboard(request):
    
    ia = 0.0
    ta = 0.0
    pa = 0.0
    
    return_amount = 0.0
    convertor = CurrencyRates()
    
    notification = WithdrowNotification.objects.filter(Q(send=False) and Q(status = True))[::-1]
    try:
        inve = Invest.objects.filter(user = request.user)
        user1 = User.objects.get(id=request.user.id)
        print()
        print("==================================")
        print(user1.last_login)
        # date = "2020-08-17"
        

        # import pdb; pdb.set_trace()
        for inv in inve:
            ia += float(inv.invest_amount)
            ta += float(inv.total_amount)
            pa += float(inv.percentage_amount)
            wid = WidthrowInfo.objects.get(Q(user = request.user) and Q(invest=inv))
            
            try:
                if wid.invest.payment_status==1 and wid.invest.transaction_type==1:
                    if wid.next_deposite.replace(tzinfo=None) <= datetime.now():
                        last_date = wid.next_deposite
                        while(last_date.replace(tzinfo=None) <= datetime.now()):
                            res=len(pd.bdate_range(last_date,last_date))
                            if res == 0 :
                                print("This is weekend")
                            else:
                                wid.no_of_days = wid.no_of_days + 1
                                wid.save()
                            last_date=last_date+relativedelta(days=1)
                        else:
                            wid.next_deposite = datetime.now() + relativedelta(days=1)
                else:
                    print("Data is Null")
                # if wid.invest.payment_status==1 and wid.invest.transaction_type==1:
                #     if wid.next_deposite.replace(tzinfo=None) <= datetime.now():
                #         wid.next_deposite = datetime.now() + relativedelta(months=1)
                #         wid.how_many_time_depo = int(wid.how_many_time_depo)-1
                #         wid.deposite_number = int(wid.deposite_number)+1
                #         wid.save()
                #         total_amount.total_return = float(total_amount.total_return) + float(wid.how_much_deposite_one_time)
                #         total_amount.save()
                #     else:
                #         print("Data is Null")
                new_amount1 = TotalAmountReturn.objects.get(user=request.user)
                if wid.no_of_days == 40:
                   new_amount1.total_return += inv.percentage_amount *20/100
                   new_amount1.save()
                if wid.no_of_days == 80:
                   new_amount1.total_return += inv.percentage_amount *30/100
                   new_amount1.save()
                if wid.no_of_days == 120:
                   new_amount1.total_return += inv.percentage_amount *40/100
                   new_amount1.save()
                if wid.no_of_days == 160:
                   new_amount1.total_return += inv.percentage_amount *60/100
                   new_amount1.save()
                if wid.no_of_days == 200:
                   new_amount1.total_return += inv.percentage_amount *80/100
                   new_amount1.save()
                   inv.over = True
                   inv.save()
                   wid.over = True
                   wid.save()
            except:
                pass
            return_amount += float(wid.deposite_number)*float(wid.how_much_deposite_one_time)
        
        new_amount = TotalAmountReturn.objects.get(user=request.user)
        new = {
            "invested_amount": round(convertor.get_rate('INR','USD',ia)),
            "total_amount": round(convertor.get_rate('INR','USD',ta)),
            "percentage_amount": round(convertor.get_rate('INR','USD',pa)),
            "return_amount": round(convertor.get_rate('INR','USD',new_amount.total_return)),
            "return_receive": round(convertor.get_rate('INR','USD',(float(new_amount.total_return)+float(new_amount.total_widthrow)))),
            "widthrow_amount": round(convertor.get_rate('INR','USD',new_amount.total_widthrow)),
            "remain": round(convertor.get_rate('INR','USD',(float(ta)-(float(new_amount.total_return)+float(new_amount.total_widthrow))))),
        }
        
    except:
        new = {
                "invested_amount": 0.0,
                "total_amount": 0.0,
                "percentage_amount": 0.0,
                "return_amount": 0.0,
                "return_receive": 0.0,
                "widthrow_amount": 0.0
            }
        
    return render(request, 'dashboard/index.html', {"data":new, "noti":notification})


def registration(request):
    if request.method == "POST":
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        referal = request.POST.get('referal_code')
        bank_name = request.POST.get('bank_name')
        aadhar_number = request.POST.get('aadhar_number')
        pan_number = request.POST.get('pan_number')
        name_as_pan = request.POST.get('name_as_pan')
        branch = request.POST.get('branch')
        account1 = request.POST.get('account1')
        account2 = request.POST.get('account2')
        ifsc = request.POST.get('ifsc')
        account_holder = request.POST.get('account_holder')
        upi = request.POST.get('upi_id')
        print('')
        print(name, email,phone, pass1, pass2, referal, bank_name, aadhar_number, pan_number, name_as_pan, branch, account1, account2, ifsc, account_holder, upi)
        print('')
        try:
            refered = User.objects.get(referal_code = referal)
            print(refered)
        except:
            refered = 0
            print('Your Referal code does not exist for any user')
        
        if pass1 == pass2:
            if refered != 0:
                try:
                    User.objects.get(email = email)
                    return render (request,'register.html', {'error':'Username is already taken!'})
                except User.DoesNotExist:
                    user = User.objects.create_user(username= email,email = email,name=name,phone=phone, password=pass1, refered_by=referal,
                        bank_name = bank_name, aadhar_number = aadhar_number, pan_number = pan_number, name_as_pan = name_as_pan,
                        branch = branch, account_number = account1, ifsc_code = ifsc, account_holder = account_holder, upi = upi)
                    auth.login(request,user)
                    point1 = Wollate.objects.get_or_create(user = refered)
                   
                    new_point = int(point1[0].point)+50
                    point1[0].point = new_point
                    point1[0].save()
                    return redirect(user_dashboard)
            else:
                return render (request,'register.html', {'error':'Referal Code Does Not exist!'})
        else:
            return render (request,'register.html', {'error':'Password does not match!'})
    else:
        return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST.get('email'),password = request.POST.get('password'))
        if user is not None:
            auth.login(request,user)
            return redirect(user_dashboard)
        else:
            return render (request,'auth_login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'auth_login.html')


@login_required(login_url='/login')
def logout1(request):
    auth.logout(request)
    return redirect(index)


@login_required(login_url='/login')
def update_profile(request, n):
    if request.method == "POST":
        print(n)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bank_name = request.POST.get('bank_name')
        aadhar_number = request.POST.get('aadhar_number')
        pan_number = request.POST.get('pan_number')
        name_as_pan = request.POST.get('name_as_pan')
        branch = request.POST.get('branch')
        account1 = request.POST.get('account1')
        account2 = request.POST.get('account2')
        ifsc = request.POST.get('ifsc')
        account_holder = request.POST.get('account_holder')
        if account1 == account2:
            user = User.objects.get(id = n)   
            user.name = name        
            user.phone = phone        
            user.email = email        
            user.aadhar_number = aadhar_number        
            user.pan_number = pan_number        
            user.name_as_pan = name_as_pan        
            user.bank_name = bank_name       
            user.branch = branch       
            user.account_number = account1        
            user.ifsc_code = ifsc
            user.account_holder = account_holder
            user.save()   
            return redirect(user_dashboard)
        else:
            return render (request,'user_update.html', {'error':'Account does not match !'})
    else:
        user = User.objects.get(id = n)
        return render(request,'user_update.html',{'user':user})

from django.contrib.sites.shortcuts import get_current_site

# @login_required(login_url='/login')
# def invest(request):
#     if request.method == "POST":
#         amount = float(request.POST.get('amount'))
#         client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
#         c = CurrencyRates()
#         amt = round(c.get_rate('USD','INR',amount))
        
#         print(amt)
#         order = Invest.objects.create(user = request.user, invest_amount = 0, percentage_amount=0, transaction_type=1, total_amount=0)
#         try:
#             tinv = TotalInvest.objects.filter(user = request.user).count()
#         except:
#             tinv = 0

#         if tinv ==0:
#             TotalInvest.objects.create(user = request.user, total_amount=0)
#         else:
#             pass
#         order_currency = 'INR'
        
#         callback_url = 'https://'+ str(get_current_site(request))+"/handlerequest/"
#         notes = {'order-type': "basic order from the website", 'key':'value'}
#         razorpay_order = client.order.create(dict(amount=amt*100, currency=order_currency, notes = notes, receipt=str(order.id), payment_capture='0'))
#         print(razorpay_order['id'])
#         submit_amount = amount + (amount * 10/100)
#         print(submit_amount)
#         order.razorpay_order_id = razorpay_order['id']
#         order.invest_amount = float(amount)
#         order.percentage_amount = submit_amount
#         order.total_amount = submit_amount
#         order.save()

#         # WidthdrowInfo working

#         date = datetime.now()
#         last_depo_time = date + relativedelta(years=1)
#         dfod = '1 month'
#         hmdot = submit_amount/12
#         hmtd = 12
#         invest = order

#         order = WidthrowInfo.objects.create(date = date, last_deposite_time=last_depo_time, duration_for_one_deposite=dfod, how_much_deposite_one_time=hmdot, how_many_time_depo=hmtd, user = request.user, invest=invest, deposite_number=0, total_deposite_amount=hmdot)
#         try:
#             object = TotalAmountReturn.objects.get(user = request.user)
#         except:
#             object = 0
#         if object == 0:
#             object = TotalAmountReturn.objects.create(user = request.user, total_return=0.0, total_widthrow=0.0)
#         else:
#             pass

#         context = {
#             "api_key" : RAZORPAY_API_KEY,
#             "order_id" : razorpay_order['id'],
#             "name" : request.user.name,
#             "email" : request.user.email,
#             "phone" : request.user.phone,
#             "amount" : amt,
#             'callback_url':callback_url
#         }

#         print(context)

#         return render(request, 'dashboard/checkout.html', context)
#     return render(request, 'dashboard/invest.html')

@csrf_exempt
@login_required(login_url='/login')
def invest(request):

    context = {
            "name" : request.user.name,
            "email" : request.user.email,
            "phone" : request.user.phone,
            "amount" : 0,
            "productinfo": "Invest"
        }

    print(context)

    if request.method == "POST":
        import uuid
        # import pdb;pdb.set_trace()
        amount = float(request.POST.get('amount'))
        data = {k: v[0] for k, v in dict(request.POST).items()}
        
        txnid = uuid.uuid1()
        data.pop('csrfmiddlewaretoken')
        data.update({"txnid": txnid})
        payu_data = payu.transaction(**data)

        # client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        # c = CurrencyRates()
        # amt = round(c.get_rate('USD','INR',amount))
        
        print(amount)
        order = Invest.objects.create(user = request.user, invest_amount = 0, percentage_amount=0, transaction_type=1, total_amount=0,txn_id=txnid, request_data=data,
                                                 requested_hash=payu_data.get('hashh'))
        try:
            tinv = TotalInvest.objects.filter(user = request.user).count()
        except:
            tinv = 0

        if tinv ==0:
            TotalInvest.objects.create(user = request.user, total_amount=0)
        else:
            pass
        order_currency = 'INR'
        
        # callback_url = 'https://'+ str(get_current_site(request))+"/handlerequest/"
        # notes = {'order-type': "basic order from the website", 'key':'value'}
        # razorpay_order = client.order.create(dict(amount=amt*100, currency=order_currency, notes = notes, receipt=str(order.id), payment_capture='0'))
        # print(razorpay_order['id'])
        submit_amount = amount 
        print(submit_amount)
        order.invest_amount = float(amount)
        order.percentage_amount = submit_amount + (amount * 300/100)
        order.total_amount = submit_amount
        order.save()

        # WidthdrowInfo working

        date = datetime.now()
        last_depo_time = date + relativedelta(years=1)
        dfod = '1 month'
        hmdot = submit_amount/12
        hmtd = 12
        invest = order

        order = WidthrowInfo.objects.create(date = date, last_deposite_time=last_depo_time, duration_for_one_deposite=dfod, how_much_deposite_one_time=hmdot, how_many_time_depo=hmtd, user = request.user, invest=invest, deposite_number=0, total_deposite_amount=hmdot, invest_amt = submit_amount)
        try:
            object = TotalAmountReturn.objects.get(user = request.user)
        except:
            object = 0
        if object == 0:
            object = TotalAmountReturn.objects.create(user = request.user, total_return=0.0, total_widthrow=0.0)
        else:
            pass

        
        return render(request, 'dashboard/checkout.html', {"posted": payu_data})
    return render(request, 'dashboard/invest.html',  {'posted': context})



# Payu success return page
@csrf_exempt
def payu_success(request):
    import pdb;pdb.set_trace()
    data = {k: v[0] for k, v in dict(request.POST).items()}
    txn_id = data.get('txnid')
    transaction = get_object_or_404(Invest, txn_id=txn_id)
    transaction.response_data = data
    transaction.reponse_hash = data.get('hash')
    transaction.payumoney_id = data.get('payuMoneyId')
    transaction.save()
    response = payu.verify_transaction(data)
    try:
        totalinv = TotalInvest.objects.get(user = transaction.user)
        am = totalinv.total_amount
        totalinv.total_amount = am 
        totalinv.save()

        transaction.payment_status = 1
        transaction.save()


        return render(request, 'dashboard/paymentsuccess.html',{'id':transaction.id})
    except:
        transaction.payment_status = 2
        transaction.save()
        return render(request, 'dashboard/paymentfail.html')
    # return JsonResponse(response)


# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    txn_id = data.get('txnid')
    transaction = get_object_or_404(Invest, txn_id=txn_id)
    response = payu.verify_transaction(data)
    transaction.payment_status = 2
    transaction.save()
    return render(request, 'dashboard/paymentfail.html')



"""
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id','')
        signature = request.POST.get('razorpay_signature','')
        params_dict = { 
        'razorpay_order_id': order_id, 
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
        }
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        try:
            order_db = Invest.objects.get(razorpay_order_id=order_id)
        except:
            return HttpResponse("505 Not Found")
        order_db.razorpay_payment_id = payment_id
        order_db.razorpay_signature = signature
        order_db.save()
        result = client.utility.verify_payment_signature(params_dict)
        if result==True:
            amount1 = order_db.invest_amount #we have to pass in paisa
            c = CurrencyRates()
            amount = round(c.get_rate('USD','INR',amount1))*100
            
            try:
                totalinv = TotalInvest.objects.get(user = order_db.user)
                am = totalinv.total_amount
                totalinv.total_amount = am + float(order_db.percentage_amount)
                totalinv.save()
                client.payment.capture(payment_id, amount)
                order_db.payment_status = 1
                order_db.save()


                return render(request, 'dashboard/paymentsuccess.html',{'id':order_db.id})
            except:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'dashboard/paymentfail.html')
        else:
            order_db.payment_status = 2
            order_db.save()
            return render(request, 'dashboard/paymentfail.html')
"""

@login_required(login_url='/login')
def investdetail(request):
    users = Invest.objects.filter(Q(user = request.user) and Q(payment_status=1))[::-1]
    new_data = []
    for user in users:
        
        contaxt={
            'id': user.id,
            'user':user.user,
            'invest_amount':float(user.invest_amount),
            'percentage_amount': float(user.percentage_amount),
            'total_amount': float(user.total_amount),
            'payment_status':user.payment_status,
            'transaction_type':user.transaction_type,
            'datetime_of_payment':user.datetime_of_payment,
            'created_at':user.created_at,
            'razorpay_order_id':user.payumoney_id,
            'razorpay_payment_id':user.txn_id,
            'razorpay_signature':user.reponse_hash,
            'over':user.over
        }
        new_data.append(contaxt)
    return render(request, 'dashboard/investdetail.html', {'data':new_data})


@login_required(login_url='/login')
def referal(request):
    refered_user = User.objects.filter(refered_by = request.user.referal_code)
    return render(request, 'dashboard/refrel.html', {'data':refered_user})


@login_required(login_url='/login')
def wallet(request):
    try:
        wallet_data = Wollate.objects.get(user = request.user)
    except:
        wallet_data = {'user':request.user, 'point':0}
    return render(request, 'dashboard/wallet.html', {'data':wallet_data})



@login_required(login_url='/login')
def balance(request, n):
    total_balance = 0
    user = User.objects.get(id = n)
    data =  Invest.objects.filter(Q(user = request.user) and Q(payment_status=1))   
    for item in data:
        total_balance = total_balance + float(item.invest_amount) 
    return render(request, 'dashboard/balance.html', {'data':total_balance})



@login_required(login_url='/login')
def trandetail(request):
    user = Invest.objects.filter(Q(user = request.user) and Q(payment_status=2))[::-1]
    return render(request, 'dashboard/transectiondetail.html', {'data':user})



def test(request):
    return render(request, 'dashboard/test.html')


def test1(request):
    return render(request, 'dashboard/userabout.html')

@login_required(login_url='/login')
def walletaddress(request):
    if request.method == 'POST':
        coin = request.POST.get('cars')
        wallet_add = request.POST.get('wallet_add')
        password = request.POST.get('password')
        print(coin, wallet_add, password)
        userdata = User.objects.get(email = request.user)
        if userdata.check_password(password):
            order = WalletAddress.objects.create(coin = coin, address = wallet_add,total_wallate_amount=0.0, user = request.user)
            return render(request,'dashboard/walletaddress.html', {'data':WalletAddress.objects.filter(user = request.user)})
        else:
            return render (request,'dashboard/walletaddress.html', {'error':'Password Does not Match !'})
    else:
        return render(request, 'dashboard/walletaddress.html', {'data':WalletAddress.objects.filter(user = request.user)})



@login_required(login_url='/login')
def userwithdrow(request):
    # import pdb; pdb.set_trace()
    try:
        total_return_user = TotalAmountReturn.objects.get(user = request.user)
    except:
        total_return_user = {
            "user": request.user,
            "total_return": 0.00,
            "total_widthrow": 0.00
        }

    if request.method == "POST":
        
        amount = request.POST.get('amount')
        password = request.POST.get('password')
        # import pdb; pdb.set_trace()
        userdata = User.objects.get(email = request.user)
        wal = TotalAmountReturn.objects.get(user= userdata)

    
        if userdata.check_password(password):
            if wal.total_return >= float(amount):
                order = WithdrowNotification.objects.create(user = request.user, amount_withdrow = float(amount))
                
                # wal.total_widthrow = wal.total_widthrow + float(amount)
                # wal.total_return = wal.total_return - float(amount)
                # wal.save()
                
            return render(request,'dashboard/userwithdrow.html', {'data':total_return_user, "msg": "Request Send to Admin for sending Money"})
        else:
            return render(request,'dashboard/userwithdrow.html', {'error':'Password Does not Match !'})
    # wid = WidthrowInfo.objects.get(user = request.user)
    return render(request, 'dashboard/userwithdrow.html', {"data": total_return_user})


@login_required(login_url='/login')
def withdrowreport(request):
    return render(request, 'dashboard/transectionreport.html')

@login_required(login_url='/login')
def gatewayinvoice(request):
    return render(request, 'dashboard/gatewayinvoice.html')

@login_required(login_url='/login')
def transferutility(request):
    if request.method == 'POST':
        coin = request.POST.get('cars')
        transamount = float(request.POST.get('transamount'))
        password = request.POST.get('password')
        print(coin, transamount, password)
        userdata = User.objects.get(email = request.user)
        inv = TotalInvest.objects.get(user = userdata)
        wal = WalletAddress.objects.get(id = int(coin))
        
        amt = transamount
        print(amt)
        if userdata.check_password(password):
            if inv.total_return >= float(amt):
                order = WalletAmount.objects.create(wallet = wal, user = request.user, amount = float(amt), coin= wal.coin)
                wal.total_wallate_amount = wal.total_wallate_amount + float(amt)
                wal.save()
                inv.total_return = inv.total_return-float(amt)
                inv.save()
            return render(request,'dashboard/transferutility.html', {'new_data':WalletAmount.objects.filter(user = request.user)})
        else:
            return render(request,'dashboard/transferutility.html', {'error':'Password Does not Match !'})
    else:
        new_data = WalletAmount.objects.filter(user = request.user)
        widrow = WalletAddress.objects.filter(user = request.user)
        return render(request, 'dashboard/transferutility.html', {'data':widrow, 'new_data':new_data})

@login_required(login_url='/login')
def transferwallet(request):
    widrow = WalletAddress.objects.filter(user = request.user)
    return render(request, 'dashboard/transferwallet.html', {'data':widrow})

