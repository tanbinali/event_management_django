from django.urls import path
from . import views
from .views import (
    EventListView, EventDetailView,
    EventCreateView, EventUpdateView, EventDeleteView,
    CategoryCreateView, UserListView
)

urlpatterns = [
    path('', views.home_view, name='home'),

    # Event URLs
    path('events/', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('events/manage/', views.event_manage, name='event_manage'),
    path('event/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),

    # Dashboard & Search
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('redirect-dashboard/', views.dashboard_redirect, name='redirect_dashboard'),
    path('search/', views.event_search, name='event_search'),
    path('filtered-events/', views.filter_by_date_range, name='filtered_events'),

    # Category URLs
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/manage/', views.category_manage, name='category_manage'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # User URLs
    path('users/manage/', UserListView.as_view(), name='user_manage'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
] 
