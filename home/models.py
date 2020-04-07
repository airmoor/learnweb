from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel



class HomePage(Page):
    body = RichTextField(blank=True)
    type = models.CharField(max_length=4, default='home')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        mainpages = self.get_children().live().order_by('title')
        context['mainpages'] = mainpages
        context['pages'] = Page.objects.live()
        return context

