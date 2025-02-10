from django.http import HttpResponse, HttpResponseNotFound,  Http404
from django.shortcuts import render, redirect, get_object_or_404
from testApp.models import TestApp
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify


menu = [
 {'title': "О сайте", 'url_name': 'about'},
 {'title': "Добавить статью", 'url_name': 'add_page'},
 {'title': "Обратная связь", 'url_name': 'contact'},
 {'title': "Войти", 'url_name': 'login'}
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
    #posts = TestApp.objects.filter(is_published=1)
    posts = TestApp.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'testApp/index.html', context=data)

def show_post(request, post_slug):
    post = get_object_or_404(TestApp, slug=post_slug)
    data = {'title': post.title,
            'menu': menu,
            'post': post,
            'cat_selected': 1,
            }
    return render(request, 'testApp/post.html', context=data)

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
        'posts': TestApp.published.all(),
        'cat_selected': cat_id,
    }
    return render(request, 'testApp/index.html', context=data)
