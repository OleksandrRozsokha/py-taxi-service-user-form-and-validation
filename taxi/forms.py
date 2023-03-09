from typing import Optional, Dict, Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    MAX_LEN = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> Optional[Dict[str, Any]]:
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != self.MAX_LEN:
            raise ValidationError(
                f"License number must consist {self.MAX_LEN} characters"
            )
        if ((not license_number[:3].isalpha())
                or (license_number[:3] != license_number[:3].upper())):
            raise ValidationError(
                "First 3 characters must be uppercase letters"
            )
        if not license_number[3:].isdigit():
            raise ValidationError(
                "Last 5 characters must be digits"
            )
        return license_number


class DriverCreationForm(UserCreationForm):
    LENGTH = 8
    MESSAGE = (
        "License number must have 8 characters"
        " and first 3 uppercase letters than 5 numbers ;)"
    )
    REGEX = "[A-Z]{3}[0-9]{5}"

    license_number = forms.CharField(
        required=True,
        validators=[
            MinLengthValidator(LENGTH),
            MaxLengthValidator(LENGTH),
            RegexValidator(
                message=MESSAGE,
                regex=REGEX
            )
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"