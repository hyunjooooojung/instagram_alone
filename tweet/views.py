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