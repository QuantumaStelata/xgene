# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from .tasks import *

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
    clan = ClanInfo.objects.get()
    static = ClanStatic.objects.latest('clan_static_update')

    url = 'https://ru.wargaming.net/clans/wot/{}/api/personnel/'.format(ClanId.objects.get())
    response = json.loads(requests.get(url).text)
    top_damage = response['personnel']['top_damage_avg']
    top_wins = response['personnel']['top_wins_ratio']
    top_battles = response['personnel']['top_battles_count_daily']
    return render(request, "main.html", {'online': online(), 'clan': clan, 'static': static,
                                         'top_damage': top_damage, 'top_wins': top_wins, 'top_battles': top_battles})
    

def players(request):
    clan = ClanInfo.objects.get()
    players_list = Players.objects.all()
    return render(request, "players.html", {'online': online(), 'clan': clan, 'list': players_list, 'len': len(players_list)})

def news(request):
    clan = ClanInfo.objects.get()
    articles = Article.objects.filter(article_publicate=True).order_by('-article_date')
    return render(request, "news.html", {'online': online(), 'clan': clan, 'articles': articles})

def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)  
    except:
        raise Http404("Статья не найдена") 

    clan = ClanInfo.objects.get()
    return render(request, 'article.html', {'online': online(), 'clan': clan, 'article': article})