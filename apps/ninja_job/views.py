from django.shortcuts import render, redirect
import datetime
import random

def random_gold(min, max):
    gold_add = random.randint(min, max)
    return gold_add

def game_over_query(request):
    game_over = False
    print('entered game over query')
    if int(request.session['gold']) >= int(request.session['gold_goal']):
        request.session['end_game_text'] = "You succeed in raising the funds necissary to pay off your mortgage to the wall-street fat-cats who wanted to steal your ancestral home. Now what?"
        game_over = True
    if int(request.session['turnsremaining']) < 0:
        request.session['end_game_text'] = "You ran out of time to earn "+ request.session['gold_goal'] + " gold. Your family's farm is reposessed by the bank and you spend the rest of your days in a debitor's prison."
        game_over = True
    if int(request.session['gold']) < 0:
        request.session['end_game_text'] = "Your gambled away all your earnings at the casino but could not quit the tables and went into debt with the mob. You check yourself into rehab for your gambling addiction while your family's farm is taken by the bank."
        game_over = True
    return game_over

def end_screen(request):
    return render(request, "ninja_job/game_over.html")

def init_session(request):
    request.session['gold_goal'] = 300
    request.session['gold'] = 0
    request.session['activities'] = []
    request.session['turns'] = 0
    request.session['maxturns'] = 45
    request.session['end_game_text'] = ''
    return render(request, "ninja_job/new_game.html")



def new_session(request):
    print(request.POST)
    request.session['gold_goal'] = request.POST['gold_owed']
    request.session['maxturns'] = request.POST['time_left']

    request.session['turnsremaining'] = int(request.session['maxturns']) - int(request.session['turns'])

    return redirect("/ninja")


def index(request):
    return render(request, "ninja_job/index.html")

def process(request, loc):

    time_of = datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")

    if loc == 'farm':
        gold_earned = random_gold(10,20)
        request.session['gold'] += int(gold_earned)
        action = ['pos', 'Earned '+ str(gold_earned) +' gold from the '+ loc +'! ('+ time_of +')']

    elif loc == 'cave':
        gold_earned = random_gold(5,10)
        request.session['gold'] += int(gold_earned)
        action = ['pos', 'Earned '+ str(gold_earned) +' gold from the '+ loc +'! ('+ time_of +')']

    elif loc == 'house':
        gold_earned = random_gold(2,5)
        request.session['gold'] += int(gold_earned)
        action = ['pos', 'Earned '+ str(gold_earned) +' gold from the '+ loc +'! ('+ time_of +')']
        
    elif loc == 'casino':
        gold_earned = random_gold(-50,50)
        request.session['gold'] += int(gold_earned)
        if int(gold_earned) < 0:
            action = ['neg', 'Lost '+ str(gold_earned * -1) +' gold at the '+ loc +'! ('+ time_of +')']
        else:
            action = ['pos', 'Won '+ str(gold_earned) +' gold at the '+ loc +'! ('+ time_of +')']
    
    print(request.session['activities'])
    request.session['turns'] += 1
    request.session['activities'].insert(0, action)
    request.session['turnsremaining'] = int(request.session['maxturns']) - int(request.session['turns'])
    if game_over_query(request):
        return redirect("/game_over")
    else:
        return redirect("/ninja")

# Create your views here.
