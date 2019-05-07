from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput
from .models import City, BusInfo, Schedule, Routes, User

class register_form(UserCreationForm):
    email = forms.EmailField(required = True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required = True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required = True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }
        def save(self, commit=True):
            user = super(register_form, self).save(commit = False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data ['last_name']
            user.email = self.cleaned_data ['email']

            if commit:
                user.save()
            return user

class edit_profile_form (UserChangeForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'password'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class bus_reg_form(forms.Form):
    plate_num = forms.CharField(required=True, label='Plate Number')
    type = forms.CharField(required=True, label='Bus Type')
    image = forms.FileField(required=True, label='Image (* JPG , PNG)', widget=forms.ClearableFileInput(attrs={'multiple': False}))
    plate_photo = forms.FileField(required=True, label='Plate Photo (* JPG , PNG)', widget=forms.ClearableFileInput(attrs={'multiple': False}))
    photo1 = forms.FileField(required=True, label='Photo 1 (* JPG , PNG)', widget=forms.ClearableFileInput(attrs={'multiple': False}))
    photo2 = forms.FileField(required=True, label='Photo 2 (* JPG , PNG)', widget=forms.ClearableFileInput(attrs={'multiple': False}))
    photo3 = forms.FileField(required=True, label='Photo 3 (* JPG , PNG)', widget=forms.ClearableFileInput(attrs={'multiple': False}))
    photo4 = forms.FileField(required=True, label='Photo 4 (* JPG , PNG)', widget=forms.ClearableFileInput(attrs={'multiple': False}))
    photo5 = forms.FileField(required=True, label='Photo 5 (* JPG , PNG)', widget=forms.ClearableFileInput(attrs={'multiple': False}))


    def __init__(self, *args, **kwargs):
        super(bus_reg_form, self).__init__(*args, **kwargs)
        self.fields['plate_num'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter vehicle plate number. Example: MDY 0A-0000'})
        self.fields['type'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter bus type'})


class bus_edit_form(forms.ModelForm):
    class Meta:
        model = BusInfo
        fields = (
            'plate_num',
            'type',
            'image',
            'plate_photo', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super(bus_edit_form, self).__init__(*args, **kwargs)
        self.fields['plate_num'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Vehicle plate number'})

class schedule_edit_form(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = (
            'route',
            'depart_time',
            'arrive_time'
        )

    # def __init__(self, *args, **kwargs):
    #     super(schedule_edit_form, self).__init__(*args, **kwargs)
    #     self.fields['depart_date'].widget = TextInput(attrs={
    #         'class': 'form-control',
    #         'id': 'datepicker'})
    #     self.fields['depart_time'].widget = TextInput(attrs={
    #         'class': 'form-control timepicker'})





