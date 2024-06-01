from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = RichTextField(verbose_name=_('Description'))
    short_description = models.TextField(verbose_name=_('short Description'), blank=True)
    price = models.PositiveIntegerField(default=0, verbose_name=_('price'))
    active = models.BooleanField(default=True, verbose_name=_('active'))
    media = models.ImageField(upload_to='cover/', blank=True, verbose_name=_('image'), default='cover/logo.jpg')

    date_time = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_view', args=[self.pk])

    def media_url(self):
        if self.media:
            return getattr(self.media, 'url', None)


class ActiveCommentManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentManager, self).get_queryset().filter(active=True)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('product'))
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name=_('comments author'))

    text = models.TextField(verbose_name=_("text comment"))
    active = models.BooleanField(default=True, verbose_name=_('active'))

    date_add = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_comment_manager = ActiveCommentManager()

    def get_absolute_url(self):
        return reverse('detail_view', args=[self.product.id])









