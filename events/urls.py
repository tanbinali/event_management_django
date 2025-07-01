from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:pk>/update/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search/', views.event_search, name='event_search'),
    path('filtered-events/', views.filter_by_date_range, name='filtered_events'),
    path('participants/create/', views.participant_create, name='participant_create'),
    path('categories/create/', views.category_create, name='category_create'),
    path('participants/manage/', views.participant_manage, name='participant_manage'),
    path('categories/manage/', views.category_manage, name='category_manage'),
    path('participants/<int:pk>/update/', views.participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

]
