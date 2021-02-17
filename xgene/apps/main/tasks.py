from django.db.models import signals
from django.dispatch import receiver
from .models import *
from threading import Thread
import time
import requests
import json

@receiver(signals.post_save, sender=ClanId)
def update_clan_info(*args, **kwargs):
    '''
    Обновляет инфорамацию о клане каждый раз, когда изменился ClanId
    '''
    clan_id = ClanId.objects.get()

    url = 'https://ru.wargaming.net/clans/wot/{}/api/claninfo/'.format(clan_id)
    clan_info = json.loads(requests.get(url).text)

    try:
        clan_name = ClanInfo.objects.get()
        clan_name.delete()
    except:
        pass
    
    clan_name = ClanInfo()
    clan_name.clan_tag = clan_info['clanview']['clan']['tag']
    clan_name.clan_name = clan_info['clanview']['clan']['name']
    clan_name.clan_motto = clan_info['clanview']['clan']['motto']
    clan_name.clan_color = clan_info['clanview']['clan']['color']
    clan_name.clan_emblem = 'https://ru.wargaming.net' + clan_info['clanview']['clan']['huge_emblem_url']
    clan_name.save()
    
    Thread(target=update_clan_static(), args=()).start()


def update_clan_static():
    '''
    Обновляет статистику клана после обновления информации о клане,
    либо каждый N минут в другом потоке функции update
    '''
    clan_id = ClanId.objects.get()

    url = 'https://ru.wargaming.net/clans/wot/{}/api/claninfo/'.format(clan_id)
    clan_rating = json.loads(requests.get(url).text)['clanview']['rating']

    url = 'https://ru.wargaming.net/clans/wot/{}/api/stronghold'.format(clan_id)
    stronghold = json.loads(requests.get(url).text)['stronghold']

    url = 'https://ru.wargaming.net/clans/wot/{}/api/globalmap/'.format(clan_id)
    globalmap = json.loads(requests.get(url).text)['globalmap'] 

    clan_static = ClanStatic()
    clan_info = ClanInfo.objects.get()

    clan_static.clan_tag = clan_info        
    clan_static.clan_sh10 = stronghold['esh_10']
    clan_static.clan_sh8 = stronghold['esh_8']
    clan_static.clan_sh6 = stronghold['esh_6']
    clan_static.clan_gm10 = globalmap['gm_elo_rating_10']
    clan_static.clan_gm8 = globalmap['gm_elo_rating_8']
    clan_static.clan_gm6 = globalmap['gm_elo_rating_6']
    clan_static.clan_battles_count = clan_rating['average_battles_count']
    clan_static.clan_win_rate = clan_rating['average_win_rate']
    clan_static.clan_rate = clan_rating['rating']
    clan_static.clan_position = clan_rating['rating_position']
    clan_static.clan_xp_per_battle = clan_rating['average_xp_per_battle']
    clan_static.clan_damage_per_battle = clan_rating['average_damage_per_battle']
    clan_static.save()


def update_clan_players():
    '''
    Обновляет список игроков клана после обновления информации о клане,
    либо каждый N минут в другом потоке функции update

    Сначала удаляет из БД лишних игроков клана.
    После обновляет игроков с API, либо добавляет их, если такого игрока не существует.
    '''
    clan_id = ClanId.objects.get()

    url = 'https://api.worldoftanks.ru/wot/clans/info/?application_id=f43f7018199159cf600980288310be15&clan_id={}'.format(clan_id)
    players_api = json.loads(requests.get(url).text)['data']['{}'.format(clan_id)]['members']
    

    players_api_list = [i['account_name'] for i in players_api]
    players_db_list = [i.player_name for i in Players.objects.all()]

    if sorted(players_api_list) != sorted(players_db_list):
        for player in players_db_list:
            if player not in players_api_list:
                Players.objects.get(player_name=player).delete()


    for pl in players_api:
        player, player_is_created = Players.objects.get_or_create(player_id=pl['account_id'], player_name = pl['account_name'],
                                                    player_clan = ClanId.objects.get(), player_role = ClanRole.objects.get(clan_role_ru=str(pl['role_i18n'])))

        url = 'https://api.worldoftanks.ru/wot/account/info/?application_id=f43f7018199159cf600980288310be15&account_id={}'.format(pl['account_id'])
        player_stats = json.loads(requests.get(url).text)['data']['{}'.format(pl['account_id'])]

        if str(player.player_battles) != str(player_stats['statistics']['all']['battles']):
            player.player_battles = player_stats['statistics']['all']['battles']
            player.player_wgr = player_stats['global_rating']
            player.player_win = round(int(player_stats['statistics']['all']['wins'])*100/int(player.player_battles if player.player_battles != 0 else 1), 2)
            player.player_damage = round(int(player_stats['statistics']['all']['damage_dealt'])/int(player.player_battles if player.player_battles != 0 else 1))
            player.player_frags = round(int(player_stats['statistics']['all']['frags'])/int(player.player_battles if player.player_battles != 0 else 1),2)

            player.save()



def update():
    while True:
        print ('Start Update')
        now = time.time()

        update_clan_static()
        update_clan_players()

        print ('Update DB - {}s.'.format(time.time()-now))
        time.sleep(60)


Thread(target=update, daemon=True, args=()).start()     
