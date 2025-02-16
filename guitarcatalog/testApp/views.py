from django.http import HttpResponse, HttpResponseNotFound,  Http404
from django.shortcuts import render, redirect, get_object_or_404
from testApp.models import TestApp, Category, TagPost, UploadFiles
from testApp.forms import AddPostForm, UploadFileForm
import uuid
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
    posts = TestApp.objects.filter(is_published=1)
    #posts = TestApp.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': TestApp.published.all(),
        'cat_selected': 0,
    }
    return render(request, 'testApp/index.html', context=data)

def show_post(request, post_slug):
    post = get_object_or_404(TestApp, slug=post_slug)
    data = {'title': post.title,
            'menu': menu,
            'post': post,
            'cat_selected': 0,
            }
    return render(request, 'testApp/post.html', context=data)

def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]

    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
            #handle_uploaded_file(form.cleaned_data['file'])
        #handle_uploaded_file(request.FILES['file_upload'])
    else:
        form = UploadFileForm()
    return render(request, 'testApp/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'testApp/addpage.html',
        {'menu': menu,
         'title': 'Добавление статьи',
         'form': form})

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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = TestApp.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'testApp/index.html', context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=TestApp.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tags}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'testApp/index.html', context=data)
