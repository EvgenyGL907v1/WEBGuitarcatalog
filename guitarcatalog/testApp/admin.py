from django.contrib import admin
from django.core.checks import messages
from .models import *
from django.utils.safestring import mark_safe

#admin.site.register(TestApp)

class ViewFilter(admin.SimpleListFilter):
    title = 'Артикул'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('ishave', 'Есть'),
            ('havenot', 'Отсутствует'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'ishave':
            return queryset.filter(article__isnull=False)
        elif self.value() == 'havenot':
            return queryset.filter(article__isnull=True)

@admin.register(TestApp)
class TestAppAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [ViewFilter, 'cat__name', 'is_published']
    fields = ['title', 'slug', 'content', 'photo',
              'post_photo', 'cat', 'article', 'tags']
    #readonly_fields = ['slug']
    readonly_fields = ['post_photo']
    save_on_top = True

    @admin.display(description="Краткое описание")
    def brief_info(self, women: TestApp):
        return f"Описание {len(women.content)} символов."

    @admin.display(description="Изображение")
    def post_photo(self, testApp: TestApp):
        if testApp.photo:
            return mark_safe(f"<img src='{testApp.photo.url}' width=50>")
        return "Без изображения"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=TestApp.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=TestApp.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
