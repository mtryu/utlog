from django.contrib import admin 

# モデルをインポート 
from .models import Profile, Rest ,ScoreLog, Question, ScoreQ

# 管理サイトへのモデルの登録 
admin.site.register(Profile) 
admin.site.register(Rest)
admin.site.register(ScoreLog) 
admin.site.register(Question) 
admin.site.register(ScoreQ) 


