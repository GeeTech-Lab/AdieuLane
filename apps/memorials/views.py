import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.base import View
from adieulane.flutterwave import FLUTTERWAVE_PUBLIC_KEY, FLUTTERWAVE_SECRET_KEY
from adieulane.utils import list_bank_names, exchange_rate
from .models import BurialMemory, MemoryGallery, MemoryTribute


class BurialMemoryList(ListView):
    model = BurialMemory
    context_object_name = "memorials"
    template_name = "burial_memories/list.html"


class BurialMemoryDetail(DetailView):
    model = BurialMemory
    context_object_name = "memorial"
    template_name = "burial_memories/detail.html"

    def get_context_data(self, **kwargs):
        context = super(BurialMemoryDetail, self).get_context_data(**kwargs)
        context["pub_key"] = FLUTTERWAVE_PUBLIC_KEY
        if self.request.user.is_authenticated:
            context["banks"] = list_bank_names(self.request.user.profile.country, FLUTTERWAVE_PUBLIC_KEY)
        context["galleries"] = MemoryGallery.objects.filter(burial_memory=self.get_object())
        context["donations"] = self.get_object().donations.all()
        context["tributes"] = self.get_object().memory_tributes.all()
        return context

# def toggle_accept_donation(request, slug):
#     memorial = BurialMemory.objects.get(slug=slug)
#     memorial.accept_donations = True
#     memorial.save()
#     return HttpResponse("<small class='text-success'>Donation accepted.</small>")


class BurialMemoryCreate(LoginRequiredMixin, CreateView):
    model = BurialMemory
    fields = (
        "title",
        "first_name",
        "last_name",
        "other_names",
        "image",
        "gender",
        "date_of_birth",
        "date_of_death",
        "place_of_birth",
        "place_of_death",
        "burial_ceremony_address",
        "cause_of_death",
        "brief_biography",
        "education",
        "work_life",
        "family_biography",
        "burial_ceremony_address",
        "accept_donations",
    )
    # success_url = reverse_lazy("burial_memories:list")
    template_name = "burial_memories/form.html"

    def form_valid(self, form):
        memorial_inst = form.save(commit=False)
        wallet = self.request.user.wallet
        upload_price = 2000.00
        toggle_donation = self.request.POST.get("toggle_donation")
        if wallet.currency == "USD":
            dollar_upload_price = exchange_rate(wallet, upload_price, 0.0014, "USD")
            if wallet.balance >= dollar_upload_price:
                wallet.balance = F('balance') - dollar_upload_price
                wallet.save()
                messages.success(self.request, f"Memorial uploaded successfully for ${dollar_upload_price}!!!...")
                if toggle_donation:
                    memorial_inst.accept_donations = True
                    print("Donation accepted...")
                memorial_inst.user = self.request.user
                print("successfully uploaded with Dollar...")
                memorial_inst.save()
                return super(BurialMemoryCreate, self).form_valid(form)
            messages.warning(self.request, "Memorial not created due to insufficient fund!!!...")
            return redirect("wallets:fund_wallet", self.request.user.wallet.uid)
        if wallet.balance >= upload_price:
            wallet.balance = F('balance') - upload_price
            wallet.save()
            messages.success(self.request, f"Memorial uploaded successfully for N{upload_price}!!!...")
            if toggle_donation:
                memorial_inst.accept_donations = True
                print("Donation accepted...")
            memorial_inst.user = self.request.user
            memorial_inst.save()
            return super(BurialMemoryCreate, self).form_valid(form)
        messages.warning(self.request, "Memorial not created due to insufficient fund!!!...")
        return redirect("wallets:fund_wallet", self.request.user.wallet.uid)

    def get_context_data(self, **kwargs):
        context = super(BurialMemoryCreate, self).get_context_data()
        my_wallet = self.request.user.wallet
        if my_wallet.user.profile.country == "NG":
            context['upload_price'] = exchange_rate(my_wallet, 2000, 1, "NGN")
        else:
            context['upload_price'] = exchange_rate(my_wallet, 2000, 0.0014, "USD")
        context['wallet'] = my_wallet
        return context

    def get_success_url(self, **kwargs):
        return reverse("memorials:list")


class BurialMemoryUpdate(LoginRequiredMixin, UpdateView):
    model = BurialMemory
    fields = (
        "title",
        "first_name",
        "last_name",
        "other_names",
        "image",
        "gender",
        "date_of_birth",
        "date_of_death",
        "place_of_birth",
        "place_of_death",
        "burial_ceremony_address",
        "cause_of_death",
        "brief_biography",
        "education",
        "work_life",
        "family_biography",
        "burial_ceremony_address",
        "accept_donations",
    )
    template_name = "burial_memories/form.html"

    def get_success_url(self, **kwargs):
        memorial = BurialMemory.objects.get(by=self.request.user)
        return reverse("memorials:update", memorial.slug)


class BurialMemoryDelete(LoginRequiredMixin, DeleteView):
    model = BurialMemory
    success_url = reverse_lazy("memorials:list")


class GalleryListView(ListView):
    template_name = "burial_memories/gallery_list.html"
    model = MemoryGallery
    context_object_name = "galleries"

    def get_queryset(self):
        get_memory = BurialMemory.objects.get(slug=self.kwargs.get("slug"))
        return get_memory.galleries.all()


class GalleryAddView(View):
    def get(self, request, slug):
        memorial = get_object_or_404(BurialMemory, slug=slug)
        galleries = memorial.galleries.all()
        # form = MemoryGalleryForm(request.POST)
        context = {
            'memorial': memorial,
            'galleries': galleries,
        }
        return render(request, 'burial_memories/detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        memorial = get_object_or_404(BurialMemory, slug=slug)
        galleries = memorial.galleries.all()
        description = request.POST.get("description")
        image = request.FILES.get("memory_image")
        video_link = request.POST.get("memory_video")
        gallery = MemoryGallery.objects.create(
            by=request.user,
            burial_memory=memorial,
            description=description,
            image=image,
            video=video_link,
        )
        gallery.save()
        context = {
            'memorial': memorial,
            'galleries': galleries,
        }
        messages.success(request, "Media item added successfully...")
        return render(request, 'burial_memories/detail.html', context)


# def add_gallery(request, slug):
#     memorial = get_object_or_404(BurialMemory, slug=slug)
#     print(memorial.get_name)
#     galleries = memorial.galleries.all()
#     description = request.POST.get("description")
#     image = request.FILES.get("memory_image")  # if True else None
#     video = request.FILES.get("memory_video")  # if True else None
#     audio = request.FILES.get("memory_audio")  # if True else None
#     gallery = MemoryGallery.objects.create(
#         by=request.user,
#         burial_memory=memorial,
#         description=description,
#         image=image,
#         video=video,
#         audio=audio,
#     )
#     memorial.galleries.add(gallery)
#     context = {
#         'galleries': galleries,
#     }
#     messages.success(request, "Media item added successfully...")
#     return render(request, 'burial_memories/gallery_list.html', context)


def add_tribute(request, slug):
    get_memory = get_object_or_404(BurialMemory, slug=slug)
    tribute_text = request.POST.get("tribute")
    get_category = request.POST.get("category")
    category = None
    if get_category == "candle":
        category = "candle"
    elif get_category == "flower":
        category = "flower"
    elif get_category == "note":
        category = "note"
    print(category)
    tribute = MemoryTribute.objects.create(
        burial_memory=get_memory,
        tribute_text=tribute_text,
        by=request.user,
        category=category,
        on=datetime.datetime.now(),
    )
    get_memory.memory_tributes.add(tribute)
    tributes = get_memory.memory_tributes.all()
    context = {
        "tributes": tributes,
    }
    return render(request, "burial_memories/tribute_list.html", context)
