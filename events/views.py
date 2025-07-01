from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from datetime import date, datetime
from django.utils.timezone import now

def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participant_set')
    categories = Category.objects.all()
    participants = Participant.objects.all()
    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'participants': participants,
    })

def event_detail(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('participant_set'), pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def dashboard_view(request):
    today = date.today()

    events_today = Event.objects.filter(date=today)
    upcoming_events = Event.objects.filter(date__gt=today)
    past_events = Event.objects.filter(date__lt=today)
    all_events = Event.objects.all()

    total_events = all_events.count()
    total_participants = Participant.objects.aggregate(total=Count('id'))['total']
    participants = Participant.objects.all()

    context = {
        'events_today': events_today,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'all_events': all_events,
        'participants': participants,
        'total_events': total_events,
        'upcoming': upcoming_events.count(),
        'past': past_events.count(),
        'total_participants': total_participants,
    }

    return render(request, 'events/dashboard.html', context)

def event_search(request):
    search = request.GET.get('search', '')
    events = Event.objects.filter(
        Q(name__icontains=search) |
        Q(description__icontains=search) |
        Q(location__icontains=search) |
        Q(category__name__icontains=search)
    ).select_related('category').prefetch_related('participant_set')

    return render(request, 'events/event_search.html', {
        'events': events,
        'search': search,
        'categories': Category.objects.all()
    })

def filter_by_date_range(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    events = Event.objects.all().order_by('date')
    
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            events = events.filter(date__gte=start_date)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            events = events.filter(date__lte=end_date)
        except ValueError:
            pass
    
    return render(request, 'events/filtered_events.html', {
        'events': events,
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'categories': Category.objects.all(),
        'today': now().date()
    })

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list') 
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})

def participant_manage(request):
    participants = Participant.objects.all()
    return render(request, 'events/participant_form.html', {'participants': participants})

def category_manage(request):
    categories = Category.objects.all()
    return render(request, 'events/category_form.html', {'categories': categories})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_manage')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participant_form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_manage')
    return render(request, 'events/participant_confirm_delete.html', {
        'participant': participant
    })

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_manage')
    return render(request, 'events/category_confirm_delete.html', {'category': category})


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



