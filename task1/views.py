from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserRegister
from .models import Game, Buyer, News
from django.core.paginator import Paginator


# Create your views here.
def sign_up_by_html(request):
    users = Buyer.objects.all()  # ['Незнайка', 'Пончик', 'Торопыжка', 'Знайка', 'Пилюлькин']
    info = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        error_message = ''

        exists = False
        for u in users:
            if username == u.name:
                exists = True
        if exists:
            error_message += 'Пользователь уже существует\n'

        if password != repeat_password:
            error_message += 'Пароли не совпадают\n'
        try:
            age = int(age)
            # Проверку на возраст убрал т.к. в базе есть игры, доступные для детей
        except:
            error_message += 'Возраст должен быть целым числом\n'

        print('sign_up_by_html(request):')
        print(f'username = "{username}"')
        print(f'password = "{password}"')
        print(f'repeat_password = "{repeat_password}"')
        print(f'age = "{age}"')
        print(info)

        if not error_message:
            Buyer.objects.create(name=username, balance=0, age=age)
            return HttpResponse(f'Приветствуем, {username}!')
        else:
            info['error'] = error_message
            return render(request, 'ans.html', context=info)
    return render(request, 'registration_page.html')


def sign_up_by_django(request):
    # Этот метод работает, но не используется в проекте (жалко удалять)
    users = ['Незнайка', 'Пончик', 'Торопыжка', 'Знайка', 'Пилюлькин']
    info = {}

    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            '''
            1.'Пароли не совпадают', если не совпали введённые пароли.
            2.'Вы должны быть старше 18', если возраст меньше 18.
            3.'Пользователь уже существует', если username есть в users.
            '''
            error_message = ''
            if password != repeat_password:
                error_message += 'Пароли не совпадают\n'
            try:
                age = int(age)
                if age < 18:
                    error_message += 'Вы должны быть старше 18\n'
            except:
                error_message += 'Возраст должен быть целым числом\n'
            if username in users:
                error_message += 'Пользователь уже существует\n'

            print('sign_up_by_django(request):')
            print(f'username = "{username}"')
            print(f'password = "{password}"')
            print(f'repeat_password = "{repeat_password}"')
            print(f'age = "{age}"')
            print(info)

            if not error_message:
                users.append(username)
                return HttpResponse(f'Приветствуем, {username}!')
            else:
                info['error'] = error_message
                return render(request, 'ans.html', context=info)
    else:
        form = UserRegister()
    return render(request, 'djangoform.html', {'form': form})


def index4(request):
    return render(request, 'index.html')


def shop4(request):
    items = Game.objects.all()
    context = {'items': items}
    return render(request, 'shop.html', context)


def cart4(request):
    return render(request, 'cart.html')


def news4(request):
    news = News.objects.all()
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'news': page_obj}
    return render(request, 'news.html', context)