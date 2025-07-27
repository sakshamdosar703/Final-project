from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(contact)

class sign_upAdmin(admin.ModelAdmin):
    list_display = ('name','mobile','email','passwd','ppic','address','dob')
admin.site.register(sign_up,sign_upAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cname', 'cdate', 'cpic')
admin.site.register(category,categoryAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ('id','name','ppic','color','tprice','disprice','pdes','pdate','pcategory')
admin.site.register(product,productAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display = ('id','pid','userid','remarks','status','odate')
admin.site.register(order,orderAdmin)

class addtocartAdmin(admin.ModelAdmin):
    list_display = ('id','pid','userid','status','cdate')
admin.site.register(addtocart,addtocartAdmin)