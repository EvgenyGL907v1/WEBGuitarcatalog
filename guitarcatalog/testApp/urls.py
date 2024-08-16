from django.urls import path, re_path, register_converter
from testApp.views import *
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', index, name='home'), #http://127.0.0.1:8000/testApp/
    path('cats/<int:catID>/', categories), #http://127.0.0.1:8000/testApp/cats/
    path('cats/<slug:catSlug>/', categories_by_slug), #http://127.0.0.1:8000/testApp/cats/

    #re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
    path('archive/<year4:year>/', archive),
]
