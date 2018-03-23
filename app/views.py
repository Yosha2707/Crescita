"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from manufacturing_cost_master.models import cost, costpack
from mode_master.models import head
from . models import profit
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import csv
from django.db import connection
from django.http import HttpResponse
import os.path
import sys
from wsgiref.util import FileWrapper

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


@login_required(login_url="/login/")
def users(request):
    users = User.objects.all()
    context = {'users' : users}
    return render(request, 'app/user.html', context)

def add(request):
    return render(request, 'app/add.html')

def create(request):
    if(request.POST.get('is_active') == 'on'):
        isActive = True
    else:
        isActive = False
    member = User.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], email=request.POST['email'], password=request.POST['password'], is_active=isActive)
    return redirect('/')

@login_required(login_url="/login/")
def import_file(request):
    reader = csv.reader(open("C:/Users/user1/Desktop/import-test.csv"), dialect='excel', delimiter=",")
    
    for row in reader:
        firstName=row[0]
        lastName=row[1]
        userName=row[2]
        passwordText=row[3]
        emailText=row[4]
        User.objects.get_or_create(first_name=firstName, last_name=lastName, username=userName, password=passwordText, email=emailText)
    return redirect('/')
    
def profit_master(request):
   
    return render(request, 'app/profit.html')

def import_profit(request):
    if profit.objects.count()>0:
        profit.objects.all().delete()


    if profit.objects.count()==0:
        if request.method == 'POST' and request.FILES['myfile']: 
            myfile = request.FILES['myfile']
            pl_sheet = request.POST.get("pl_sheet")
            start = request.POST.get("start")
            end = request.POST.get("end")
            fs = FileSystemStorage()
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename) 
            reader = csv.reader(open(BASE_DIR + uploaded_file_url), dialect='excel', delimiter=",") 
            
            count = 0
            b = 0
            for row in reader:
                if count==0:
                    count=1
                    continue
                productCode  = row[0]
                quantitySold = row[1]
                effectiveRate = row[2]
                b = b + int(effectiveRate)
                value = row[3]
                member = profit(product_code=productCode,
                                quantity_sold=quantitySold,
                                effective_rate = effectiveRate,
                                value=value,
                                pl_sheet=pl_sheet,
                                start_date=start,
                                end_date=end
                    )
                member.save()

            cursor = connection.cursor()
            cursor.execute("SELECT a.pl_sheet, a.start_date, a.end_date,substr(mcp.product_code,0, instr(mcp.product_code, '-')) as brand,mcp.product_name, mcp.product_code, mcp.factory_name,mcp.margin_per, mcp.margin_amount,a.quantity_sold, a.effective_rate, a.value,round(a.quantity_sold*(((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc) +  (mode_master_head.factory*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+  table_pack.fpc)/100) + (mcp.overall_wastage*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100))) *mcp.rawmultiplier)+ table_pack.fpc)/100)) ,4) as effectiveCost,round(a.value-(a.quantity_sold*(((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc) +  (mode_master_head.factory*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+  table_pack.fpc)/100) + (mcp.overall_wastage*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100))) *mcp.rawmultiplier)+ table_pack.fpc)/100))) ,4) as profit, ROUND(((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc) +  (mode_master_head.factory*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+  table_pack.fpc)/100) + (mcp.overall_wastage*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100))) *mcp.rawmultiplier)+ table_pack.fpc)/100),4) as totalcost, ROUND((mcp.margin_amount + ((((mcp.rawmultiplier*rpm.cost_price) /(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc) + (mode_master_head.factory* ((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+ table_pack.fpc)/100) +  (mcp.overall_wastage*((((mcp.rawmultiplier*rpm.cost_price)/(mcp.rawmultiplier-(mcp.wastage*mcp.rawmultiplier/100)))*mcp.rawmultiplier)+  table_pack.fpc)/100)), 4) as dealerprice fROM manufacturing_cost_master_cost as mcp inner join raw_packing_master_raw as rpm  on mcp.raw_id = rpm.id inner join mode_master_head inner join app_profit as a on mcp.product_code=a.product_code left join (SELECT cost_id , ifnull(SUM(rpm.cost_price*mccp.multipliar), 0) as fpc from  manufacturing_cost_master_costpack as mccp left join raw_packing_master_raw as rpm on mccp.packing_id = rpm.id group by mccp.cost_id) as table_pack on table_pack.cost_id=mcp.id")
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            a = 0
            c = 0
            d = 0
            for ro in results:
                a = a + ro["dealerprice"]
                c = c + ro["margin_amount"]
                d = d + ro["profit"]
            context = {'results':results , 'b':b, 'a':a, 'c':c, 'd':d}
        return render(request, 'app/profit.html', context)


def export(request):
    myc = "mycsv.csv"
    if os.path.isfile(myc):
        os.remove(myc)
    pl_sheet = request.POST.get("pl_sheet")
    start = request.POST.get("start")
    end = request.POST.get("end")    
    brand = request.POST.getlist('brand[]')
    productC = request.POST.getlist('productC[]')
    productN = request.POST.getlist('productN[]')
    factoryN = request.POST.getlist('factoryN[]')
    quantityS = request.POST.getlist('quantityS[]')
    totalC = request.POST.getlist('totalC[]')
    effectiveC = request.POST.getlist('effectiveC[]')
    effectiveR = request.POST.getlist('effectiveR[]')
    vaL = request.POST.getlist('vaL[]')
    dealerP = request.POST.getlist('dealerP[]')
    marginP = request.POST.getlist('marginP[]')
    marginA = request.POST.getlist('marginA[]')
    profit = request.POST.getlist('profit[]')
    totalER = request.POST.getlist('totalER[]')
    totalDP = request.POST.getlist('totalDP[]')
    totalMA = request.POST.getlist('totalMA[]')
    totalP = request.POST.getlist('totalP[]')
    other = request.POST.getlist('other[]')
    otherE = request.POST.getlist('otherE[]')
    totalotherE = request.POST.getlist('totalotherE[]')
    netP = request.POST.getlist('netP[]')
    csvd =zip(brand, productC, productN, factoryN ,quantityS, totalC, effectiveC, effectiveR, vaL, dealerP, marginP, marginA ,profit)
   
    with open('mycsv.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['Brand Code', 'Product Code', 'Product Name', 'Factory Name', 'Quantity Sold', 'Cost Price', 'Effective Cost', 'Effective Rate', 'Value', 'Dealer Price', 'Margin %', 'Margin In Amount', 'Profit'])
        
        q = []
        for r in csvd:
            print(r)
            q.append(r)
        print(q)
        writer.writerows(q)
    return Next(writer)

def Next(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename =  BASE_DIR + '\\'+ 'mycsv.csv'
    download_name ="Profit_Loss.csv"
    wrapper      = FileWrapper(open(filename))
    response     = HttpResponse(wrapper,content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response