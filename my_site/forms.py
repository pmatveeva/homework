from my_site.models import UserProfile, Computer, Order
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.core.files import File
from django.core.files.storage import FileSystemStorage


class LoginForm(forms.Form):
    password = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'id': 'password',
                   'placeholder': 'Password'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Enter login', }),
        label='Login:')

    def clean(self):
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Wrong username or password')
        self.cleaned_data['user'] = user


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Enter login', }),
        min_length=5, label='Login:')
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'Enter name', }),
        max_length=30, label='Name:')
    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'surname',
                   'placeholder': 'Enter surname', }),
        max_length=30, label='Surname:')
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'id': 'email',
                   'placeholder': 'Enter email', }))
    password = forms.CharField(
        min_length=8, label='Password:',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'id': 'password',
                   'placeholder': 'Enter password', }))
    password2 = forms.CharField(
        min_length=8, label='Confirm password:',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'id': 'password2',
                   'placeholder': 'Confirm password', }))
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'address',
                   'placeholder': 'Enter address', }),
        max_length=300, label='Address:')
    telephone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'telephone',
               'placeholder': 'Enter telephone', }),
        max_length=20, label='Telephone:')
    birth_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control',
               'id': 'birth_date',
               'placeholder': 'Enter your date of birth', }),
        label='Birth date:',
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(
        widget=forms.RadioSelect, choices=GENDER_CHOICES)

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Passwords does not match')

    def save(self):
        u = UserProfile()
        u.username = self.cleaned_data.get('username')
        u.password = make_password(self.cleaned_data.get('password'))
        u.first_name = self.cleaned_data.get('name')
        u.last_name = self.cleaned_data.get('surname')
        u.email = self.cleaned_data.get('email')
        u.is_staff = False
        u.is_active = True
        u.is_superuser = False
        u.address = self.cleaned_data.get('address')
        u.telephone = self.cleaned_data.get('telephone')
        u.birth_date = self.cleaned_data.get('birth_date')
        u.gender = self.cleaned_data.get('gender')
        u.save()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('This login is already used')
        except User.DoesNotExist:
            return username


class ComputerForm(forms.ModelForm):
    class Meta(object):
        model = Computer
        fields = ['name', 'price', 'pic', 'description', 'quantity', 'type']

    def save(self):
        computer = Computer()
        computer.name = self.cleaned_data.get('name')
        computer.price = self.cleaned_data.get('price')
        computer.type = self.cleaned_data.get('type')
        computer.quantity = self.cleaned_data.get('quantity')
        computer.description = self.cleaned_data.get('description')
        f = self.cleaned_data.get("pic")
        if f is None:
            file_url = r'/default.jpg'
        else:
            file_url = r'/media/%s%s' % (computer.name, '.jpg')
            filename = FileSystemStorage().save(
                '/Users/hp/PycharmProjects/hw/' + file_url,
                File(f))
        computer.pic = file_url
        computer.save()
