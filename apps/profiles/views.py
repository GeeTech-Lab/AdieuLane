import json
from currencies.models import Currency
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View

from adieulane.utils import get_phone_country
from apps.profiles.models import Profile
from apps.wallets.models import Wallet


def check_phone(request):
    phone = request.POST.get('phone')
    print(f"Checking Phone {phone}")
    if Profile.objects.filter(phone=phone).exists():
        return HttpResponse("<small class='text-danger'>Sorry phone number already in use.</small>")


class ProfileView(LoginRequiredMixin, DetailView, UpdateView):
    model = Profile
    fields = (
        "phone",
        "gender",
        "bio",
        "image",
        "country",
        "city",
        "birth_day",
    )
    context_object_name = 'profile'
    template_name = "profiles/me.html"

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.request.user.profile.slug)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        # if not self.request.session.has_key('currency'):
        #     self.request.session["currency"] = settings.DEFAULT_CURRENCY
        #     context["currency"] = self.request.session["currency"]
        context["user"] = Profile.objects.get(user=self.request.user)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profiles/form.html"
    context_object_name = 'profile'
    fields = (
        "phone",
        "gender",
        "bio",
        "image",
        "country",
        "city",
        "birth_day",
        "currency",
    )

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.kwargs.get("slug"))

    def form_valid(self, form, *args, **kwargs):
        last_url = self.request.META.get('HTTP_REFERER')
        phone = self.request.POST.get('phone')
        print(f"Phone number from frontend {phone}")
        profile_inst = form.save(commit=False)
        if Profile.objects.filter(phone=phone).exists():
            messages.error(self.request, "Phone number already taken please re-enter with another phone number")
            profile_inst.phone = ""
            profile_inst.save()
            return HttpResponseRedirect(last_url)
        profile_inst.phone = phone
        profile_inst.country = get_phone_country(phone)
        print(f"The original country is {profile_inst.country}")
        profile_inst.save()
        return super(ProfileUpdateView, self).form_valid(form)


# def select_currency(request):
#     last_url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         request.session['currency'] = request.POST['currency']
#         return HttpResponseRedirect(last_url)
#     return HttpResponseRedirect(last_url)


class SelectCountryCurrency(View):
    def post(self, request, slug):
        data = json.loads(request.body)
        country = data["countryVal"]
        print(f"country from frontend {country}")
        profile = Profile.objects.get(slug=slug)
        wallet = Wallet.objects.get(user=profile.user)
        if country == "NG":
            wallet.currency = "NGN"
            wallet.save()
            print("currency saved...")
            messages.success(request, "currency updated successfully...")
            return redirect("profiles:profile_detail", profile.slug)
        # ELSE assign US Dollars...
        wallet.currency = "USD"
        wallet.balance = wallet.balance/0.0014
        wallet.save()
        print("currency saved...")
        messages.success(request, "currency updated successfully...")
        return redirect("profiles:profile_detail", profile.slug)
        # ======= last_url = request.META.get('HTTP_REFERER')
        # ======= return HttpResponseRedirect(last_url)
