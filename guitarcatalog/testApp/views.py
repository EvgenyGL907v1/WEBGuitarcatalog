from django.contrib.auth.decorators import login_required, permission_required
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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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


class TestAppHome(DataMixin, ListView):
    template_name = 'testApp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0)

    def get_queryset(self):
        return TestApp.published.all().select_related('cat')


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

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    model = TestApp
    permission_required = 'testApp.add_testapp'
    #form_class = AddPostForm
    fields = ['title', 'slug', 'content', 'photo',
              'is_published', 'cat', 'article', 'tags']
    template_name = 'testApp/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = TestApp
    permission_required = 'testApp.change_testapp'
    fields = ['title', 'slug', 'content', 'photo',
              'is_published', 'cat', 'article', 'tags']
    template_name = 'testApp/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'

class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    model = TestApp
    permission_required = 'testApp.delete_testapp'
    template_name = 'testApp/deletepage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

@permission_required(perm='testApp.view_testapp', raise_exception=True)
def contact(request):
    return HttpResponse("Обратная связь")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def login(request):
    return HttpResponse("Авторизация")

@login_required
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

class TestAppCategory(DataMixin, ListView):
    template_name = 'testApp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat

        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id)

    def get_queryset(self):
        return TestApp.published.filter(cat__slug=self.kwargs['cat_slug' ]).select_related('cat')

class TagPostList(DataMixin, ListView):
    template_name = 'testApp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return TestApp.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
