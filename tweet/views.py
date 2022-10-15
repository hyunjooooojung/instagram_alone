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
from django.views.generic import ListView, TemplateView

# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')
    

def tweet(request):
    if request.method == "GET":
        # 사용자가 로그인 되어있는지 확인하기
        user = request.user.is_authenticated
        
        if user: # 로그인 되어있는 사용자라면 
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            all_comment = TweetComment.objects.all().order_by('-created_at')
            all_image = TweetComment.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet, 'comment': all_comment, 'image': all_image})
        else: # 로그인 되어있지 않다면
            return redirect('/sign-in')
        
    elif request.method == "POST":
        user = request.user
        content = request.POST.get('my-content')
        image = request.FILES.get('image', '')
        tags = request.POST.get('tag', '').split('#')
        
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/post-add.html', {'error':'글은 공백일 수 없습니다', 'tweet':all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content, image=image)  # 글쓰기 모델 가져오기
            my_tweet.author = user  # 모델에 사용자 저장
            my_tweet.content = request.POST.get('my-content', '')  # 모델에 글 저장
            for tag in tags:
                tag = tag.strip()
                if tag != '': # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')
    
    
@login_required    
def post_add(request):
    return render(request, 'tweet/post-add.html') 


@login_required
def post_edit(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    
    if request.method == 'POST':
        my_tweet.content = request.POST.get('my-content')
        my_tweet.image = request.FILES.get('image', '')
        
        if my_tweet.content == '' or my_tweet.image == '' :
            my_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/post-edit.html', {'error':'글과 이미지는 공백일 수 없습니다.'})
            
        my_tweet.save()
        return redirect('/tweet/')
    
    else :
        return render(request, 'tweet/post-edit.html', {'tweet':my_tweet})
        


@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet':my_tweet, 'comment':tweet_comment})


@login_required
def write_comment(request, id):
    if request.method == "POST":
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)
        
        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()
        
        return redirect('/tweet/'+str(id))
    
    
@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))


@login_required
def mainpage_write_comment(request, id):
    if request.method == "POST":
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)
        
        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()
        
        return redirect('/tweet/')
    
    
@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet/')



# 태그 기능
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context