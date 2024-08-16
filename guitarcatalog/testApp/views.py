from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

def index(request):
 return HttpResponse("Страница приложения testApp.")

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
