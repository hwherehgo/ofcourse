
from django.forms import ModelForm
from django.forms import CharField
from django.forms import ValidationError

from user.models import User


class Userform(ModelForm):
    class Meta:
        model = User
        fields = ['nickname','password','icon','sex','age']
    password2 = CharField(max_length=128)

    def clean_password2(self):
        cleaned_data = super().clean()
        if cleaned_data['password']!=cleaned_data['password2']:
            raise ValidationError('两次密码不正确')