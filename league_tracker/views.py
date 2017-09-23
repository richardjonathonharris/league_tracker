from django.db.models import Count, Max, F
from django.shortcuts import render, get_object_or_404
from league_tracker.models import User, Records, Decks, Event
from league_tracker.forms import UserForm, DeckForm, RecordForm, EventForm, get_faction_dictionary 
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request): 
    return render(request, 'index.html')

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

def create_deck(request):
    if request.method == 'POST':
        runner_vals, corp_vals = get_faction_dictionary()
        payload = request.POST.copy()
        form = DeckForm(payload)
        form.save()
        updater = Decks.objects.last()
        updater.runner_faction = runner_vals[payload['runner_id']]
        updater.corp_faction = corp_vals[payload['corp_id']]
        updater.save()
        return HttpResponseRedirect('/')
    else:
        form = DeckForm()
    return render(request, 'add_decks.html', {'form': form})

def create_record(request):
    ### When somebody puts in a result we want to put in  reverse as well
    ### for example: user 3 sweeps user 1, we want to include a result for
    ### user 3 - user 1 6-0 points
    ### user 1 - user 3 0-6 points
    if request.method == 'POST':
        form = RecordForm(request.POST)
        reverse_form = request.POST.copy()
        original_form = request.POST.copy()
        form.save()
        reverse_form['opponent_id'] = request.POST['user_id']
        reverse_form['user_id'] = request.POST['opponent_id']
        flip_dict = {
                'WI': 'LO',
                'LO': 'WI',
                'TW': 'TL',
                'TL': 'TW',
                'TI': 'TI',
                }
        for stat in ['runner_status', 'corp_status']:
            reverse_form[stat] = flip_dict[request.POST[stat]]
        form = RecordForm(reverse_form)
        form.save()
        opp_record = Records.objects.last()
        opp_record.linked_record = opp_record.pk - 1
        opp_record.display = False
        opp_record.save()
        user_record = Records.objects.get(pk=opp_record.pk-1)
        user_record.linked_record = user_record.pk + 1
        user_record.save()
        return HttpResponseRedirect('/')
    else:
        form = RecordForm()
    return render(request, 'add_records.html', {'form': form})

def update_record(request, id):
    record = Records.objects.get(pk=id)
    form = RecordForm(request.POST or None, instance=record)
    if request.method == 'POST':
        form.save()
        linked_record = Records.objects.get(pk=record.linked_record)
        updated_record = Records.objects.get(pk=id)
        linked_record.user_id = updated_record.opponent_id
        linked_record.opponent_id = updated_record.user_id
        linked_record.game = updated_record.game
        linked_record.round_num = updated_record.round_num
        flip_dict = {
                'WI': 'LO',
                'LO': 'WI',
                'TW': 'TL',
                'TL': 'TW',
                'TI': 'TI',
                }
        linked_record.runner_status = flip_dict[updated_record.runner_status]
        linked_record.corp_status = flip_dict[updated_record.corp_status]
        linked_record.save()
        return HttpResponseRedirect('/')
    return render(request, 'update_records.html', {'form': form, 'id': id})

def delete_record(request, id):
    record = Records.objects.filter(id=id)
    partner = record[0].linked_record
    Records.objects.filter(id=id).delete()
    Records.objects.filter(id=partner).delete()
    return HttpResponseRedirect('/')
    

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def return_all_standings(request):
    all_records = Records.objects.all()
    context = {
            'record': all_record,
            }
    return render(request, 'index.html', context)

def records(request, id):
    records = Records.objects.filter(user_id_id=id).order_by('-game', 'round_num')
    sos = Records.stats.sos(id)
    esos = Records.stats.esos(id)
    user = User.objects.get(pk=id)
    decks = Decks.objects.filter(user_id_id=id).order_by('-game')
    context = {
            'records': records,
            'user': user,
            'sos': sos,
            'esos': esos,
            'deck': decks,
            }
    return render(request, 'standings.html', context)

point_vals = {
            'WI': 3,
            'TW': 2,
            'TI': 1,
            'TL': 0,
            'LO': 0
            }

def faction_records(records, decks):    
    vals = {}
    for record in records:
        game_deck = decks.filter(user_id=record.user_id_id, game=record.game_id).first()
        if game_deck is not None:
            if game_deck.corp_faction not in vals.keys():
                vals[game_deck.corp_faction] = point_vals[record.corp_status]
            else:
                vals[game_deck.corp_faction] += point_vals[record.corp_status]
            if game_deck.runner_faction not in vals.keys():
                vals[game_deck.runner_faction] = point_vals[record.runner_status]
            else:
                vals[game_deck.runner_faction] += point_vals[record.runner_status]
    return vals

def id_records(records, decks):
    vals = {}
    for record in records:
        game_deck = decks.filter(user_id=record.user_id_id, game=record.game_id).first()
        if game_deck is not None:
            if game_deck.corp_id not in vals.keys():
                vals[game_deck.corp_id] = point_vals[record.corp_status]
            else:
                vals[game_deck.corp_id] += point_vals[record.corp_status]
            if game_deck.runner_id not in vals.keys():
                vals[game_deck.runner_id] = point_vals[record.runner_status]
            else:
                vals[game_deck.runner_id] += point_vals[record.runner_status]
    return vals

def all_records(request, game_night=None):
    records = Records.objects.all().filter(display=True)
    all_players = set(list(Records.objects.values_list('user_id_id', flat=True)))
    all_players = [player for player in all_players if player!=1]
    stats = {}
    for player in all_players:
        decks = Decks.objects.filter(user_id=player)
        corp_factions = decks.distinct('corp_faction').values('corp_faction')
        runner_factions = decks.distinct('runner_faction').values('runner_faction')
        points = Records.stats.total_points(player)
        total_possible = Records.stats.total_games(player) * 6 # because there's a max value of 6 points in each round
        point_percentage = (points / total_possible ) * 100
        stats[player] = {
                'name': User.objects.filter(user_id=player).values('name')[0]['name'],
                'total_games': Records.stats.total_games(player),
                'points': points,
                'point_percentage': point_percentage,
                'runner_factions': ', '.join([faction['runner_faction'].title() for faction in runner_factions]),
                'corp_factions': ', '.join([faction['corp_faction'].title() for faction in corp_factions]),
                'sos': Records.stats.sos(player),
                'esos': Records.stats.esos(player),
                }
    context = {
            'records': records,
            'stats': stats,
            }
    return render(request, 'records.html', context)

def statistics(request):
    non_filtered_records = Records.objects.exclude(user_id_id=1)
    all_decks = Decks.objects.all()
    faction_recs = faction_records(non_filtered_records, all_decks)
    id_recs = id_records(non_filtered_records, all_decks)
    runner_records = non_filtered_records.values('runner_status').annotate(runner_count=Count('runner_status')).order_by('-runner_status')
    corp_records = non_filtered_records.values('corp_status').annotate(corp_count=Count('corp_status')).order_by('-corp_status')
    runner = [record for record in runner_records]
    corp = [record for record in corp_records]
    win_rates = {}
    for x in range(len(runner)):
        newkey = runner[x]['runner_status']
        win_rates[newkey] = {
                'runner': runner[x].get('runner_count', 0),
                'corp': corp[x].get('corp_count', 0),
                }
    for key in ['WI', 'LO', 'TW', 'TL', 'TI']:
        if not win_rates.get(key, None):
            win_rates[key] = {
                    'runner': 0,
                    'corp': 0
                    }
    context = {
            'win_rates': win_rates,
            'faction_records': faction_recs,
            'id_records': id_recs,
            }
    return render(request, 'statistics.html', context)
