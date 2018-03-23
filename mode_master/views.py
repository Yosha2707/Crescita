from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import mode, head 
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import csv



@login_required(login_url="/login/")
def index(request):
    members = mode.objects.all().order_by('-created_date')
    member = head.objects.all()
    context = {'members': members, 'member': member}
    return render(request, 'crud/index.html', context)

def create(request):
    member = mode(mode_name=request.POST['mode_name'])
    member.save()
    return redirect('/mode_master')


def edit(request, id):
    members = mode.objects.get(id=id)
    context = {'members': members}
    return render(request, 'crud/edit.html', context)


def update(request, id):
    member = mode.objects.get(id=id)
    member.mode_name = request.POST.get('mode_name')
    member.save()
    return redirect('/mode_master')

def delete(request, id):
    member = mode.objects.get(id=id)
    member.delete()
    return redirect('/mode_master')


def change(request):
    if head.objects.count()==0:
        member = head(factory=request.POST['factory'])
        print(request.POST)
   
    if head.objects.count()>0:
       member = head.objects.get(id=1)
       member.factory = request.POST.get('factory')

    if not request.POST['factory']:
        member.factory = 0;

    member.save()
    return redirect('/mode_master')

def import_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        reader = csv.reader(open(BASE_DIR + uploaded_file_url), dialect='excel', delimiter=",")
        count=0
        for row in reader:
            if count==0 :
                count=1
                continue

            mode_name=row[0]
            oo= mode(mode_name=mode_name)
            oo.save()
           
    return redirect('/mode_master')
   



