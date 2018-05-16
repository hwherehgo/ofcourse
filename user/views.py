from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
from user.models import User
from user.forms import Userform

def register(request):
    if request.method == 'POST':
        form = Userform(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info')
        else:
            return render(request,'register.html',{'error':form.errors})

    else:
        return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request,'login.html',{'error':'用户不存在'})
        if check_password(password,user.password):
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request,'login.html',{'error':'密码错误'})

    return render(request,'login.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def user_info(request):
    uid = request.session.get('uid')
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return redirect('/user/login/')
    return render(request,'user_info.html',{'user':user})
