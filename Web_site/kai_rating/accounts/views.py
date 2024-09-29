from django.shortcuts import render
from django.http import HttpResponse

from . import db





# Create your views here.
def profile(request):
    user = request.user
    context ={
        'user':user
    }

    return render(request, 'accounts/profile.html',context)

def reg(request):
    is_same = False
    
    if request.method == 'POST':
        req = request.POST
        if req['password']==req['confirm-password']:
            db.user_to_db(req['username'],req['password'])
            return HttpResponse('регистрация выполнена')
        else:
            is_same = True
            context={
                'flag':is_same
            }
            return render(request, 'accounts/registr.html',context)
    else:
        return render(request, 'accounts/registr.html')

            

        
        
    