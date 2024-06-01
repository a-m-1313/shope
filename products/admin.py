from django.contrib import admin
from .models import Product, Comment
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin


class ProductCommentsInline(admin.TabularInline):
    model = Comment
    field = ('title', 'active', 'author', )
    extra = 0


@admin.register(Product)
class PageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    model = Product
    list_display = ('title',  'get_created_jalali', 'get_modified_jalali', 'active', 'price', )
    list_editable = ['price', 'active']
    inlines = [ProductCommentsInline]

    @admin.display(description='تاریخ ایجاد', ordering='created')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_time).strftime('%d / %m / %Y / %H:%M:%S')

    @admin.display(description='تاریخ تغییر', ordering='modified')
    def get_modified_jalali(self, obj):
        return datetime2jalali(obj.date_modified).strftime('%d / %m / %Y / %H:%M:%S')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('author', 'get_created_jalali', 'get_modified_jalali',  'product', 'active')

    @admin.display(description='تاریخ ایجاد', ordering='created')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_add).strftime('%d / %m / %Y / %H:%M:%S')

    @admin.display(description='تاریخ تغییر', ordering='modified')
    def get_modified_jalali(self, obj):
        return datetime2jalali(obj.date_modified).strftime('%d / %m / %Y / %H:%M:%S')