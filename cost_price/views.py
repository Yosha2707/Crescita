from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def index(request):
    return render(request, 'cost/cost.html')

def ping(request):
    return render(request, 'cost/price.html')
