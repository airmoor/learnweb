# from wagtail.contrib.modeladmin.options import (
#     ModelAdmin, ModelAdminGroup, modeladmin_register
# )
# from django.contrib import admin
# from .models import Question, Choice

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

# class QuestionAdmin(ModelAdmin):
#     model = Question
#     fieldsets = [
#         (None, {'fields': ['question_text']})
#     ]
#     inlines = [ChoiceInline]
#     search_fields = ['question_text']
    


# class ChoiceAdmin(ModelAdmin):
#     model = Choice

# class QuestionGroup(ModelAdminGroup):
#     items = (QuestionAdmin, ChoiceInline) 
#     menu_label = 'Тесты'


# modeladmin_register(QuestionGroup)