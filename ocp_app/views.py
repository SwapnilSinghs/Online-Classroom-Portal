from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def signUpStud(request):
    if request.method=="POST":
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        cnfpassword = request.POST.get('confpassword', '')
        signUpStud = SignUpStud(username=username,firstname=firstname,lastname=lastname,email=email,phone=phone,password=password)
        signUpStud.save()
    return render(request, 'ocp_app/signUpStud.html')