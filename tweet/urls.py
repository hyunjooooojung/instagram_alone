# tweet/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.tweet, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('tweet/', views.tweet, name='tweet'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
   
    # 게시글, 댓글
    path('tweet/<int:id>', views.detail_tweet, name='detail-tweet'),
    path('tweet/comment/<int:id>', views.write_comment, name='write-comment'),
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('tweet/home/comment/<int:id>', views.mainpage_write_comment, name='mainpage-write-comment'),
    
    # 게시글 추가하기, 수정하기
    path('post-add/', views.post_add, name='post-add'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)