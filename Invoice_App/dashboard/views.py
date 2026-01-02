from django.shortcuts import render
from invoice.models  import Invoice
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    total_invoices = Invoice.objects.count()
    today_invoices = Invoice.objects.filter(
        date_created__date=timezone.now().date()
    ).count()
    today=timezone.localdate()
    total_amount = Invoice.objects.filter(date_created__date=today).aggregate(
        total=Sum('amount_due')
    )['total'] or 0
    formatted_total_amount = round(total_amount, 2)

    context = {
        'total_invoices': total_invoices,
        'today_invoices': today_invoices,
        'formatted_total_amount': formatted_total_amount,
    }

    return render(request, 'dashboard.html', context)
