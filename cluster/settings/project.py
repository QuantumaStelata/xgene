from cluster.settings.environment import env

FRONT_DOMAIN = env.str('FRONT_DOMAIN', '')
BACK_DOMAIN = env.str('BACK_DOMAIN', '')
