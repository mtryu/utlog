from django.urls import path
from iekari.views import  mypage , recommend, assess, superuser, rest_func

app_name = 'iekari'
urlpatterns = [

    path('mypage', mypage.mypage_top, name='mypage_top'),
    path('rest_func/<int:first_id>',rest_func.rest_view, name='rest_func'),
    path('rest_api/<slug:rest_id>', rest_func.rest_api, name='rest_api'),
    path('rest_detail/<slug:rest_id>', rest_func.rest_detail, name='rest_detail'),
    path('rest_detail',rest_func.rest_detail,name='rest_detail'),
    path('rest_detail/<slug:rest_id>/rate', rest_func.rate, name='rest_rate'),
    path('result',rest_func.rest_result,name='rest_result'),
    path('result/nitaku/<slug:qqqq_id>',rest_func.rest_nitaku,name='rest_nitaku'),


    ]