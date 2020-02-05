from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields= ('username','email','password1','password2')

    # def clean_email(self):
    #         username = self.cleaned_data["username"]
    #         email = self.cleaned_data["email"]
    #         users = User.objects.filter(email__iexact=email).exclude(username__iexact=username)
    #         if users:
    #             raise forms.ValidationError(("User with that email already exists."))
    #         return email.lower()

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2
 
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
    

        
class ProfileForm(forms.ModelForm):
    profilePicture = models.ImageField(upload_to = 'photos/%Y/%m/%d', blank = True)



    class Meta:
        model = userProfile
        fields = ('address','mobile_no','city','state','country','profilePicture')


# class AccountAuthenticationForm(forms.ModelForm):

#     password = forms.CharField(label='Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('username', 'password')

#     def clean(self):
#         if self.is_valid():
#             email = self.cleaned_data['email']
#             password = self.cleaned_data['password']
#             if not authenticate(email=email, password=password):
#                 raise forms.ValidationError("Invalid login")


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = ("There is no user registered with the specified E-Mail address.")

            self.add_error('email', msg)
        return email