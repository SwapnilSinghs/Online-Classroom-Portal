from django.shortcuts import render

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
    return render(request, 'ocp_app/signUpStud.html')