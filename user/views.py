from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from user.models import UserModel #사용자가 있는지 검사하는 함수
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == "GET":
        # 로그인된 사용자가 요청하는 것인지 검사
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else: #로그인 안되어있으면 다시 회원가입 화면 보여주기
            return render(request, 'user/signup.html')
    elif request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '')
        bio = request.POST.get('bio', None)
        
        if password != password2:
            return render(request, 'user/signup.html', {'error: 패스워드가 일치하지 않습니다!'})
        else:
            if username == '' or password == '' or first_name == '' :
                return render(request, 'user/signup.html',{'error':'빈칸을 모두 채워주세요!'})
            
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
                return render(request, 'user/signup.html', {'error': '사용자가 이미 존재합니다!'}) 
            else:
                UserModel.objects.create_user(username=username, password=password, first_name=first_name)
                return redirect('/sign-in')
            
            
def sign_in_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        me = auth.authenticate(request, username=username, password=password)
        # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
        if me is not None:
            auth.login(request, me)
            return redirect('/tweet')
        else:
            return render(request, 'user/signin.html', {'error':'유저이름 혹은 패스워드를 확인해주세요! '})
        
    elif request.method == "GET":
        # 로그인된 사용자가 요청하는 것인지 검사
        user = request.user.is_authenticated
        if user: 
            return redirect('/tweet')
        else: #로그인이 되어있지 않으면
            return render(request, 'user/signin.html')
        
        
@login_required
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")
            
            
@login_required
def user_view(request):
    if request.method == "GET":
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})
    
    
@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')


@login_required
def profile(request):
    return render(request, 'user/profile.html')


@login_required
def change_profile(request):
    if request.method == 'POST':
        user_image = request.user
        user_image.profile = request.FILES.get('profile','')
        user_image.save()

        return render(request, 'user/profile.html')
            
    elif request.method == 'GET':
        user_image = UserModel()
        return render(request, 'user/change_profile.html',{'profile':user_image})


@login_required
def profile_change(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/profile.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        first_name = request.POST.get('first_name','')
        bio = request.bio.POST.get('post','')
        
        