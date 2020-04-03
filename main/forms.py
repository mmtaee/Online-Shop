from django import forms
from django.core.exceptions import ValidationError
from .models import Manufacturer, Category, Product

# Manufacturer Forms
class ManufacturerCreateForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'image', 'desc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desc'].required = False
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'id' : 'validationServer013', 'placeholder' : 'Manufacturer Name', 'model' : 'Manufacturer'})
        for field in self.fields:
                self.fields[field].widget.attrs.update({'placeholder' : field.title()})

    def clean_name(self):
        cleaned_data = super().clean()
        name = self.cleaned_data['name']
        if Manufacturer.objects.filter(name__iexact=name):
            raise forms.ValidationError(f"The manufacturer name {name} already exists")
        return name

class ManufacturerEditForm(forms.ModelForm):
    edit = forms.CharField(widget=forms.TextInput(), max_length=120, label="Edit Name")
    class Meta:
        model = Manufacturer
        fields = ['name', 'edit', 'image', 'desc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['edit'].required = False
        self.fields['desc'].required = False
        self.fields['name'].disabled = True
        self.fields['edit'].widget.attrs.update({'class': 'form-control', 'id' : 'validationServer013', 'placeholder' : 'Manufacturer Name', 'model' : 'Manufacturer'})

        for field in self.fields:
                self.fields[field].widget.attrs.update({'placeholder' : field.title()})

    def clean_new_name(self):
        cleaned_data = super().clean()
        new_name = self.cleaned_data['new_name']
        if new_name :
            if Manufacturer.objects.filter(name__iexact=new_name):
                raise forms.ValidationError(f"The manufacturer name {new_name} already exists")
        return new_name


# Category Forms
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'id' : 'validationServer013', 'placeholder' : 'Category Name', 'model' : 'Category'})

    def clean_name(self):
        cleaned_data = super().clean()
        name = self.cleaned_data['name']
        if Category.objects.filter(name__iexact=name):
            raise forms.ValidationError(f"The category name {name} already exists")
        return name


# Product Forms
class ProductCreateForm(forms.ModelForm):
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all())
    multipleimages = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        fields = ['manufacturer', 'category', 'name', 'model' , 'tags', 'initial_price', 'off', 'stock', 'image','multipleimages', 'desc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'inp_text form-control', 'id' : 'validationServer013', 'model' : 'Product'})
        self.fields['category'].empty_label="Select Category"
        self.fields['manufacturer'].empty_label="Select Manufacturer"
        self.fields['off'].widget.attrs.update({'class': "inp form-control", "min" : "0", "max" : "99"})
        self.fields['stock'].widget.attrs.update({'class': "inp form-control"})
        self.fields['desc'].widget.attrs.update({'rows':10, 'cols':35,})
        self.fields['initial_price'].widget.attrs.update({'class': 'number-separator'})
        self.fields['manufacturer'].widget.attrs.update({'class': 'inp2 browser-default custom-select',})
        self.fields['category'].widget.attrs.update({'class': 'inp2 browser-default custom-select',})

        required_False = ['manufacturer', 'category', 'off', 'tags','multipleimages']
        for field in self.fields:
                self.fields[field].widget.attrs.update({'placeholder' : field.title()})
                if field in required_False :
                    self.fields[field].required = False


    def clean_name(self):
        cleaned_data = super().clean()
        name = self.cleaned_data['name']
        if Product.objects.filter(name__iexact=name):
            raise forms.ValidationError(f"The product name {name} already exists")
        return name

    def clean_initial_price(self):
        cleaned_data = super().clean()
        initial_price = self.cleaned_data['initial_price']
        if not initial_price.replace(",", "").isnumeric():
            raise forms.ValidationError("Input should be number")
        return initial_price

class ProductEditForm(forms.ModelForm):
    clear_images = forms.BooleanField(widget=forms.NullBooleanSelect(), help_text="This Field Can Delete All Old Multiple Images, But Save New Multiple Images ")
    multipleimages = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    edit = forms.CharField(widget=forms.TextInput(), max_length=120,)

    class Meta:
        model = Product
        fields = ['name', 'edit', 'tags', 'initial_price', 'off', 'stock', 'image', 'multipleimages', 'clear_images', 'desc',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['edit'].widget.attrs.update({'class': 'form-control', 'id' : 'validationServer013', 'placeholder' : 'Edit Name', 'model' : 'Product'})
        self.fields['off'].widget.attrs.update({'class': "inp form-control", "min" : "0", "max" : "99"})
        self.fields['stock'].widget.attrs.update({'class': "inp form-control"})
        self.fields['desc'].widget.attrs.update({'rows':10, 'cols':35, 'placeholder':'Description'})
        self.fields['initial_price'].widget.attrs.update({'class': 'number-separator'})
        self.fields['name'].disabled = True
        for field in self.fields:
            if field != 'edit':
                self.fields[field].widget.attrs.update({'placeholder' : field.title()})
            self.fields[field].required = False

        self.fields['clear_images'].widget = forms.Select(choices=[(False, "No"),(True, "Yes"),])
        self.fields['tags'].widget.attrs.update({"class":"form-control", "name":"tags", "data-role":"tagsinput",})

    def clean_new_name(self):
        cleaned_data = super().clean()
        new_name = self.cleaned_data['new_name']
        if new_name :
            if Product.objects.filter(name__iexact=new_name):
                raise forms.ValidationError(f"The product name {new_name} already exists")
        return new_name

    def clean_initial_price(self):
        cleaned_data = super().clean()
        initial_price = self.cleaned_data['initial_price']
        if initial_price :
            if not initial_price.replace(",", "").isnumeric():
                raise forms.ValidationError("Input should be number")
        return initial_price


class DeleteProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = True
        self.fields['product'].widget.attrs.update({'class': 'browser-default custom-select'})
