from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator
from iekari.models import Rest,ScoreLog,Question,ScoreQ
import random
import requests
import json
from django.db.models import Q
from iekari import forms
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

message_rate_created = '評価が登録・更新されました！'



inokashira = {1000:"駒場東大前", 1001:"神泉", 1002:"渋谷", 1003:"下北沢", 1004:"吉祥寺"}
genle_dict = {1:"カレー", 2:"ラーメン", 3:"定食", 4:"ギョウザ",5:"カフェ", 6:"中華", 7:"居酒屋", 8:"イタリアン",9:"つけ麺",10:"油そば"}
station_list =["駒場東大前","神泉","渋谷","下北沢","吉祥寺"]
genle_list = ["カレー","ラーメン","定食","ギョウザ","カフェ","中華","居酒屋","イタリアン","つけ麺","油そば"]
score_detail  = {7:"非常に良い", 6:"良い", 5:"どちらかと言えば良い", 4:"普通", 3:"どちらかと言えば悪い", 2:"悪い", 1:"非常に悪い"}
times = ["0分","~15分","~3分","~1時間","1時間以上"]
member = ["1人","2人","3~5人","6~9人","10人~"]
hours = list(range(7,25))
app = ''


def rest_view(request,first_id):
    first = int(first_id)
    allrest = Rest.objects.all()
    for rest in allrest:
        allscore = ScoreLog.objects.filter(rest_id=rest.id)
        total=0
        for i in allscore:
            total += int(i.score)     
        rest.score = ((rest.tabelog)*20+total)/(20+len(allscore))
        rest.save()

    if first>=1000:
        station = inokashira[first]
        rest_list = Rest.objects.filter(station=station).order_by('-score')
    else:
        food_genle = genle_dict[first]
        rest_list = Rest.objects.filter(
                Q(genle=food_genle)|
                Q(genle2=food_genle)
                ).distinct().order_by('-score')
    paginator = Paginator(rest_list, 20) # ページ当たり20個表示
    
    
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    rests = paginator.get_page(page)

    return render(request, 'iekari/rest_list.html', {'rests': rests, 'page': page, 'last_page': paginator.num_pages,'station_list':station_list, 'genle_list':genle_list})

def rest_detail(request,rest_id):
    
    API_Key = '97bad1368c7685b49e90eb3b091a9464'
    rest = Rest.objects.get(id=rest_id)
    alllog = ScoreLog.objects.filter(rest_id=rest_id)
    alltext=[]
    for log in alllog:
        if log.text != "0":
            alltext.append(log.text)
    if len(alltext) ==0:
        text_view = ["感想が投稿されていません。"]
    elif len(alltext) <= 2:
        text_view = alltext
    else:
        text_view = random.sample(alltext, 2)
    print(alllog)
    

    


    if rest.guru == 0:
        name = rest.name
        latitude = rest.lat
        longitude = rest.lon
        tel = rest.tel
        shop_image1 = '/static/iekari/img/no_img.jpg'
        station = rest.station
        station_exit =''
        walk = ''
        store_url = rest.url

    else:
        tel = rest.tel
        url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
        query = {
            'keyid': API_Key,
            'tel': tel
        }
        res = requests.get(url, params=query)
        Data = res.json()
        name = rest.name
        latitude = Data['rest'][0]['latitude']
        longitude = Data['rest'][0]['longitude']
        tel = Data['rest'][0]['tel']
        store_url = Data['rest'][0]['url']
        if Data['rest'][0]['image_url']['shop_image1'] == app:
            shop_image1 = '/static/iekari/img/no_img.jpg'
        else: 
            shop_image1 = Data['rest'][0]['image_url']['shop_image1']
        station = Data['rest'][0]['access']['station']
        station_exit = Data['rest'][0]['access']['station_exit']
        walk = (Data['rest'][0]['access']['walk'])+"分"
    


    return render(request, 'iekari/rest_detail.html',{'rest':rest, 'name': name, 'lat':latitude,'lon':longitude, 'tel':tel, 'url':store_url, 'shop_image':shop_image1,
             'station':station, 'station_exit':station_exit, 'walk':walk, 'score_detail':score_detail, 'times':times,'member':member, "hours":hours,
             'form': forms.Scoreform(), 'text_view':text_view})


@login_required
def rate(request,rest_id):
    rest = Rest.objects.get(id=rest_id)
    try:
        max_id = ScoreLog.objects.latest('id').id
    except ObjectDoesNotExist:
        max_id = 'C00000000'
    profile_id = request.user.profile.id
    ScoreLog.objects.filter(profile_id=profile_id,rest_id=rest_id).delete()
    
    score_id = 'C'+(str(int(max_id[1:])+1).zfill(8))
    if request.method == 'POST':
        
        log, created = ScoreLog.objects.update_or_create( 
            id = score_id,
            defaults = {
                'score':request.POST.get('score'),
                'time':request.POST.get('time'),
                'num':request.POST.get('num'),
                'wait':request.POST.get('wait'),
                'text':request.POST.get('text'),
                },
            profile_id = profile_id,
            rest_id = rest_id,
           
        )
  


    messages.success(request, message_rate_created)
    return redirect('iekari:rest_result')


def rest_result(request):  
    qqq = Question.objects.all()
    number = len(qqq)
    c = random.randint(1,number)
    qqqq = Question.objects.get(id=c)
    return render(request,"iekari/rest_result.html",{"qqqq":qqqq,'form': forms.Scoreform()})

def rest_nitaku(request,qqqq_id):
    try:
        max_id = ScoreQ.objects.latest('id').id
    except ObjectDoesNotExist:
        max_id = '0'
    profile_id = request.user.profile.id
    ScoreQ.objects.filter(profile_id=profile_id,question_id=qqqq_id).delete()
    
    q_id = int(max_id)+1
    if request.method == 'POST':
        
        log, created = ScoreQ.objects.update_or_create( 
            id = q_id,
            defaults = {'answer':request.POST.get('answer')},
            profile_id = profile_id,
            question_id = qqqq_id,
           
        )
    return redirect('/')

def rest_api(request,rest_id):
    
    API_Key = '03de712051fadd917905cdd2da9006a4'
    rest = Rest.objects.get(id=rest_id)
    tel = rest.tel
    url = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
    query = {
        'keyid': API_Key,
        'tel': tel
    }
    res = requests.get(url, params=query)
    Data = res.json()
    print(Data) 
    
