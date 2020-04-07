# 
from django.views.generic.list import ListView #показывает список всех статей на сайте
from django.views.generic.detail import DetailView 
from wagtail.core.models import Page, Orderable
from home.models import HomePage
from blog.models import BlogPage, BlogIndexPage



class SectionsListView(ListView): #класс листа статей
    model = HomePage
    template_name = 'includes/aside.html' #в какой шаблон показывать лист статей
	#template_name='all.html'

    def get_context_data(self, *args, **kwargs): #
        context=super(SectionsListView, self).get_context_data(*args, **kwargs)
        context['sections']=self.model.objects.all()
        # context['pages']=HomaPage.objects.all()
        context['pages'] = self.get_children().live().order_by('title')
        # all_articles=Article.objects.all()
        # context['article']=all_articles[0]
        # context['slider_articles']=Article.objects.all().order_by('?')[:5]

        # context['pop_articles']=Article.objects.last()
        return context

# class SectionsDetailView(DetailView, CategoryListMixin):
#     model = HomePage
#     template_name='includes/aside.html' #в какой шаблон показывать лист статей

#     def get_context_data(self, *args, **kwargs): #
#         context=super(SectionsDetailView, self).get_context_data(*args, **kwargs)
#         context['categorcatsies']=self.model.objects.all()
#         context['category']=self.get_object()
#         current_category=self.get_object()
#         context['articles_from_category']=self.get_object().article_set.all().filter(category=current_category)  #
#         return context