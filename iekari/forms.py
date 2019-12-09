from django.forms import Form, ModelForm, HiddenInput
from django import forms



class Scoreform(forms.Form):
    SCORE = [
        ('7','7:非常に良い'),
        ('6','6:良い'),
        ('5','5:どちらかと言えば良い'),
        ('4','4:普通'),
        ('3','3:どちらかと言えば悪い'),
        ('2','2:悪い'),
        ('1','1:非常に悪い')
        ]
    score=forms.ChoiceField(
        label='総合評価',
        widget=forms.RadioSelect(),
        choices=SCORE,
        required=True,
    )
    NUM = [
        ('1','1人'),
        ('2','2人'),
        ('4','3~5人'),
        ('8','6~9人'),
        ('10','10人'),
        ]
    num=forms.ChoiceField(
        label='人数',
        widget=forms.RadioSelect(),
        choices=NUM,
        required=True,
    )
    QUESTIONS = [
        ('0','0'),
        ('1','1'),
        ]
    answer=forms.ChoiceField(
        label='おまけ2択',
        widget=forms.RadioSelect(),
        choices=QUESTIONS,
        required=True,
    )
    TIME = [
        ('0','0分'),
        ('8','~15分'),
        ('20','~30分'),
        ('45','~1時間'),
        ('60','1時間以上'),
        ]
    wait=forms.ChoiceField(
        label='待ち時間',
        widget=forms.RadioSelect(),
        choices=TIME,
        required=True,
    )
    
    EMPTY_CHOICES =[
        ('', '選択してください'),
    ]
    TIMECHOICES = []
    for p in range(7,25):
        TIMECHOICES.append(
            [p,str(p)+'時'])
    
    time = forms.ChoiceField(
        label='入店時間:',
        widget=forms.Select,
        choices=EMPTY_CHOICES + TIMECHOICES,
        required=True,
    )
    text = forms.CharField(
        label='感想!!(あれば)', 
        widget=forms.Textarea,
        required=False,
    )

