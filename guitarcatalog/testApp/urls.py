from django.urls import path, re_path, register_converter
from testApp.views import *
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")
'''
urlpatterns = [
    path('', index, name='home'), #http://127.0.0.1:8000/testApp/
    path('cats/<int:catID>/', categories), #http://127.0.0.1:8000/testApp/cats/
    path('cats/<slug:catSlug>/', categories_by_slug), #http://127.0.0.1:8000/testApp/cats/

    #re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
    path('archive/<year4:year>/', archive),

    path('about/', about, name='about')
]
'''

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    #path('post/<int:post_id>/', show_post, name='post'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    #path('category/<int:cat_id>/', show_category, name='category'),
    path('category/<slug:cat_slug>/', show_category, name='category'),
    path('tag/<slug:tag_slug>/', show_tag_postlist, name='tag'),
]
