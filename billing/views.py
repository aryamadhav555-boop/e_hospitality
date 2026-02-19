import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import BillForm
from doctors.models import Doctor
from django.contrib.auth.decorators import login_required
from .models import Bill, Insurance


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_bill(request):

    if request.user.role != "DOCTOR":
        return redirect("doctor/dashboard/")  # change here

    doctor = Doctor.objects.get(user=request.user)

    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.doctor = doctor
            bill.save()
            return redirect("home")
    else:
        form = BillForm()

    return render(request, "billing/create_bill.html", {"form": form})




from django.urls import reverse

@login_required
def pay_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],


        line_items=[ {
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': bill.description,
                },
                'unit_amount': int(bill.amount * 100),
            },
            'quantity': 1,
        }],

        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment_success')
        ) + f"?bill_id={bill.id}&session_id={{CHECKOUT_SESSION_ID}}",

        cancel_url=request.build_absolute_uri(
            reverse('payment_cancel')
        ),
    )

    return redirect(session.url)


def payment_success(request):
    session_id = request.GET.get("session_id")

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        bill_id = request.GET.get("bill_id")
        bill = Bill.objects.get(id=bill_id)
        bill.is_paid = True
        bill.save()

    return render(request, "billing/success.html")



def payment_cancel(request):
    return render(request, "billing/cancel.html")

@login_required
def bill_list(request):
    # Show only bills of logged-in user
    bills = Bill.objects.filter(patient=request.user)

    return render(request, "billing/list.html", {
        "bills": bills
    })



@login_required
def billing_dashboard(request):
    bills = Bill.objects.filter(patient__user=request.user)
    insurance = Insurance.objects.filter(patient__user=request.user).first()

    return render(request, "billing/dashboard.html", {
        "bills": bills,
        "insurance": insurance
    })

