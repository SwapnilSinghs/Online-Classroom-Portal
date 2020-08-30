from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'ocp_app/index.html')