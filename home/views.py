# 
from django.views.generic.list import ListView #показывает список всех статей на сайте
from django.views.generic.detail import DetailView 
from wagtail.core.models import Page, Orderable
from home.models import HomePage
from blog.models import BlogPage, BlogIndexPage

class SectionsListView(ListView): #класс листа статей
    model = HomePage
    template_name = 'includes/aside.html' #в какой шаблон показывать лист статей

    def get_context_data(self, *args, **kwargs): #
        context=super(SectionsListView, self).get_context_data(*args, **kwargs)
        context['sections']=self.model.objects.all()
        context['pages'] = self.get_children().live().order_by('title')

        return context