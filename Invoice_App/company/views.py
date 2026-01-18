# company/views.py
from django.shortcuts import render, redirect
from .models import Company

def create_company(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone_number = request.POST["phone_number"]
        address = request.POST["address"]

        company = Company.objects.create(
            name=name,
            phone_number=phone_number,
            address=address
        )

        # Optionally assign company to the logged-in user's profile
        if hasattr(request.user, 'profile'):
            request.user.profile.company = company
            request.user.profile.save()

        return redirect('company_list')  # or wherever you want

    return render(request, 'company/company_form.html')


def company_list(request):
    profile = request.user.profile

    if not profile.company:
        return redirect('create_company')

    return render(request, 'company/company_list.html', {
        'company': profile.company
    })
