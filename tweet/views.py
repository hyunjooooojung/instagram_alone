from re import T
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import TweetModel
from .models  import TweetComment
from user.models import UserModel
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
import random

# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/home')
    else:
        return redirect('/sign-in')
    

def tweet(request):
    if request.method == "GET":
        # 사용자가 로그인 되어있는지 확인하기
        user = request.user.is_authenticated
        
        if user: # 로그인 되어있는 사용자라면 
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            all_comment = TweetComment.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet, 'comment': all_comment})
        else: # 로그인 되어있지 않다면
            return redirect('/sign-in')
        
    elif request.method == "POST":
        user = request.user
        my_tweet = TweetModel()  # 글쓰기 모델 가져오기
        my_tweet.author = user  # 모델에 사용자 저장
        my_tweet.content = request.POST.get('my-content', '')  # 모델에 글 저장
        my_tweet.save()
        return redirect('/tweet')