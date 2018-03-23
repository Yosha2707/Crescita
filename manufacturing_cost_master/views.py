from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.shortcuts import render_to_response
from raw_packing_master.models import raw
import json
from django.http import HttpResponse
from mode_master.models import head
from . models import cost, costpack
from django.db.models.query import QuerySet
from itertools import chain
import types
from django.db.models import Count
from django.db import connection
from django.urls import reverse
import csv
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages


def add(request):
    member = head.objects.all()
    context = {'member': member}
    return render(request, 'main.html', context)


def get_places(request):
    
    if True:
        q = request.GET.get('q', '')
        places = raw.objects.filter(material_name__icontains=q, material_type='PACKAGING MATERIAL')
        results = []
        for pl in places:
          place_json = { }  
          place_json ['id'] = pl.id
          place_json ['material_name'] = pl.material_name
          place_json ['cost_price'] = pl.cost_price
          results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def my_custom_sql(request):
    cursor = connection.cursor()
    cursor.execute("SELECT mcp.id, mcp.product_name, mcp.product_code, mcp.factory_name, mcp.pack_size, mcp.mrp_per, mcp.mrp_price, mcp.margin_per, mcp.margin_amount, ROUND(((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc) + (mode_master_head.factory*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc)/100) + (mcp.overall_wastage*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc)/100),4) as totalcost, ROUND((mcp.margin_amount + ((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc) + (mode_master_head.factory*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc)/100) + (mcp.overall_wastage*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc)/100)), 4) as dealerprice fROM manufacturing_cost_master_cost as mcp inner join raw_packing_master_raw as rpm on mcp.raw_id = rpm.id inner join mode_master_head left join (SELECT cost_id , ifnull(SUM(rpm.cost_price*mccp.multipliar), 0) as fpc from manufacturing_cost_master_costpack as mccp left join raw_packing_master_raw as rpm on mccp.packing_id = rpm.id group by mccp.cost_id) as table_pack on table_pack.cost_id=mcp.id")
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))

    context = {'results':results}
    return render(request, 'list.html', context)
  

def get_place(request):
    #if request.is_ajax():
    if True:
        q = request.GET.get('q', '')
        places = raw.objects.filter(material_name__icontains=q, material_type='RAW MATERIAL')
        results = []
        for pl in places:
          place_json = { }  
          place_json ['id'] = pl.id
          place_json ['material_name'] = pl.material_name
          place_json ['raw_cost_price'] = pl.cost_price
          results.append(place_json)
        content = json.dumps(results)
    else:
        content = 'fail'
    mimetype = 'application/json'
    return HttpResponse(content, mimetype)

def insert(request):
    co = []
    cop = cost()
    cop.Raw_id = str(request.POST.get('Raw_id'))
    cop.product_name = request.POST.get('product_name')
    cop.product_code = request.POST.get('product_code')
    cop.factory_name = request.POST.get('factory_name')
    cop.pack_size = str(request.POST.get('pack_size'))
    cop.rawmultiplier = str(request.POST.get('rawmultiplier'))
    cop.wastage = str(request.POST.get('wastage'))
    cop.overall_wastage = str(request.POST.get('overall_wastage'))
    cop.margin_per = str(request.POST.get('marginin_per'))
    cop.margin_amount = str(request.POST.get('margin_in_amount'))
    cop.mrp_per = str(request.POST.get('mrp_per'))
    cop.mrp_price = str(request.POST.get('mrp_price'))
    co.append(cop)
    cost.objects.bulk_create(co)
    p = cost.objects.latest('id')
    oo = p.id
    packingId = request.POST.getlist('packing_id[]'),
    multipliarVal = request.POST.getlist('multiplier[]'),
    if len(packingId) > 0:
        packingMaterials = packingId[0]
        packingMultipliars = multipliarVal[0]
    unique = []
    for i in range(len(packingMaterials)):
        cos = costpack()
        cos.packing_id = str(packingMaterials[i])
        cos.multipliar = str(packingMultipliars[i])
        cos.Raw_id = str(packingMaterials[i])
        cos.cost_id = oo
        unique.append(cos)
    costpack.objects.bulk_create(unique)
    return redirect('/manufacturing_cost_master')

def delete(request, id):
    member = cost.objects.filter(id=id)
    members = costpack.objects.filter(cost_id=id)
    member.delete()
    members.delete()
    return redirect('/manufacturing_cost_master')

def edit(request, id):
    a = cost.objects.get(id=id)
    y = a.Raw_id
    b = raw.objects.get(id=y)
    margin_per = a.margin_per
    mrp_per = a.mrp_per
    mrp_price = a.mrp_price
    costPrice = b.cost_price 
    rawMultiplier = a.rawmultiplier
    multI = costPrice*rawMultiplier
    wastagE = a.wastage
    oWastage = a.overall_wastage
    percentage = wastagE*rawMultiplier/100
    sub = rawMultiplier - percentage
    div = round(multI/sub, 4)
    finalR = round(div*rawMultiplier, 4)

    mem = costpack.objects.filter(cost_id=id).values('Raw__cost_price','id', 'multipliar', 'Raw__material_name')
    baba = 0
    final = []
    for m in mem:
        print(m)
        pack = {}
        pack["id"] = m["id"]
        pack["material_name"] = m["Raw__material_name"]
        pack["multipliar"] = m["multipliar"]
        pack["cost_price"] = m["Raw__cost_price"]
        pack["finalpack"] = round(pack["multipliar"]*pack["cost_price"], 4)
        baba = round(baba + pack["finalpack"], 4)
        final.append(pack)
    
    
    totalcost = round(baba+finalR, 4)

    ishu = head.objects.values('factory')
    for i in ishu:
        fact = i["factory"]

    ping = totalcost*oWastage/100
    pong = totalcost*fact/100
    pataka = round(ping+pong+totalcost, 4)
    po = round(margin_per*pataka/100, 4)
    dealerprice = round(po+pataka , 4)
    ek = round(mrp_per*dealerprice/100, 4)
    MRP = round(ek+dealerprice, 4)
    

    context = {'a': a,'b':b, 'baba': baba,'po':po,'MRP':MRP ,'multI': multI,'finalR': finalR, 'div':div,'final': final, 'totalcost':totalcost, 'ishu':ishu, 'oWastage':oWastage, 'pataka':pataka, 'margin_per':margin_per,'dealerprice':dealerprice, 'mrp_per':mrp_per}
    return render(request, 'update.html', context)

def update(request, id):
    member = cost.objects.get(id=id)
    member.rt_id=request.POST.get('rt_id')
    member.Raw_id=request.POST.get('Raw_id')
    member.product_name=request.POST.get('product_name')
    member.product_code=request.POST.get('product_code')
    member.factory_name=request.POST.get('factory_name')
    member.pack_size=request.POST.get('pack_size')
    member.rawmultiplier=request.POST.get('rawmultiplier')
    member.wastage=request.POST.get('wastage')
    member.overall_wastage=request.POST.get('overall_wastage')
    member.margin_per=request.POST.get('marginin_per')
    member.margin_amount=request.POST.get('margin_in_amount')
    member.mrp_per=request.POST.get('mrp_per')
    member.mrp_price=request.POST.get('mrp_price')
    
    member.save()


    a = member.id
    packingId = request.POST.getlist('packing_id[]'),
    if len(packingId) > 0:
        packingMaterials = packingId[0]

    else:
        packingId = 0

    multipliarVal = request.POST.getlist('multiplier[]'),

    if len(multipliarVal) > 0:
        packingMultipliars = multipliarVal[0]

    else:
        multipliarVal = 0
    
    for i in range(len(packingMaterials)):
        packId = packingMaterials[i]
        multiVal = packingMultipliars[i]
        members = costpack(packing_id = packId,Raw_id = packId, multipliar = multiVal, cost_id = a)
        members.save()

    return redirect('/manufacturing_cost_master')
   
def remove(request, id):
    p = costpack.objects.filter(id=id)
    for i in p :
        q = i.cost_id
    par = costpack.objects.get(id=id)
    par.delete()
    return redirect('edit', id=q)

def import_file(request):
    if request.method == 'POST' and request.FILES['myfile']: 
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename) 
        reader = csv.reader(open(BASE_DIR + uploaded_file_url), quotechar='"', delimiter=',') 
        idd = []
        Sfinal = []
        to = []
        unique = []
        rat = [] 
        count = 0
        for row in reader:
            if(row[0]!="PRODUCT NAME"):
                material_name = row[4]
                productCode = row[1]
                try:
                    raws= raw.objects.get(material_name=material_name)
                    Raw_id = raws.id
                except raw.DoesNotExist:
                    raws = None
                    messages.info(request, 'No Such Raw Material' +row[4], extra_tags='alert')
                    pass
                if(raws!=None):
                    t = []
                    t.append(count)
                    t.append(row[1])
                    to.append(t)   
                    
                    r = cost()
                    r.Ki = count
                    r.product_name=row[0]
                    r.product_code=row[1]
                    r.factory_name=row[2]
                    r.pack_size=row[3]
                    r.rawmultiplier=row[6]
                    r.wastage=row[8]
                    r.overall_wastage=row[43]
                    r.margin_per=row[45]
                    r.margin_amount=row[46]
                    r.mrp_per=row[48]
                    r.mrp_price=row[49]
                    r.Raw_id=Raw_id
                    r.rt_id=Raw_id
                    rat.append(r)
                                   
                    i = 10
                    j = 38
                
                    while j > i:
                        pack={}
                        multi = {}
                        if len(row[i]) > 0:
                            pack["material_name"] = row[i]
                            multi = row[i+1]
                            
                            raws = raw.objects.get_or_create(material_name = pack["material_name"],
                                                            defaults = {'mode_id':1,
                                                            'material_type':"PACKAGING MATERIAL",
                                                            'material_name':pack["material_name"],
                                                            'purchase_name':"NoN",
                                                            'purchase_date':str("2018-1-1"),
                                                            'factory_wise_bifercation':str(0),
                                                            'ex_factory_price':str(0),
                                                            'supplier_name':"NON",
                                                            'hsn_code':str(0),
                                                            'gst':str(0),
                                                            'price_after_gst':str(0),
                                                            'freight':str(0),
                                                            'cost_price':str(0),
                                                            'transpoter':"NON"}
                                                             )
                            
                            ro = raw.objects.get(material_name=pack["material_name"])
                            print("chala")
                            uu = ro.id
                            idd.append(uu)
                            Sfinal.append(multi)
                        i += 3
                    
                    if len(idd) > 0:
                        packingMaterials = idd
                        packingMultipliars = Sfinal
                    else:
                        packingMaterials = 0
                    
                    if packingMaterials!=0:
                        
                        for i in range(len(packingMaterials)):
                            packId = packingMaterials[i]
                            multiVal = packingMultipliars[i]
                            o = []
                            o.append(count)
                            o.append(packId)
                            o.append(packId)
                            o.append(multiVal)
                            unique.append(o)

                            
                    count += 1    
                    idd = []
                    Sfinal = []
    

    z = [ ]
    cost.objects.bulk_create(rat)
    for i in to:
       for j in unique:
            if i[0]==j[0]:
                e = cost.objects.get(product_code=i[1])
                ee = e.id
                k = costpack()
                k.cost_id = ee
                k.multipliar = j[3]
                k.Raw_id = j[2]
                k.packing_id = j[2]
                z.append(k)

    costpack.objects.bulk_create(z)
    return redirect('/manufacturing_cost_master')



                                





          
   

    



