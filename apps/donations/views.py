from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from adieulane.flutterwave import FLUTTERWAVE_SECRET_KEY
from adieulane.utils import create_sub_account, get_bank_detail
from apps.donations.models import Donation, DonationAccount
from apps.memorials.models import BurialMemory


class DonationAccountCreateView(View):
    def post(self, request, slug):
        memorial = BurialMemory.objects.get(slug=slug)
        bank_country = self.request.user.profile.country
        account_bank = request.POST.get("account_bank")
        account_number = request.POST.get("account_number")
        routing_number = request.POST.get("routing_number")
        swift_code = request.POST.get("swift_code")
        branch_code = request.POST.get("branch_code")

        # List and get bank code of any given country...
        get_bank_code = get_bank_detail(
            bank_country,
            account_bank,
            FLUTTERWAVE_SECRET_KEY
        )
        print(f"get_bank_code() ==> Executed! \n {get_bank_code}")

        # Create sub_account
        sub_account = create_sub_account(
            get_bank_code["code"],
            account_number,
            memorial.user.get_short_name,
            memorial.user.email,
            memorial.user.get_full_name,
            memorial.user.profile.phone,
            memorial.user.profile.phone,
            memorial.user.profile.country,
            0.05,
            routing_number,
            swift_code,
            branch_code,
            FLUTTERWAVE_SECRET_KEY,
        )

        # Create DonationAccount()
        if sub_account["status"] == "success":
            donation = DonationAccount.objects.filter(burial_memory=memorial).update(
                account_name=sub_account["data"]["full_name"],
                bank_account_number=sub_account["data"]["account_number"],
                bank_code=sub_account["data"]["account_bank"],
                bank_name=sub_account["data"]["bank_name"],
                sub_account_id=sub_account["data"]["subaccount_id"],
                split_type=sub_account["data"]["split_type"],
                split_value=sub_account["data"]["split_value"],
            )
            messages.success(request, "Account added successfully")
            return redirect("memorials:detail", memorial.slug)
            # return JsonResponse({'account_success': 'Account added successfully'}, status=200)
        messages.warning(request, "Account was not added please check your network and try again")
        return redirect("memorials:detail", memorial.slug)
        # return JsonResponse({'account_error': 'Account was not added please check your network and try again'},
        # status=400)


def add_donation(request, slug):
    get_memory = get_object_or_404(BurialMemory, slug=slug)
    get_name = request.POST.get('name')
    get_tx_ref = request.POST.get('tx_ref')
    get_amount = request.POST.get('amount')
    get_status = request.POST.get('status')
    donation = Donation.objects.create(
        burial_memory=get_memory,
        donor_fullname=get_name,
        status=get_status,
        trans_ref=get_tx_ref,
        amount=get_amount,
    )
    get_memory.donations.add(donation)
    messages.success(request, "Donation added successfully")
    return render(request, "donations/donation_list.html")


def list_donations(request, slug):
    get_memory = get_object_or_404(BurialMemory, slug=slug)
    donations = get_memory.donations.all()
    return render(request, "donations/donation_list.html", {'donations': donations})
