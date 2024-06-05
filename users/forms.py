from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label="Email")

    def clean(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email__iexact=email)
            self.cleaned_data['username'] = user.username
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email id or password")
        return self.cleaned_data
    
    def get_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            users = User.objects.filter(email=username) | User.objects.filter(username=username)
            for user in users:
                if user.check_password(password):
                    return user
        except User.DoesNotExist:
            return None