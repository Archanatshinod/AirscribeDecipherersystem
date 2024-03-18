from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Login,User,Review
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.
###landing page###
def landing(request):
    return render(request,'landing_page.html')

def logins(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            data = Login.objects.get(Username=username,Password=password)
            if data is not None:
                request.session['id'] = data.id
                if data.Type=='Admin':
                    return redirect(admin_home)
                elif data.Type=='User' and data.Status=='Accepted':
                    return redirect(user_home)
                else:
                   return render(request, 'login.html',{'error':'Wait for Admin approvel'})

            else:
                return render(request, 'login.html',{'error':'invalid credentials'})
        except Exception as e:
            return render(request, 'login.html',{'error':e})
    else:
        return render(request,'login.html')
    

def logout(request):
    # if 'id' in request.session:
        request.session.flush()
        return redirect(landing)
    # else:
    #     return HttpResponse("logout")

def user_registeration(request):
    if request.method=='POST':
        Name=request.POST['Name']
        Email=request.POST['Email']
        if Login.objects.filter(Username=Email):
            return render(request,'user_registeration.html',{'x':'Email already Exist!!!'})
        Phone=request.POST['Phone']
        Dob=request.POST['Dob']
        Gender=request.POST['gender']
        Password=request.POST['Password']
        Confirm_password=request.POST['Confirm_password']

        if Password!=Confirm_password:
            return render(request,'user_registeration.html',{'x':'Password not matching!!!'})
        data1=Login.objects.create(Username=Email,Password=Password,Type='User')
        data1.save()

        data2=User.objects.create(login=data1,
                                Name=Name,
                                Email=Email,
                                Phone=Phone,
                                Dob=Dob,
                                Gender=Gender,
                                Password=Password,
                                Confirm_password=Confirm_password
                                )
        data2.save()
        return render(request,'login.html')
    else:
        return render(request,'user_registeration.html')
    
####ADMIN####

def admin_home(request):
    return render(request,'admin_home.html')

def view_users(request):
    data1=User.objects.filter(login__Status="Accepted")
    return render(request,'view_users.html',{'data':data1})

def verify_users(request):
    data=User.objects.all()
    return render(request,'verify_user.html',{'data':data})



def user_status(request,id):
    data=Login.objects.get(id=id)
    if request.method=='POST':
        data1=request.POST['Status']
        if data1=='Accepted':
            data.Status='Accepted'
        elif data1=='Rejected':
           data.Status='Rejected'
        data.save() 
    return redirect(verify_users)

def change_password(request):
    data=request.session['id']
    data1=Login.objects.get(id=data)
    if request.method=='POST':
        newpwd=request.POST['newpwd']
        confpwd=request.POST['confpwd']
        if newpwd!=confpwd:
                return render(request,'change_password.html',{'x':'Password not matching!!!'})
        else:
            data1.Password=newpwd
            data1.save()
            return render(request,'change_password.html',{'x':'Password Successfully changed'})
    else:
        return render(request,'change_password.html')


def view_review(request):
    content=Review.objects.all()
    items_per_page = 10
    paginator = Paginator(content, items_per_page)
    page = request.GET.get('page', 1)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return render(request,'view_review.html',{'data':data})




    
####user


def user_home(request):
    return render(request,'user_home.html')


def view_profile(request):
    data=request.session['id']
    data1=Login.objects.get(id=data)
    data2=User.objects.get(login=data1.id)
    return render(request,'view_profile.html',{'data2':data2})

def edit_profile(request,id):
    data=User.objects.get(id=id)
    if request.method=='POST':
        data.Name=request.POST['Name']
        data.Phone=request.POST['Phone']
        data.Dob=request.POST['Dob']
        data.Gender=request.POST['gender']
        data.save()
        return redirect(view_profile)
    else:
        return render(request,'edit_profile.html',{'data':data})
    

def rating(request):
    return render(request,'rating.html')   

def changepassword_user(request):
    data=request.session['id']
    data1=Login.objects.get(id=data)
    data2=User.objects.get(login=data1.id)
    if request.method=="POST":
        newpwd=request.POST['newpwd']
        confpwd=request.POST['confpwd']
        if newpwd!=confpwd:
            return render(request,'change_password.html',{'x':'Password not matching!!!'})
        else:
            data1.Password=newpwd
            data1.save()
            data2.Password=newpwd
            data2.Confirm_password=confpwd
            data2.save()
    return render(request,'changepassword_user.html')

def user_view_review(request):
    data=request.session['id']
    data1=Login.objects.get(id=data)
    data2=User.objects.get(login=data1.id)
    content=Review.objects.all()
    items_per_page = 1
    paginator = Paginator(content, items_per_page)
    page = request.GET.get('page', 1)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    if request.method=="POST":
        review=request.POST['review']
        rating=request.POST['rating']
        data3=Review.objects.create(user_id=data2,review=review,rating=rating)
        data3.save()
        return render(request,'user_view_review.html',{'message':'Review/Rating added successfully!!!','reviews':data})
    else:
        return render(request,'user_view_review.html',{'reviews':data})





