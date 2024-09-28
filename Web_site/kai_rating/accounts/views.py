from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
def profile(request):
    user = request.user
    context ={
        'user':user
    }

    return render(request, 'accounts/profile.html',context)

def reg(request):
    if request.method == 'POST':
        req = request.POST
        if req['pass1']==req['pass2']:
            User(username = req['user'], password = req['pass1']).save()
            return HttpResponse('регистрация выполнена')
        else:
            return HttpResponse('пароли не совпадают')
    else:
        return render(request, 'accounts/registr.html')

            

        
        
    