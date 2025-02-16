from django import forms
from .models import *
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

class AddPostForm(forms.ModelForm):
    '''title = forms.CharField(max_length=255,
                            label="Заголовок",
                            min_length= 5,
                            )
    widget = forms.TextInput(attrs={'class': 'form-input'})
    slug = forms.SlugField(max_length=255, label="URL",
                        validators=[
                            MinLengthValidator(3),
                            MaxLengthValidator(100)
                        ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
                              required=False,
                              label="Контент")
    is_published = forms.BooleanField(required=False, initial=True, label="Статус публикации")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    article = forms.ModelChoiceField(queryset=Article.objects.all(), empty_label="Не выбрано", required=False, label="Артикул")
'''
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label="Категория не выбрана",
                                 label="Категории")
    article = forms.ModelChoiceField(queryset=Article.objects.all(),
                                     required=False,
                                     empty_label="Не заполнено",
                                     label="Артикул")

    class Meta:
        model = TestApp
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'article', 'tags'] # 'photo',
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
                   }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50: raise ValidationError('Длина превышает 50 символов')
        return title

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")
