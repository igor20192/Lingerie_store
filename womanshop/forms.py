from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.
    """

    class Meta:
        model = UserProfile
        fields = [
            "address",
            "city",
            "state",
            "zip_code",
            "phone_number",
            "date_of_birth",
            "gender",
            "profile_pic",
        ]

        widgets = {
            "profile_pic": forms.ClearableFileInput(
                attrs={"multiple": True}
            ),  # Настройка виджета для загрузки медиа-файлов
        }
        widgets["profile_pic"].attrs.update({"enctype": "multipart/form-data"})

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Установка дефолтных значений для полей формы из полей модели
        self.initial["address"] = self.instance.address
        self.initial["city"] = self.instance.city
        self.initial["state"] = self.instance.state
        self.initial["zip_code"] = self.instance.zip_code
        self.initial["phone_number"] = self.instance.phone_number
        self.initial["date_of_birth"] = self.instance.date_of_birth
        self.initial["gender"] = self.instance.gender


class CategoryForm(forms.Form):
    """
    Форма для выбора категории товаров.
    """

    bodysuit = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Боди",
        required=False,
    )
    bras = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Бюстгальтеры",
        required=False,
    )
    tights_and_socks = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label=" Колготки и носки ",
        required=False,
    )
    swimwear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Купальники",
        required=False,
    )
    men_underwear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Мужское белье ",
        required=False,
    )
    panties = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Трусики",
        required=False,
    )
    seamless_underwear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Бесшовное нижнее белье",
        required=False,
    )
    thermal_underwear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
        label="Термобелье",
    )
    accessories = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Аксессуары",
        required=False,
    )


class PriceForm(forms.Form):
    """
    Форма для выбора диапазона цен.
    """

    start = forms.IntegerField(
        required=False,
        label="От",
        widget=forms.TextInput(attrs={"style": "width: 97px;"}),
    )
    end = forms.IntegerField(
        required=False,
        label="До",
        widget=forms.TextInput(attrs={"style": "width: 97px;"}),
    )


class StyleForm(forms.Form):
    """
    Форма для выбора стилей белья.

    Поля формы:
        - basic_underwear: bool, выбор базового белья.
        - new: bool, выбор новинок.
        - comfort_underwear: bool, выбор комфортного белья.
        - sexual: bool, выбор сексуального белья.
        - lacy: bool, выбор кружевного белья.
        - everyday: bool, выбор повседневного белья.
        - homewear: bool, выбор одежды для дома.
        - sleepwear: bool, выбор одежды для сна.
        - for_wedding: bool, выбор белья для свадьбы.
    """

    basic_underwear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Базовое белье",
        required=False,
    )
    new = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Новинки",
        required=False,
    )
    сomfort_underwear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Комфортное белье",
        required=False,
    )
    sexual = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
        label="Сексуальное",
    )
    lacy = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Кружевное",
        required=False,
    )
    everyday = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Повседневное",
        required=False,
    )
    homewear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Одежда для дома",
        required=False,
    )
    sleepwear = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Одежда для сна",
        required=False,
    )
    for_wedding = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
        label="Для свадьбы",
    )


class BrandForm(forms.Form):
    """
    Форма для выбора брендов белья.

    Поля формы:
        - avelin: bool, выбор белья бренда AVELIN.
        - comazo: bool, выбор белья бренда COMAZO.
        - lauma: bool, выбор белья бренда LAUMA.
        - melado: bool, выбор белья бренда MELADO.
        - milavitsa: bool, выбор белья бренда MILAVITSA.
        - serge: bool, выбор белья бренда SERGE.
        - teatro: bool, выбор белья бренда TEATRO.
        - triumph: bool, выбор белья бренда TRIUMPH.
    """

    avelin = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="AVELIN",
        required=False,
    )
    comazo = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="COMAZO",
        required=False,
    )
    lauma = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="LAUMA",
        required=False,
    )
    melado = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
        label="MELADO",
    )
    milavitsa = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="MILAVITSA",
        required=False,
    )
    serge = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="SERGE",
        required=False,
    )
    teatro = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="TEATRO",
        required=False,
    )
    triumph = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="TRIUMPH",
        required=False,
    )
