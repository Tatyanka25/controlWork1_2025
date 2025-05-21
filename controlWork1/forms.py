import re
from django import forms
from .models import Order, ArtworkCostCalculation, CanvasType, MaterialType
from datetime import date, timedelta


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "surname", "patronymic", "birth_date", "phone_number"]
        widgets = {
            "birth_date": forms.DateInput(
                attrs={"type": "date", "placeholder": "ГГГГ-ММ-ДД"}, format="%Y-%m-%d"
            ),
            "name": forms.TextInput(attrs={"placeholder": "Иван"}),
            "surname": forms.TextInput(attrs={"placeholder": "Иванов"}),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Иванович (необязательно)"}
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "+79991234567 или 89991234567"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control mb-2"
            if field.required:
                field.label = f"{field.label} *"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[А-ЯЁ][а-яёА-ЯЁ]*$", name):
            raise forms.ValidationError(
                "Имя должно начинаться с заглавной буквы и содержать только русские буквы."
            )
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get("surname")
        if not re.match(r"^[А-ЯЁ][а-яёА-ЯЁ]*$", surname):
            raise forms.ValidationError(
                "Фамилия должна начинаться с заглавной буквы и содержать только русские буквы."
            )
        return surname

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get("patronymic")
        if patronymic:  # Валидируем только если поле заполнено
            if not re.match(r"^[А-ЯЁ][а-яёА-ЯЁ]*$", patronymic):
                raise forms.ValidationError(
                    "Отчество должно начинаться с заглавной буквы и содержать только русские буквы (если указано)."
                )
        return patronymic

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date:
            today = date.today()
            sixteen_years_ago = today - timedelta(days=16 * 365.25)
            try:
                sixteen_years_ago_exact = today.replace(year=today.year - 16)
            except ValueError:
                sixteen_years_ago_exact = today.replace(
                    year=today.year - 16, day=today.day - 1
                )

            if birth_date > sixteen_years_ago_exact:
                raise forms.ValidationError(
                    f'Вам должно быть не менее 16 лет. Минимальная дата рождения: {sixteen_years_ago_exact.strftime("%d.%m.%Y")}.'
                )
        return birth_date

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        cleaned_phone = re.sub(r"[^\d+]", "", phone_number)

        if cleaned_phone.startswith("+7"):
            if not re.match(r"^\+7\d{10}$", cleaned_phone):
                raise forms.ValidationError(
                    'Номер телефона должен быть в формате +7XXXXXXXXXX (11 цифр после "+").'
                )
            return cleaned_phone
        elif cleaned_phone.startswith("8"):
            if not re.match(r"^8\d{10}$", cleaned_phone):
                raise forms.ValidationError(
                    'Номер телефона должен быть в формате 8XXXXXXXXXX (10 цифр после "8").'
                )
            return cleaned_phone
        elif (
            re.match(r"^\d{10}$", cleaned_phone)
            and not cleaned_phone.startswith("8")
            and not cleaned_phone.startswith("7")
        ):
            raise forms.ValidationError("Номер телефона должен начинаться с +7 или 8.")
        else:
            raise forms.ValidationError(
                "Некорректный формат номера телефона. Используйте +7XXXXXXXXXX или 8XXXXXXXXXX."
            )

class ArtworkCostCalculationForm(forms.ModelForm):
    height = forms.IntegerField(
        label="Высота картины (см)",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Например, 50'})
    )
    width = forms.IntegerField(
        label="Ширина картины (см)",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Например, 70'})
    )
    canvas_type = forms.ModelChoiceField(
        queryset=CanvasType.objects.all().order_by('price_per_sq_cm', 'name'),
        label="Тип холста",
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    material_type = forms.ModelChoiceField(
        queryset=MaterialType.objects.all().order_by('price_per_sq_cm', 'name'),
        label="Тип материалов",
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ArtworkCostCalculation
        fields = ['height', 'width', 'canvas_type', 'material_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('canvas_type') and self.fields['canvas_type'].queryset.exists():
            self.initial['canvas_type'] = self.fields['canvas_type'].queryset.first()
        if not self.initial.get('material_type') and self.fields['material_type'].queryset.exists():
            self.initial['material_type'] = self.fields['material_type'].queryset.first()

        for field_name, field in self.fields.items():
            if field.required:
                field.label = f"{field.label}*"