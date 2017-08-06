from django.contrib import admin
from django.forms import ModelForm

from django import forms
from .models import *


def make_published(modeladmin, request, queryset):
    print (request)
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']
    actions = [make_published]

class ChoiceEdit(forms.ModelForm):
    pass

class ChoiceAdmin(admin.ModelAdmin):
    exclude = ('votes', )

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'state', ]



class QuestionInLine(admin.TabularInline):
    model = Choice
    

class QuestionChoice(admin.ModelAdmin):

    my_choice = {}
    my_choice['choice_text'] = (('New', 'Новый'),('Active', 'Активный'),)
    def change_view(self, request, object_id, form_url='', extra_context=None):
        State = Question.objects.get(pk=object_id).state
        QuestionInLine.readonly_fields = ''

        if State == 'New':
            QuestionChoice.inlines = [QuestionInLine, ]
            QuestionInLine.exclude = ('votes', )
            form = QuestionForm
            #qs = super(QuestionChoice, self).get_queryset(request).filter(state = 'New')
        if State == 'Active':
            QuestionChoice.inlines = [QuestionInLine, ]
            QuestionInLine.readonly_fields = (Question, )
            QuestionInLine.exclude = ''
        if State == 'Ended':
            QuestionChoice.inlines = ''

        return super(QuestionChoice, self).change_view(request, object_id, form_url, extra_context)
    
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = QuestionForm
        return super(QuestionChoice, self).get_form(request, obj, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        save_url_id = request.get_full_path().split('/')[4]
        state = Question.objects.get(pk=save_url_id).state

        if db_field.name == 'state' and state == 'New':
            kwargs['choices'] = (
                ('New', 'Новый'),
                ('Active', 'Активный'),
            )
        if db_field.name == 'state' and state == 'Active':
                kwargs['choices'] = (
                ('Active', 'Активный'),
                ('Ended', 'Конечный'),
            )
        if db_field.name == 'state' and state == 'Ended':
                kwargs['choices'] = (
                ('Ended', 'Конечный'),
            )  
        return super(QuestionChoice, self).formfield_for_choice_field(db_field, request, **kwargs)

#admin.site.register(Article, ArticleAdmin)
admin.site.register(Question, QuestionChoice)