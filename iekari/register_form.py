from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import re

from iekari.models import GENDER_LIST, Profile

class RegisterForm(UserCreationForm):
    
    gender = forms.ChoiceField(choices=GENDER_LIST, required=True)


    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','gender','email']
        labels = {
            'username': 'ユーザー名',
            'password1': 'パスワード',
            'password2': 'パスワード確認',
            'gender': '性別',
            'email': 'メールアドレス \n(末尾が@g.ecc.u-tokyo.ac.jp)',

            
        }

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError('Cannot create User and Profile without database save')
        email = self.cleaned_data['email']
        if  not re.match(r'.+@g.ecc.u-tokyo.ac.jp',email):
            raise ValueError('Users must have an correct email end with "@g.ecc.u-tokyo.ac.jp"')
        user = super().save()

        try:
            max_id = Profile.objects.latest('id').id
        except ObjectDoesNotExist:
            max_id = 'B00000'

        prof_id = 'B'+(str(int(max_id[1:])+1).zfill(5))

       
        gender = self.cleaned_data['gender']
        


        profile = Profile(id=prof_id,gender=gender,user_id=user.id,email=email)
        profile.save()

        return user