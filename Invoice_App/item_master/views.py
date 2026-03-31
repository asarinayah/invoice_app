from django.shortcuts import render
from .models import ItemMaster

# Create your views here.
def newitem(request):
    if request.method=='POST':
        item=ItemMaster.objects.create(
            company=request.user.profile,
        item_name=request.POST["item_name"],
        brand=request.POST["Brand"],
        category=request.POST["category"],
        description=request.POST["description"],
        unit_price=request.POST["unit_price"],
        )
    return render(request,'item_master/new_item.html')

def item_list(request):
    list=ItemMaster.objects.filter(company=request.user.profile)
    return render(request,'item_master/item_list.html',{'items':list})