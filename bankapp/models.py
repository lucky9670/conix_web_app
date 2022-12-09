from email.policy import default
# import profile
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# from .utils import generate_ref_code
import uuid
import random
# Create your models here.

DEPOSIT = 1
WITHDRAWAL = 2

TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT, 'Deposit'),
    (WITHDRAWAL, 'Withdrawal'),
)
def create_new_ref_number():
    not_unique = True
    try:
        while not_unique:
            unique_ref = "RCT"+str(random.randint(10000000, 99999999))
            if not User.objects.filter(referal_code=unique_ref):
                not_unique = False
        return str(unique_ref)
    except:
        return None

class User(AbstractUser):
    name = models.CharField(max_length=240)
    identity = models.UUIDField(default = uuid.uuid4, unique=True)
    phone = models.CharField(max_length=20)
    aadhar_number = models.CharField(max_length=200)
    pan_number = models.CharField(max_length=200)
    name_as_pan = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=400)
    pan_photo = models.ImageField(upload_to ='pan/')
    branch = models.CharField(max_length=400)
    account_number = models.CharField(max_length=400)
    ifsc_code = models.CharField(max_length=400)
    account_holder = models.CharField(max_length=400)
    upi = models.CharField(max_length=400)
    date_time = models.DateTimeField(auto_now_add=True)
    referal_code = models.CharField(max_length = 15,unique=True,default=create_new_ref_number)
    refered_by = models.CharField(max_length=100)
    mail_varification = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if self.referal_code == '':
    #        referal_code = generate_ref_code() 
    #        self.referal_code = referal_code
    #     super().save(*args, **kwargs)


class Invest(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invest_amount = models.FloatField()
    percentage_amount = models.FloatField()
    total_amount = models.FloatField()
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    txn_id = models.CharField(max_length=120, unique=True)
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    request_data = models.TextField(null=True, blank=True)
    requested_hash = models.TextField(null=True, blank=True)
    response_data = models.TextField(True, blank=True)
    reponse_hash = models.TextField(null=True, blank=True)
    payumoney_id = models.CharField(editable=False, max_length=120)
    transaction_mode = models.CharField(max_length=2, null=True, blank=True)

    over = models.BooleanField(default=False)


class TotalInvest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    status = models.BooleanField(default=True)
    

class Wollate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.CharField(max_length=100, default=0)


class WidthrowInfo(models.Model):
    date = models.DateTimeField()
    last_deposite_time = models.DateTimeField()
    duration_for_one_deposite = models.CharField(max_length=100)
    next_deposite = models.DateTimeField(default=timezone.now)
    no_of_days = models.IntegerField(default = 0)           
    how_much_deposite_one_time = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=10)
    how_many_time_depo = models.IntegerField()
    deposite_number = models.IntegerField()
    total_deposite_amount = models.FloatField()
    invest_amt = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invest = models.ForeignKey(Invest, on_delete=models.CASCADE)
    over = models.BooleanField(default=False)


class TotalAmountReturn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_return = models.FloatField()
    total_widthrow = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class WalletAddress(models.Model):
    wallet_type = (
        (1, 'CPRO'),
    )
    coin = models.IntegerField(choices = wallet_type)
    address = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    total_wallate_amount = models.FloatField()
    user = models.ForeignKey(User,  on_delete=models.CASCADE)

class WalletAmount(models.Model):
    wallet_type = (
        (1, 'CPRO'),
    )
    wallet = models.ForeignKey(WalletAddress, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    coin = models.IntegerField(choices = wallet_type)
    created_at = models.DateTimeField(auto_now_add=True)



class WithdrowNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_withdrow = models.FloatField()
    seen = models.BooleanField(default=False)
    send = models.BooleanField(default= False)
    status = models.BooleanField(default=True)

    
