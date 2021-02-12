# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import *

from threading import Thread
from time import sleep, time
import requests
import json

def update_db():
    while True:
        print ("Start update DB")
        tm = time()
        
        clan_id = ClanId.objects.get()

        url = 'https://ru.wargaming.net/clans/wot/{}/api/claninfo/'.format(clan_id)
        clan_info = json.loads(requests.get(url).text)

        url = 'https://ru.wargaming.net/clans/wot/{}/api/stronghold'.format(clan_id)
        stronghold = json.loads(requests.get(url).text)['stronghold']

        url = 'https://ru.wargaming.net/clans/wot/{}/api/globalmap/'.format(clan_id)
        globalmap = json.loads(requests.get(url).text)['globalmap']
 
        url = 'https://ru.wargaming.net/clans/wot/{}/api/claninfo/'.format(clan_id)
        clan_rating = json.loads(requests.get(url).text)['clanview']['rating']

        clan_name = ClanName.objects.get()
        if str(clan_name.clan_name) != clan_info['clanview']['clan']['name'] or str(clan_name.clan_position) != clan_rating['rating_position']:
            clan_name.clan_name = clan_info['clanview']['clan']['name']
            clan_name.clan_motto = clan_info['clanview']['clan']['motto']
            clan_name.clan_sh10 = stronghold['esh_10']
            clan_name.clan_sh8 = stronghold['esh_8']
            clan_name.clan_sh6 = stronghold['esh_6']
            clan_name.clan_gm10 = globalmap['gm_elo_rating_10']
            clan_name.clan_gm8 = globalmap['gm_elo_rating_8']
            clan_name.clan_gm6 = globalmap['gm_elo_rating_6']
            clan_name.clan_battles_count = clan_rating['average_battles_count']
            clan_name.clan_win_rate = clan_rating['average_win_rate']
            clan_name.clan_rate = clan_rating['rating']
            clan_name.clan_position = clan_rating['rating_position']
            clan_name.clan_xp_per_battle = clan_rating['average_xp_per_battle']
            clan_name.clan_damage_per_battle = clan_rating['average_damage_per_battle']

            clan_name.save()

        url = 'https://api.worldoftanks.ru/wot/clans/info/?application_id=f43f7018199159cf600980288310be15&clan_id={}'.format(clan_id)
        response = json.loads(requests.get(url).text)
    
        Players.objects.all().delete()
        for pl in response['data']['{}'.format(clan_id)]['members']:
            url = 'https://api.worldoftanks.ru/wot/account/info/?application_id=f43f7018199159cf600980288310be15&account_id={}'.format(pl['account_id'])
            player_stats = json.loads(requests.get(url).text)
            player_battles = player_stats['data']['{}'.format(pl['account_id'])]['statistics']['all']['battles']
            player_wgr = player_stats['data']['{}'.format(pl['account_id'])]['global_rating']
            player_win = round(int(player_stats['data']['{}'.format(pl['account_id'])]['statistics']['all']['wins'])*100/int(player_battles), 2)
            player_damage = round(int(player_stats['data']['{}'.format(pl['account_id'])]['statistics']['all']['damage_dealt'])/int(player_battles))
            player_frags = round(int(player_stats['data']['{}'.format(pl['account_id'])]['statistics']['all']['frags'])/int(player_battles),2)

            role = ClanRole.objects.get(clan_role_ru=str(pl['role_i18n']))
            player = Players.objects.create(player_clan=clan_id,  player_role=role, 
                                            player_id=pl['account_id'], player_name=pl['account_name'], 
                                            player_battles= player_battles, player_wgr= player_wgr,
                                            player_win= player_win, player_damage= player_damage, player_frags=player_frags)
        player.save()

        print ("Finish update DB - {}".format(time() - tm))
        sleep(900)

Thread(target=update_db, daemon=True, args=()).start()     


def online():
    url = 'https://wgstatus.com/api/data'
    response = json.loads(requests.get(url).text)
    online = {}
    for i in response['results']:
        try:
            for j in i['data']['servers']:
                if 'RU' in j['name']:
                    online[j['name']]=j['online']
        except:
            continue
    return online


def main(request):
    time1 = time()

    clan = ClanName.objects.get()

    url = 'https://ru.wargaming.net/clans/wot/{}/api/personnel/'.format(ClanId.objects.get())
    response = json.loads(requests.get(url).text)
    top_damage = response['personnel']['top_damage_avg']
    top_wins = response['personnel']['top_wins_ratio']
    top_battles = response['personnel']['top_battles_count_daily']
    print ('%s' % (time()-time1))
    return render(request, "main.html", {'online': online(), 'clan': clan, 
                                         'top_damage': top_damage, 'top_wins': top_wins, 'top_battles': top_battles})
    

def players(request):
    players_list = Players.objects.all()
    return render(request, "players.html", {'online': online(), 'list': players_list})

def news(request):
    articles = Article.objects.filter(article_publicate=True).order_by('-article_date')
    return render(request, "news.html", {'online': online(), 'articles': articles})

def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)  
    except:
        raise Http404("Статья не найдена") 

    return render(request, 'article.html', {'online': online(), 'article': article})