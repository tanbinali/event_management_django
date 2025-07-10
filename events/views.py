from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Event, Category, RSVP
from django.contrib.auth.models import User, Group
from .forms import EventForm, CategoryForm, ParticipantForm
from datetime import date, datetime
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib import messages

def home_view(request):
    return render(request, 'events/home.html')

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

@login_required
def event_list(request):
    events = Event.objects.select_related('category').all()
    categories = Category.objects.all()
    participants = User.objects.filter(groups__name='Participant').only('id', 'username', 'email', 'first_name', 'last_name')
    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'participants': participants,
    })

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event.objects.select_related('category').prefetch_related('participants'), pk=pk)
    user = request.user
    is_admin_or_organizer = (
        user.is_superuser or user.groups.filter(name__in=['Admin', 'Organizer']).exists()
    )
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_admin_or_organizer': is_admin_or_organizer
    })

@admin_or_organizer_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
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
def dashboard_view(request):
    today = date.today()
    events_today = Event.objects.filter(date=today)
    upcoming_events = Event.objects.filter(date__gt=today)
    past_events = Event.objects.filter(date__lt=today)
    all_events = Event.objects.all()
    all_users = User.objects.all()
    organizers = User.objects.filter(groups__name='Organizer')
    participants = User.objects.filter(groups__name='Participant')
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
    is_organizer = request.user.groups.filter(name='Organizer').exists()
    context = {
        'events_today': events_today,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'all_events': all_events,
        'total_events': all_events.count(),
        'upcoming': upcoming_events.count(),
        'past': past_events.count(),
        'users': all_users,
        'organizers': organizers,
        'participants': participants,
        'is_admin': is_admin,
        'is_organizer': is_organizer,
    }
    return render(request, 'events/dashboard.html', context)

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

@admin_or_organizer_required
@login_required
def event_manage(request):
    user = request.user
    events = Event.objects.select_related('category').all() if user.is_superuser or user.groups.filter(name="Organizer").exists() else Event.objects.none()
    return render(request, 'events/event_manage.html', {'events': events})

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

@admin_or_organizer_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})

@admin_or_organizer_required
def category_manage(request):
    categories = Category.objects.all()
    return render(request, 'events/category_form.html', {'categories': categories})

@admin_or_organizer_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_manage')
    return render(request, 'events/category_confirm_delete.html', {'category': category})

@admin_or_organizer_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_manage')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form})

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
    return redirect('participant_dashboard')

@login_required
def participant_dashboard(request):
    user = request.user
    rsvped_events = user.rsvped_events.select_related('category').order_by('date')
    return render(request, 'events/participant_dashboard.html', {
        'rsvped_events': rsvped_events,
    })

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_superuser or user.groups.filter(name__in=['Admin', 'Organizer']).exists():
        return redirect('dashboard')
    elif user.groups.filter(name='Participant').exists():
        return redirect('participant_dashboard')
    else:
        return redirect('event_list')

@admin_required
def participant_list(request):
    participants = User.objects.filter(groups__name='Participant').only('id', 'username', 'email', 'first_name', 'last_name')
    return render(request, 'events/participant_list.html', {'participants': participants})

@admin_required
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_manage')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form})

@admin_required
def participant_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant updated successfully.')
            return redirect('participant_manage')
    else:
        form = ParticipantForm(instance=user)
    return render(request, 'events/participant_form.html', {'form': form})

@admin_required
def participant_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Participant deleted successfully.')
        return redirect('participant_manage')
    return render(request, 'events/participant_confirm_delete.html', {'user': user})

@admin_required
def participant_manage(request):
    participants = User.objects.filter(groups__name='Participant').only('id', 'username', 'email', 'first_name', 'last_name')
    return render(request, 'events/participant_manage.html', {'participants': participants})
