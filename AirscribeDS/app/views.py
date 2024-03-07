from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Login,User

# Create your views here.
###landing page###
def landing(request):
    return render(request,'landing_page.html')

def login(request):
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
    data=User.objects.all()
    return render(request,'view_users.html',{'data':data})

def user_status(request,id):
    data=Login.objects.get(id=id)
    if request.method=='POST':
        data1=request.POST['Status']
        if data1=='Accepted':
            data.Status='Accepted'
        elif data1=='Rejected':
           data.Status='Rejected'
        data.save() 
    return redirect(view_users)


###common###
def change_password(request):
    return render(request,'change_password.html')

def changepassword_user(request):
    return render(request,'changepassword_user.html')

def view_review(request):
    return render(request,'view_review.html')

def user_view_review(request):
    return render(request,'user_view_review.html')

    



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







