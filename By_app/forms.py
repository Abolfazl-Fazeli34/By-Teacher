from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        label='نام',
        widget=forms.TextInput(attrs={'placeholder': 'نام خود را وارد کنید'})
    )
    last_name = forms.CharField(
        max_length=50,
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی خود را وارد کنید'})
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder': 'ایمیل خود را وارد کنید'})
    )
    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور را وارد کنید'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور را دوباره وارد کنید'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']




from django import forms

class EmailCodeForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(max_length=6)

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={
        'placeholder': 'ایمیل خود را وارد کنید',
        'class': 'form-control'
    }))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={
        'placeholder': 'رمز عبور را وارد کنید',
        'class': 'form-control'
    }))


from django import forms
from .models import Teacher

class VoteForm(forms.Form):
    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="معلم(های) مورد نظر برای رأی دادن (حداکثر ۳ معلم)"
    )

    def clean_teachers(self):
        teachers = self.cleaned_data.get('teachers')
        if len(teachers) > 3:
            raise forms.ValidationError("شما فقط می‌توانید به حداکثر ۳ معلم رأی دهید.")
        return teachers


