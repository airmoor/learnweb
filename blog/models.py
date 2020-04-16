from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import admin

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import get_all_child_relations
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel,FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


STATUS_CHOICES = [
    ('0', 'Неверный'), 
    ('1', 'Верный'), 
]

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
    type = models.CharField(max_length=4, default='blog')
    body = RichTextField(blank=True, features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
    'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code'],
    verbose_name="Содержание")
    intro = models.CharField(max_length=250, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True, verbose_name="Категории")
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Информация"),
        FieldPanel('body'),
    ]
    class Meta:
        ordering = ['id']
        # ordering = ['title']

    class Meta:
        verbose_name = 'Страница с теорией'



class BlogIndexPage(Page):
    type = models.CharField(max_length=5, default='index')
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        # blogpages = self.get_children().live().order_by('title')
        blogpages = self.get_children().live().order_by('id')
        context['blogpages'] = blogpages
        
        context['parents'] = self.get_ancestors()

        context['pages'] = Page.objects.live()

        paginator = Paginator(blogpages, 1)

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts

        return context

    class Meta:
        verbose_name = 'Страница раздела'



class QuestionAnswer(Orderable):
    page = ParentalKey('QuestionPage', on_delete=models.CASCADE, related_name='questionanswer')
    answer_text = models.CharField(max_length=200, verbose_name="Ответ")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="Статус")

    panels = [
        FieldRowPanel([
            FieldPanel('answer_text'),
            FieldPanel('status')
        ], heading="Варианты ответа")
    ]  
    

class QuestionPage(Page):
    type = models.CharField(max_length=8, default='question')
    content_panels = Page.content_panels + [
        InlinePanel('questionanswer', label='Варианты ответа', min_num=2, max_num=10),
    ]
    def get_context(self, request):
        context = super().get_context(request)
        pages = self.get_children().live()
        return context
    
    def answers(self):
        answers = [
            n for n in self.questionanswer.all()
        ]
        return answers

    class Meta:
        verbose_name = 'Страница вопроса'



@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'

