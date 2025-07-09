from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:pk>/update/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search/', views.event_search, name='event_search'),
    path('filtered-events/', views.filter_by_date_range, name='filtered_events'),
    path('categories/create/', views.category_create, name='category_create'),
    path('participants/manage/', views.participant_manage, name='participant_manage'),
    path('categories/manage/', views.category_manage, name='category_manage'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('event/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('participant_dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('redirect-dashboard/', views.dashboard_redirect, name='redirect_dashboard'),
    path('events/manage/', views.event_manage, name='event_manage'),
    path('participants/', views.participant_list, name='participant_list'),
    path('participants/manage/', views.participant_manage, name='participant_manage'),
    path('participants/add/', views.participant_create, name='participant_create'),
    path('participants/<int:pk>/update/', views.participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),

]
