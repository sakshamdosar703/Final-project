from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.db import connection
import datetime


# Create your views here.
def home(req):
    cdata = category.objects.all().order_by('-id')[0:5]
    pdata = product.objects.all().order_by('-id')[0:12]
    user=req.session.get('userid')
    noofitemsincart = addtocart.objects.filter(userid=user).count()

    return render(req, 'user/index.html', {"data": cdata, "proddata": pdata, "noofitemsincart": noofitemsincart})


def services(req):
    return render(req, 'user/services.html')


def contactus(req):
    displaydata = False
    if req.method == 'POST':
        Name = req.POST.get("name", "")
        Mobile = req.POST.get("mobile", "")
        Email = req.POST.get("email", "")
        Message = req.POST.get("msg", "")
        contact(name=Name, mobile=Mobile, email=Email, msg=Message).save()
        displaydata = True
    return render(req, 'user/contactus.html', {'ds': displaydata})


def about(req):
    return render(req, 'user/about.html')


def prod(req):
    cdata = category.objects.all().order_by('-id')
    x = req.GET.get('abc')

    if x is not None:
        pdata = product.objects.filter(pcategory=x)
    else:
        pdata = product.objects.all().order_by('-id')

    return render(req, 'user/product.html', {"cat": cdata, "proddata": pdata})


def myprofile(req):
    user = req.session.get('userid')
    pdata = sign_up.objects.filter(email=user)

    return render(req, 'user/myprofile.html', {"profile": pdata})


def updateprofile(request):
    user = request.session.get('userid')
    if user:
        if request.method == 'POST':
            Name = request.POST.get("name", "")
            Mobile = request.POST.get("mobile", "")
            Password = request.POST.get("passwd", "")
            DOB = request.POST.get("dob", "")
            Address = request.POST.get("address", "")
            profilepic = request.FILES['userpic']
            sign_up(email=user, name=Name, mobile=Mobile, passwd=Password, dob=DOB, ppic=profilepic,
                    address=Address).save()
            return HttpResponse(
                "<script>alert('Your Profile Updated Successfully...');window.location.href='/user/myprofile/';</script>")

    return render(request, 'user/Updatemyprofile.html')


def myorders(req):
    userid = req.session.get('userid')
    oid = req.GET.get('oid')
    orderdata = ""
    if userid:
        cursor = connection.cursor()
        cursor.execute(
            "select o.*,p.* from user_order o, user_product p where o.pid=p.id and o.userid='" + str(userid) + "'")
        orderdata = cursor.fetchall()
        if oid:
            res = order.objects.filter(id=oid, userid=userid)
            res.delete()
            return HttpResponse(
                "<script>alert('Your order has been cancelled...');window.location.href='/user/myorders/';</script>")
    return render(req, 'user/myorders.html', {"pendingorder": orderdata})


def signup(request):
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Mobile = request.POST.get("mobile", "")
        EMAIL = request.POST.get("email", "")
        Password = request.POST.get("passwd", "")
        DOB = request.POST.get("DOB", "")
        Address = request.POST.get("address", "")
        profilepic = request.FILES['fu']
        d = sign_up.objects.filter(email=EMAIL)

        if d.count() > 0:
            return HttpResponse(
                "<script>alert('You are already registered..');window.location.href='/user/signup/';</script>")
        else:
            sign_up(name=Name, mobile=Mobile, email=EMAIL, passwd=Password, address=Address, ppic=profilepic,
                    dob=DOB).save()
            return HttpResponse(
                "<script>alert('You are registered successfully...');window.location.href='/user/signup';</script>")
        # return HttpResponse("<script>alert('Thanks for signUp...');window.location.href='/user/signup';</script>")
    return render(request, 'user/signup.html')


def signin(req):
    if req.method == 'POST':
        uname = req.POST.get("email", "")
        passwd = req.POST.get("password", "")
        checkuser = sign_up.objects.filter(email=uname, passwd=passwd)
        if (checkuser):
            req.session['userid'] = uname
            return HttpResponse(
                "<script>alert('Logged In Successfully'); window.location.href='/user/signin';</script>")
        else:
            return HttpResponse(
                "<script>alert('Username or Password is incorrect'); window.location.href='/user/signin';</script>")

    return render(req, 'user/signin.html')


def viewdetails(req):
    a = req.GET.get('msg')
    data = product.objects.filter(id=a)
    return render(req, 'user/viewsdetails.html', {"d": data})


def process(request):
    userid = request.session.get('userid')
    pid = request.GET.get('pid')
    btn = request.GET.get('bn')
    if userid is not None:
        if btn == 'cart':
            checkcartitem = addtocart.objects.filter(pid=pid, userid=userid)
            if checkcartitem.count() == 0:
                addtocart(pid=pid, userid=userid, status=True, cdate=datetime.datetime.now()).save()
                return HttpResponse(
                    "<script>alert('You item is successfully added in cart..');window.location.href='/user/home/'</script>")
            else:
                return HttpResponse(
                    "<script>alert('This items is already added in Cart...');window.location.href='/user/home/'</script>")
        elif btn == 'order':
            order(pid=pid, userid=userid, remarks="Pending", status=True, odate=datetime.datetime.now()).save()
            return HttpResponse(
                "<script>alert('Your order have confirmed....');window.location.href='/user/myorders/'</script>")

        elif btn == 'orderfromcart':
            res = addtocart.objects.filter(pid=pid, userid=userid)
            res.delete()
            order(pid=pid, userid=userid, remarks="Pending", status=True, odate=datetime.datetime.now()).save()
            return HttpResponse(
                "<script>alert('Your order have confirmed....');window.location.href='/user/myorders/'</script>")
        return render(request, 'user/process.html', {"alreadylogin": True})
    else:
        return HttpResponse("<script>window.location.href='/user/signin/';</script>")


def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home';</script>")


def cart(req):
    cartdata = ""
    if req.session.get('userid'):
        userid = req.session.get('userid')
        cursor = connection.cursor()
        cursor.execute(
            "select c.*,p.* from user_addtocart c,user_product p where p.id=c.pid and userid='" + str(userid) + "'")
        cartdata = cursor.fetchall()
        pid = req.GET.get('pid')
        if req.GET.get('pid'):
            res = addtocart.objects.filter(id=pid, userid=userid)
            res.delete()
            return HttpResponse(
                "<script>alert('Your product has been removed successfully...');window.location.href='/user/cart/';</script>")

    return render(req, 'user/cart.html', {"cart": cartdata})
