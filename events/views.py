from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch
from django.contrib.auth.models import User, Group
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps
from datetime import date, datetime

from .models import Event, Category, RSVP
from .forms import EventForm, CategoryForm, UserForm

# ---------- Home ----------
def home_view(request):
    return render(request, 'events/home.html')

# ---------- Permissions ----------
def group_required(group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and (user.is_superuser or user.groups.filter(name__in=group_names).exists()):
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'users/no_perm.html', status=403)
        return _wrapped_view
    return decorator

def admin_required(view_func):
    return group_required(['Admin'])(view_func)

def organizer_required(view_func):
    return group_required(['Organizer'])(view_func)

def participant_required(view_func):
    return group_required(['Participant'])(view_func)

def admin_or_organizer_required(view_func):
    return group_required(['Admin', 'Organizer'])(view_func)

# ---------- Event Views ----------
@login_required
def event_list(request):
    user = request.user
    is_admin_or_organizer = (
        user.is_superuser or
        user.groups.filter(name__in=['Admin', 'Organizer']).exists()
    )
    is_participant = user.groups.filter(name='Participant').exists()

    events = Event.objects.all()
    categories = Category.objects.all()

    context = {
        'events': events,
        'categories': categories,
        'is_admin_or_organizer': is_admin_or_organizer,
        'is_participant': is_participant,
    }
    return render(request, 'events/event_list.html', context)

@login_required
def event_detail(request, pk):
    event = get_object_or_404(
    Event.objects.select_related('category').prefetch_related('participants'),
    pk=pk
)
    user = request.user
    is_admin_or_organizer = user.is_superuser or user.groups.filter(name__in=['Admin', 'Organizer']).exists()

    participants = []
    for p in event.participants.all():
        display_name = p.get_full_name() if p.get_full_name() else p.username
        participants.append({
            'name': display_name,
            'email': p.email
        })

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_admin_or_organizer': is_admin_or_organizer,
        'participants': participants
    })

@admin_or_organizer_required
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})

@admin_or_organizer_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})

@admin_or_organizer_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@admin_or_organizer_required
def event_manage(request):
    user = request.user
    events = Event.objects.select_related('category') if user.is_superuser or user.groups.filter(name="Organizer").exists() else Event.objects.none()
    return render(request, 'events/event_manage.html', {'events': events})

@login_required
def event_search(request):
    search = request.GET.get('search', '')
    events = Event.objects.filter(
        Q(name__icontains=search) |
        Q(description__icontains=search) |
        Q(location__icontains=search) |
        Q(category__name__icontains=search)
    ).select_related('category').distinct()
    categories = Category.objects.all()
    return render(request, 'events/event_search.html', {
        'events': events,
        'search': search,
        'categories': categories
    })

@login_required
def filter_by_date_range(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    events = Event.objects.select_related('category')
    if start_date:
        try:
            start_date_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            events = events.filter(date__gte=start_date_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_date_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            events = events.filter(date__lte=end_date_dt)
        except ValueError:
            pass
    events = events.order_by('date')
    return render(request, 'events/filtered_events.html', {
        'events': events,
        'start_date': start_date or '',
        'end_date': end_date or '',
        'categories': Category.objects.all(),
        'today': now().date()
    })

# ---------- RSVP & Dashboards ----------
@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    rsvp, created = RSVP.objects.get_or_create(user=user, event=event)
    if created:
        rsvp.status = 'confirmed'
        rsvp.save()
        event.participants.add(user)
        participant_group, _ = Group.objects.get_or_create(name='Participant')
        user.groups.add(participant_group)
    return redirect('user_dashboard')

@login_required
def user_dashboard(request):
    user = request.user
    rsvped_events = user.rsvped_events.select_related('category').order_by('date')
    return render(request, 'events/user_dashboard.html', {
        'rsvped_events': rsvped_events,
    })

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_superuser or user.groups.filter(name__in=['Admin', 'Organizer']).exists():
        return redirect('dashboard')
    elif user.groups.filter(name='Participant').exists():
        return redirect('user_dashboard')
    return redirect('event_list')

@admin_or_organizer_required
def dashboard_view(request):
    today = date.today()
    all_events = Event.objects.all()
    context = {
        'events_today': all_events.filter(date=today),
        'upcoming_events': all_events.filter(date__gt=today),
        'past_events': all_events.filter(date__lt=today),
        'all_events': all_events,
        'total_events': all_events.count(),
        'upcoming': all_events.filter(date__gt=today).count(),
        'past': all_events.filter(date__lt=today).count(),
        'users': User.objects.select_related().all(),
        'organizers': User.objects.filter(groups__name='Organizer'),
        'participants': User.objects.filter(groups__name='Participant'),
        'is_admin': request.user.is_superuser or request.user.groups.filter(name='Admin').exists(),
        'is_organizer': request.user.groups.filter(name='Organizer').exists(),
    }
    return render(request, 'events/dashboard.html', context)

# ---------- Category Views ----------
@admin_or_organizer_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/category_form.html', {'form': form})

@admin_or_organizer_required
def category_manage(request):
    categories = Category.objects.all()
    return render(request, 'events/category_form.html', {'categories': categories})

@admin_or_organizer_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_manage')
    return render(request, 'events/category_form.html', {'form': form})

@admin_or_organizer_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_manage')
    return render(request, 'events/category_confirm_delete.html', {'category': category})

# ---------- User Views ----------
@admin_required
def user_manage(request):
    users = User.objects.all().prefetch_related('groups')
    return render(request, 'events/user_manage.html', {'users': users})

@admin_required
def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user_manage')
    return render(request, 'events/user_form.html', {'form': form})

@admin_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user_manage')
    return render(request, 'events/user_form.html', {'form': form})

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_manage')
    return render(request, 'events/user_confirm_delete.html', {'user': user})
