from django import forms
from .models import BurialMemory, FamilyTree, MemoryGallery, MemoryTribute


class BurialMemoryForm(forms.ModelForm):

    class Meta:
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
            "accept_donations",
        )
        # widgets = {
        #     'content': SummernoteWidget(),
        # }
        widgets = {
            'accept_donations': forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "flexSwitchCheckChecked",
                    "checked": "",
                    "type": "checkbox",
                    "data-toggle": "switch",
                    "data-on-text": "<i class='nc-icon nc-check-2'></i>",
                    "data-off-text": "<i class='nc-icon nc-simple-remove'></i>",
                    "data-on-color": "success",
                    "data-off-color": "success",
                }
            )
        }


class MemoryGalleryForm(forms.ModelForm):

    class Meta:
        model = MemoryGallery
        fields = (
            "description",
            "image",
            "video",
            "audio",
        )


class FamilyTreeForm(forms.ModelForm):

    class Meta:
        model = FamilyTree
        fields = (
            "title",
            "user_full_name",
            "guest_full_name",
            "image",
            "relationship",
        )


class MemoryTributeForm(forms.ModelForm):

    class Meta:
        model = MemoryTribute
        fields = (
            "tribute_text",
            "category",
        )
