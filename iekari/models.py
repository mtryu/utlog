from django.contrib.auth.models import User 
from django.db import models 
 
GENDER_LIST = ( (0, '男性'), (1, '女性') )
dict_gender_list = dict(GENDER_LIST) 

class Rest(models.Model):
    class Meta:
        verbose_name = '飲食店データ'
        verbose_name_plural = '飲食店データ'
    id = models.CharField(max_length=6,primary_key=True)
    name = models.CharField('店名',max_length=50) 
    guru = models.IntegerField('ぐるなびAPI有無',default=0)
    genle = models.CharField('ジャンル1',max_length=50) 
    genle2 = models.CharField('ジャンル2',max_length=50,default=0)
    genle3 = models.CharField('ジャンル3',max_length=50,default=0)
    station = models.CharField('最寄り駅',max_length=50)
    distance = models.IntegerField('距離')
    price_lunch = models.IntegerField('昼金額')
    price_dinner = models.IntegerField('夜金額')
    tabeloog = models.FloatField('ログ')
    tabelog = models.FloatField('ログ修正値')
    tel = models.CharField('電話番号',max_length=50,default=0)
    score = models.FloatField('評価') 
    times = models.IntegerField('評価回数', default=3)  
    other = models.CharField('その他',max_length=50,default=0)  
    lat = models.FloatField('緯度',default=0)
    lon = models.FloatField('経度',default=0)
    url = models.CharField('URL',max_length=300,default=0)

    def __str__(self):
        return self.name

class Profile(models.Model):
    class Meta:
        verbose_name = 'ユーザー情報データ'
        verbose_name_plural = 'ユーザー情報データ'
    
    user = models.OneToOneField(User, verbose_name='ユーザー',null=True, blank=True, on_delete=models.CASCADE)

    id = models.CharField(max_length=6,primary_key=True)
    gender = models.IntegerField('性別',choices=GENDER_LIST)
    email = models.CharField('email',max_length=200,default=0)
    
    def __str__(self):
        user_str = ''
        if self.user is not None:
            user_str = '(' + self.user.username + ')'
        return self.id+' '+dict_gender_list.get(self.gender)+' ' 
  

class Question(models.Model):
    class Meta:
        verbose_name = '2択データ'
        verbose_name_plural = '2択データ'

    id = models.CharField(max_length=12,primary_key=True)
    question = models.CharField('質問',max_length=500,default=0)
    blue = models.CharField('回答1',max_length=500,default=0)
    red = models.CharField('回答1',max_length=500,default=0)
   
    
    

class ScoreLog(models.Model):
    class Meta:
        verbose_name = '飲食店評価データ'
        verbose_name_plural = '飲食店評価データ'

    id = models.CharField(max_length=12,primary_key=True)
    profile = models.ForeignKey(Profile, verbose_name='ユーザー情報', on_delete=models.CASCADE)
    rest = models.ForeignKey(Rest, verbose_name='飲食店', on_delete=models.CASCADE,default=0)

    score = models.IntegerField('評価',default=4)  
    time = models.IntegerField('入店時間',default=18)
    num = models.IntegerField('人数',default=2)
    wait = models.IntegerField('待ち時間',default=0)
    text = models.CharField('感想',max_length=10000,default=0)
    timestamp = models.DateTimeField('日時', auto_now_add=True) # 評価時点で更新


class ScoreQ(models.Model):
    class Meta:
        verbose_name = '2択回答データ'
        verbose_name_plural = '2択回答データ'
    id = models.CharField(max_length=12,primary_key=True)
    profile = models.ForeignKey(Profile, verbose_name='ユーザー情報', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=' 2択データ', on_delete=models.CASCADE)
    answer = models.IntegerField('回答',default=0)


