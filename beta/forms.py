# import form class from django
from .models import CustomUser
from django.http import request
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
# import GeeksModel from models.py
from .models import Review


class DateInput(forms.DateInput):
    input_type = 'date'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'moveIn': DateInput(),
            'moveOut': DateInput(),

        }

    # def __init__(self, *args, **kwargs):
    #     super(ReviewForm, self).__init__(*args, **kwargs)
    #     self.fields['moveIn'].widget = widgets.AdminDateWidget()
    #     self.fields['moveOut'].widget = widgets.AdminDateWidget()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        help_texts = {
            'username': None,
            'password': None,
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'signup_username'})
        self.fields['email'].widget.attrs.update({'class': 'signup_email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'signup_password1'}, widget=forms.TextInput())
        self.fields['password2'].widget.attrs.update(
            {'class': 'signup_password2'}, widget=forms.TextInput())

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
