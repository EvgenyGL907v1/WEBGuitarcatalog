from django.http import HttpResponse, HttpResponseNotFound,  Http404
from django.shortcuts import render, redirect, get_object_or_404
from testApp.models import TestApp, Category, TagPost, UploadFiles
from testApp.forms import AddPostForm, UploadFileForm
import uuid
from django.views import View
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views.generic import TemplateView, ListView, DetailView
from testApp.utils import DataMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


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

'''
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
'''
class TestAppHome(DataMixin, ListView):
    template_name = 'testApp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0)

    def get_queryset(self):
        return TestApp.published.all().select_related('cat')

'''
def show_post(request, post_slug):
    post = get_object_or_404(TestApp, slug=post_slug)
    data = {'title': post.title,
            'menu': menu,
            'post': post,
            'cat_selected': 0,
            }
    return render(request, 'testApp/post.html', context=data)
'''
class ShowPost(DataMixin, DetailView):
    model = TestApp
    template_name = 'testApp/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'])

    def get_object(self, queryset=None):
        return (get_object_or_404
                (TestApp.published,
                 slug=self.kwargs[self.slug_url_kwarg]))

'''
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
'''
'''
class AddPage(View):
    form_class = AddPostForm
    template_name = 'testApp/addpage.html'

    def get(self, request):
        form = AddPostForm()
        return render(request, 'testApp/addpage.html',
            {'menu': menu, 'title': 'Добавление статьи', 'form': form})

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'testApp/addpage.html',
            {'menu': menu, 'title': 'Добавление статьи', 'form':form})
'''
'''
class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'testApp/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
'''
class AddPage(DataMixin, CreateView):
    model = TestApp
    #form_class = AddPostForm
    fields = ['title', 'slug', 'content', 'photo',
              'is_published', 'cat', 'article', 'tags']
    template_name = 'testApp/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = TestApp
    fields = ['title', 'slug', 'content', 'photo',
              'is_published', 'cat', 'article', 'tags']
    template_name = 'testApp/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'

class DeletePage(DataMixin, DeleteView):
    model = TestApp
    template_name = 'testApp/deletepage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

def contact(request):
    return HttpResponse("Обратная связь")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def login(request):
    return HttpResponse("Авторизация")

def about(request):
    contact_list = TestApp.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
            #handle_uploaded_file(form.cleaned_data['file'])
        #handle_uploaded_file(request.FILES['file_upload'])
    else:
        form = UploadFileForm()
    #return render(request, 'testApp/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})
    return render(request, 'testApp/about.html', {'page_obj': page_obj, 'title': 'О сайте'})

'''
def categories(request, catID):
 return HttpResponse(f"<h1>Статьи по категориям</h1><p> int:{catID}<p>")
'''

'''
def categories_by_slug(request, catSlug):
 if request.GET:
  print(request.GET)
 return HttpResponse(f"<h1>Статьи по категориям</h1><p > slug:{ catSlug }</p>")
'''

'''
def archive(request, year):
 if year > 2023:
  #raise Http404()
  return redirect('home', permanent=True)
 return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
'''

'''
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
'''
class TestAppCategory(DataMixin, ListView):
    template_name = 'testApp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        '''context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context'''
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id)

    def get_queryset(self):
        return TestApp.published.filter(cat__slug=self.kwargs['cat_slug' ]).select_related('cat')

'''
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
'''
class TagPostList(DataMixin, ListView):
    template_name = 'testApp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        '''context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context'''
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return TestApp.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
