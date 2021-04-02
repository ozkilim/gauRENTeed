# import form class from django
from .models import CustomUser
from django.http import request
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
# import GeeksModel from models.py
from .models import Review, Property


class DateInput(forms.DateInput):
    input_type = 'date'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ('verified', 'property',)
        widgets = {
            'moveIn': DateInput(),
            'moveOut': DateInput(),
        }

    def clean(self):
        # not working currently.
        cleaned_data = super(ReviewForm, self).clean()
        start_date = cleaned_data.get("moveIn")
        end_date = cleaned_data.get("moveOut")
        if start_date and end_date:
            if end_date < start_date:
                print("hereerror")
                raise forms.ValidationError(
                    "End date should be later than start date.")
                return cleaned_data
        # return cleaned_data

    # def __init__(self, *args, **kwargs):
    #     super(ReviewForm, self).__init__(*args, **kwargs)
    #     self.fields['moveIn'].widget = widgets.AdminDateWidget()
    #     self.fields['moveOut'].widget = widgets.AdminDateWidget()


class PropertyCreationForm(forms.ModelForm):
    class Meta:

        # here use google api input for property finding then house or appartment fields...

        model = Property
        fields = '__all__'
        exclude = ('fullAddress',)

        # make the appt number only changable  when
        # widgets = {
        #     'moveIn': DateInput(),
        #     'moveOut': DateInput(),

        # }


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
