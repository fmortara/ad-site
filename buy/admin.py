from django.contrib import admin

# Register your models here.
from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email', 'to_email', 'message', 'status')
    list_editable = ('status',)
    list_filter = ('data_cria',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('nome', 'mensagem', 'status', 'approved', 'data_resp')
    list_editable = ('status', 'approved')
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)