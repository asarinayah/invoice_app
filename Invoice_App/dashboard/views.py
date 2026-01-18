from django.shortcuts import render
from invoice.models  import Invoice,Company
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
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
def dashboard(request):
    company=request.user.profile.company
    total_invoices = Invoice.objects.filter(company=company).count()
    today_invoices = Invoice.objects.filter(company=company,
        date_created__date=timezone.now().date()
    ).count()
    today=timezone.localdate()
    total_amount = Invoice.objects.filter(company=company,date_created__date=today).aggregate(
        total=Sum('amount_due')
    )['total'] or 0
    formatted_total_amount = round(total_amount, 2)

    context = {
        'total_invoices': total_invoices,
        'today_invoices': today_invoices,
        'formatted_total_amount': formatted_total_amount,
    }

    return render(request, 'dashboard.html', context)
