from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import raw, mode
from django.db import IntegrityError
import csv
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .models import Document





def index(request):
    raws = raw.objects.values(
        'id',
        'material_type',
        'mode_id',
        'mode__mode_name',
        'material_name', 
        'purchase_name', 
        'purchase_date', 
        'factory_wise_bifercation', 
        'ex_factory_price', 
        'supplier_name', 
        'hsn_code',
        'gst',
        'price_after_gst',
        'transpoter',
        'freight',
        'cost_price',
       
    )
    
    context = {'raws' : raws}
    return render(request, 'index.html', context)

def add(request):
    modes = mode.objects.all()
    context = {'modes': modes}
    return render(request, 'add.html', context)

def insert(request):
    member = raw(mode_id=request.POST.get('mode_id'),
                 material_type=request.POST.get('material_type'),
                 material_name=request.POST.get('material_name'),
                 purchase_name=request.POST.get('purchase_name'),
                 purchase_date=request.POST.get('purchase_date'), 
                 factory_wise_bifercation=request.POST.get('factory_wise_bifercation'),
                 ex_factory_price=request.POST.get('ex_factory_price'),
                 supplier_name=request.POST.get('supplier_name'), 
                 hsn_code=request.POST.get('hsn_code'),
                 price_after_gst=request.POST.get('price_after_gst'),
                 gst=request.POST.get('gst'),
                 transpoter=request.POST.get('transpoter'),
                 freight=request.POST.get('freight'),
                 cost_price=request.POST.get('cost_price'))
    member.save()
    return redirect('/raw_packing_master')

def edit(request, id):
    raws = raw.objects.get(id=id)
    context = {'raws': raws}
    return render(request, 'edit.html', context)

def update(request, id):
    member = raw.objects.get(id=id)
    member.material_type = request.POST.get('material_type')
    member.material_name = request.POST.get('material_name')
    member.purchase_name = request.POST.get('purchase_name')
    member.purchase_date = request.POST.get('purchase_date')
    member.factory_wise_bifercation = request.POST.get('factory_wise_bifercation')
    member.ex_factory_price = request.POST.get('ex_factory_price')
    member.supplier_name = request.POST.get('supplier_name')
    member.hsn_code = request.POST.get('hsn_code')
    member.price_after_excise = request.POST.get('price_after_excise')
    member.gst = request.POST.get('gst')
    member.price_after_gst = request.POST.get('price_after_gst')
    member.transpoter = request.POST.get('transpoter')
    member.freight = request.POST.get('freight')
    member.cost_price = request.POST.get('cost_price')
    member.save()
    return redirect('/raw_packing_master')

def delete(request, id):
    member = raw.objects.get(id=id)
    member.delete()
    return redirect('/raw_packing_master')

def import_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        reader = csv.reader(open(BASE_DIR + uploaded_file_url), dialect='excel', delimiter=",")
        count=0
        yo = []
        for row in reader:
            if count==0 :
                count=1
                continue

            modeName=row[0]
            try:
                modes = mode.objects.get(mode_name=modeName)
            except mode.DoesNotExist:
                modes = None
            if(modes != None):
                y = raw()
                y.mode_id=modes.id
                y.material_type = row[1]
                y.material_name = row[2]
                y.purchase_name = row[3]
                y.purchase_date = row[4]
                y.factory_wise_bifercation = row[5]
                y.ex_factory_price = float(row[6])
                y.supplier_name = row[7]
                y.hsn_code = row[8]
                y.gst = row[9]
                y.price_after_gst = row[10]
                y.transpoter = row[11]
                y.freight = row[12]
                y.cost_price = row[13]
                yo.append(y)
            
            else:
                print("Mode not found")
        raw.objects.bulk_create(yo)
    return redirect('/raw_packing_master')


