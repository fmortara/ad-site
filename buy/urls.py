from django.urls import path

from .import views

urlpatterns = [
    path('ask/<int:pk>/', views.ask, name='ask'),
    path('ask/', views.ask, name='ask'),
    path('ask-complete/', views.ask_complete , name='ask-complete'),
    path('ask-admin/', views.QuestionListView.as_view(), name='ask-admin'),
    path('message-admin/', views.message_admin, name='message-admin'),
    path('message-reply/', views.message_reply, name='message-reply'),
]