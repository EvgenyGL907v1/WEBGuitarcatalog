from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify


menu = [
 {'title': "О сайте", 'url_name': 'about'},
 {'title': "Добавить статью", 'url_name': 'add_page'},
 {'title': "Обратная связь", 'url_name': 'contact'},
 {'title': "Войти", 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': 'Гитара 1', 'content':
    '''<h1>Акустическая гитара YAMAHA F310</h1> Прекрасный звук и отличное качество изготовления по демократичной цене - отличительные особенности гитары серии F.
    Эта гитара способна передавать самые тонкие оттенки настроения, ее можно назвать совершенным инструментом.
    Традиционный дизайн дредноутов в сочетании с громким акустическим звучанием и
    хорошими игровыми качествами делают этот инструмент идеальным выбором.
    Юные гитаристы по достоинству оценят комфорт при игре благодаря немного уменьшенной глубине корпуса и средней длине мензуры.
    Тип гитары: вестерн
    Материал верхней деки: ель
    Материал накладки: яванский палисандр
    Корпус: индонезийское красное дерево
    Глубина корпуса: 96-116 мм
    Материал обечаек: индонезийское красное дерево
    Гриф: красное дерево
    Материал струнодержателя: палисандр Сонокелинг
    Колки: хром''',
     'is_published': True},
    {'id': 2, 'title': 'Гитара 2', 'content':
        'Описание гитары 2', 'is_published': False},
    {'id': 3, 'title': 'Гитара 3', 'content':
        'Описание гитары 3', 'is_published': True},
]

cats_db = [
 {'id': 1, 'name': 'Классические гитары'},
 {'id': 2, 'name': 'Акустические гитары'},
 {'id': 3, 'name': 'Электрогитары'},
 {'id': 4, 'name': 'Бас-гитары'},
]

class MyClass:
 def __init__(self, a, b):
  self.a = a
  self.b = b

def index(request):
 #return HttpResponse("Страница приложения testApp.")
 #return HttpResponse(render_to_string('testApp/index.html'))
 #return render(request, 'testApp/index.html')
 #return render(request, 'testApp/index.html', {'title': 'Главная страница'})
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,
    }
    return render(request, 'testApp/index.html', context=data)

def show_post(request, post_id):
 return HttpResponse(f"Отображение статьи с id = {post_id}")

def addpage(request):
 return HttpResponse("Добавление статьи")

def contact(request):
 return HttpResponse("Обратная связь")

def login(request):
 return HttpResponse("Авторизация")

def categories(request, catID):
 return HttpResponse(f"<h1>Статьи по категориям</h1><p> int:{catID}<p>")


def categories_by_slug(request, catSlug):
 if request.GET:
  print(request.GET)
 return HttpResponse(f"<h1>Статьи по категориям</h1><p > slug:{ catSlug }</p>")

def archive(request, year):
 if year > 2023:
  #raise Http404()
  return redirect('home', permanent=True)
 return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def page_not_found(request, exception):
 return HttpResponseNotFound('<h1>Страница не найдена</h1>')


#def about(request):
 #return render(request, 'base.html', {'title': 'О сайте', 'menu': menu})

def about(request):
 return render(request, 'testApp/about.html', {'title': 'О сайте', 'menu': menu})

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'testApp/index.html', context=data)
