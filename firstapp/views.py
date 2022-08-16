from distutils.util import convert_path
from django.shortcuts import render
from django.http import HttpResponse
from . import forms
# Create your views here.

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def index(request):
    return render(request, 'firstapp/index.html')

def resources(request):
    return render(request, 'firstapp/resources.html')

def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("SUCCESS")
            date= form.cleaned_data['date_stat'] 
            #algorithm = form.cleaned_data['algorithm_field']
            #prop = form.cleaned_data['prop_stat']
            #list_of_players = nba_bet_grabber(date, prop)
            list_poop = []
            list_poop.append(["Lebron James", "Lakers-SF", "30", "Lebron", "James"])
            toCheck = scrape_player_data(list_poop, date)
            for p in toCheck:
                print(p[1])
                print(p[2])
                print(p[3])
                print(p[4])
                print(p[5])
                print(p[6])
                print(p[7])
                print(p[8])


    return render(request, 'firstapp/formpage.html', {'form':form})

def nba_bet_grabber(date_to_use, prop) :
    players = []
    numPlayers = 0
    url = "https://www.bettingpros.com/nba/picks/prop-bets/bet/"+prop+"/?date="
    if prop == 'three-points%20made' :
        stat = "three point shots made"
    else:
        stat = prop

    url += date_to_use
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table = soup.find('table')
    table2 = table.find('tbody')
    table3 = table2.find_all('tr')

    for player in table3:
        # Name
        first_name_tag = player.find('span', {'class':'yearbook-block__title--block player-name player-name--desktop'})
        first_name = first_name_tag.text if first_name_tag else ''

        last_name_tag = player.find('span', {'class':'yearbook-block__title--block player-name'})
        last_name = last_name_tag.text if last_name_tag else ''

        name = first_name + last_name

        # Team - Position
        description_tag = player.find('div', {'class':'yearbook-block__description'})
        description = description_tag.text if description_tag else ''

        # Over/Under Line
        ou_tag = player.find('span', {'class':'ou-line__line'})
        ou_line = ou_tag.text if ou_tag else ''

        players.append([name, description, ou_line, first_name, last_name])
        holder = players[numPlayers]
        print(holder[0], holder[1],":", holder[2], stat)
        numPlayers+=1
    
    return players

def name_converter(f_name, l_name) :
    if len(l_name) >= 6 :
        username = l_name[0:6] + f_name[0:2] + "01"
    else :
        username = l_name[0:len(l_name)] + f_name[0:2] + "01"

    username = l_name[0] + "/" + username + "/gamelog/"
    return username

def year(date):
    if(date.month < 7) :
        return str(date.year)
    else :
        return str(date.year + 1)

def scrape_player_data(player_list, date2Use):
    toReturn=[]
    for player in player_list:

        bball_ref_url = "https://www.basketball-reference.com/players/" + name_converter(player[3], player[4]) + year(date2Use)
        response = requests.get(bball_ref_url)
        data = response.text
        soup1 = BeautifulSoup(data, 'html.parser')
        first = soup1.find('div', {'id':'content'})
        second = first.find('div', {'id':'all_pgl_basic'})
        stats1 = second.find('table', {'id':'pgl_basic'})
        stats2 = stats1.find('tbody')
        stats = stats2.find_all('tr')

        ppg = 0
        rpg = 0
        apg = 0
        spg = 0
        bpg = 0
        tpg = 0
        mpg = 0
        fg_percentage = 0
        three_point_percentage = 0

        games = 0

        for game in stats:
            date_tag = game.find('td', {'class':'left'})
            if (date_tag) :
                date1 = date_tag.text
                date = datetime.strptime(date1, '%Y-%m-%d')
                dt = datetime.combine(date2Use, datetime.min.time())
                if (date <= dt): 
                    pts_tag = game.find('td', {'data-stat':'pts'})
                    if (pts_tag) :
                        pts = pts_tag.text
                        rebs = game.find('td', {'data-stat':'trb'}).text
                        asts = game.find('td', {'data-stat':'ast'}).text
                        stls = game.find('td', {'data-stat':'stl'}).text
                        blks = game.find('td', {'data-stat':'blk'}).text
                        tov = game.find('td', {'data-stat':'tov'}).text
                        min = game.find('td', {'data-stat':'mp'}).text
                        fg = game.find('td', {'data-stat':'fg_pct'}).text
                        threeP = game.find('td', {'data-stat':'fg3_pct'}).text

                        games += 1
                        ppg += int(pts)
                        rpg += int(rebs)
                        apg += int(asts)
                        spg += int(stls)
                        bpg += int(blks)
                        tpg += int(tov)
                        mpg += timeToMin(min)
                        #fg_percentage += int(fg)
                        #three_point_percentage += int(threeP)
                    else :
                        pts = 0
                        rebs = 0
                        asts = 0
                        stls = 0
                        blks = 0
                        tov = 0
                        min = 0
                        fg = 0
                        threeP = 0
                    
                else :
                    break
        if (games != 0):
            ppg /= games
            rpg /= games
            apg /= games
            spg /= games
            bpg /= games
            tpg /= games
            mpg /= games
            fg_percentage /= games
            three_point_percentage /= games

        toReturn.append([player_list[0], ppg, rpg, apg, spg, bpg, tpg, mpg, fg_percentage, three_point_percentage])
    return toReturn

def timeToMin(time) :
    time = str(time)
    print(time)

    min = time[0:(len(time)-3 )]
    min = int(min)
    sec = time[(len(time))-2:len(time)]
    sec = int(sec)
    toReturn = min + (sec / 60)
    return toReturn


