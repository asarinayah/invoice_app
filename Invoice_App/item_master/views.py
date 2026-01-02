from django.shortcuts import render,redirect
from .models import new_item
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404

# Create your views here.
def add_item(request):
    if request.method == 'POST':
        tyre = request.POST.get('tyre')
        tube = request.POST.get('tube')
        tyre_valve = request.POST.get('tyre_valve')
        stock_quantity = request.POST.get('stock_quantity', 0)

        new_item.objects.create(
            tyre=tyre,
            tube=tube,
            tyre_valve=tyre_valve,
            stock_quantity=stock_quantity
        )

        return redirect('item_list')

    return render(request, 'add_item.html')
