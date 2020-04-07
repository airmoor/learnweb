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
    'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code'])
    intro = models.CharField(max_length=250)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('body'),
    ]
    class Meta:
        ordering = ['title']



class BlogIndexPage(Page):
    type = models.CharField(max_length=5, default='index')
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('title')
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


class TestPage(Page):
    type = models.CharField(max_length=4, default='test')
   
    answer1 = models.CharField(max_length=250)
    answer2 = models.CharField(max_length=250)
    answer3 = models.CharField(max_length=250)
    answer4 = models.CharField(max_length=250)

    status1 = models.CharField(max_length=1, choices=STATUS_CHOICES)
    status2 = models.CharField(max_length=1, choices=STATUS_CHOICES)
    status3 = models.CharField(max_length=1, choices=STATUS_CHOICES)
    status4 = models.CharField(max_length=1, choices=STATUS_CHOICES)
    # answers = ClusterTaggableManager(blank=True, default = )
    content_panels = Page.content_panels + [
        
        # FieldPanel('question'),
        MultiFieldPanel([
            FieldPanel('answer1'),
            FieldPanel('status1'),
            FieldPanel('answer2'),
            FieldPanel('status2'),
            FieldPanel('answer3'),
            FieldPanel('status3'),
            FieldPanel('answer4'),
            FieldPanel('status4'),
           
        ], heading="Blog information"),
     
    ]



# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     panels = [
#         FieldPanel('question_text')
#     ]

#     def __str__(self):
#         return self.question_text


# class Answer(models.Model):
#     answer_text = models.CharField(max_length=200)
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES)

#     panels = [
#         FieldRowPanel([
#             FieldPanel('answer_text'),
#             FieldPanel('status')
#         ], heading="Варианты ответа")
#     ]

#     def __str__(self):
#         return self.answer_text        


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES)

#     def __str__(self):
#         return self.choice_text


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['question_text']})
#     ]
#     inlines = [ChoiceInline]
    
#     class Meta:
#         abstract = True


 

# class QuestionAnswer(Orderable, Answer):
#     # answer_text = models.CharField(max_length=200)
#     # status = models.CharField(max_length=1, choices=STATUS_CHOICES)
#     page = ParentalKey('QuestionPage', on_delete=models.CASCADE, related_name='questionanswer')


#     # panels = [
#     #     FieldRowPanel([
#     #         FieldPanel('answer_text'),
#     #         FieldPanel('status')
#     #     ], heading="Варианты ответа")
#     # ]

#     # def __str__(self):
#     #     return self.answer_text    
    

# class QuestionPage(Page):
#     type = models.CharField(max_length=8, default='question')
#     content_panels = Page.content_panels + [
        
#         InlinePanel('questionanswer', label='Варианты ответа', min_num=2, max_num=10),
     
#     ]
#     def get_context(self, request):
#         context = super().get_context(request)
#         pages = self.get_children().live()
#         answers = get_all_child_relations(self)

#         return context
        

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


