# invoices/views.py
from django.shortcuts import render
from .models import Invoice
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from functools import wraps
from django.shortcuts import redirect



def company_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper

@company_required
def create_invoice(request):
    if request.method == "POST":
        invoice=Invoice.objects.create(
            company=request.user.profile.company,  # automatically link company
            customer_name=request.POST["customer_name"],
            phone_number=request.POST["phone_number"],
            service_description=request.POST["service_description"],
            amount_due=request.POST["amount_due"],
            discount=request.POST.get("discount", 0),
            tax=request.POST.get("tax", 0)
        )
        
        # Render the invoice as a PDF (optional)
        return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})

    return render(request, 'invoices/create_invoice.html')

@company_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice,id=invoice_id,company=request.user.profile.company)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})


@company_required
def invoice_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    query = request.GET.get('q')
    company = request.user.profile.company
    invoices = Invoice.objects.filter(company=company).order_by('-date_created') 
    ###company=company LEFT SIDE company indicates field mentioned in Invoice models
    ###RIGHT SIDE company indicated the variable in your view (company = request.user.profile.company)

    if start_date and end_date:
        invoices = invoices.filter(
            date_created__date__range=[start_date, end_date]
        )
    if query:
        # Search by phone_number (partial match) or customer_name (partial match)
        invoices = invoices.filter(
            Q(phone_number__icontains=query) |
            Q(customer_name__icontains=query)
        )

    return render(request, 'invoices/invoice_list.html', {
        'invoices': invoices,'query': query
    })

