from django.contrib import admin
from .models import Invest, TotalAmountReturn, TotalInvest, User, WalletAddress, WalletAmount, WidthrowInfo, WithdrowNotification, Wollate

# Register your models here.

admin.site.register(User)
admin.site.register(Invest)
admin.site.register(Wollate)
admin.site.register(WidthrowInfo)
admin.site.register(WalletAddress)
admin.site.register(WalletAmount)
admin.site.register(TotalInvest)
admin.site.register(TotalAmountReturn)
admin.site.register(WithdrowNotification)
