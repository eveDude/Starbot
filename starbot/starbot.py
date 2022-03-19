#!/usr/bin/env python3
''' Starbot - posting Zkillboard Kills matching foo to Discord '''
import json
import configparser
import asyncio
import logging
import websocket
import discord_notify as dn


## Settings
CONFIG_FILE = "/home/starbot/starbot.ini"


## No touchy


#websocket.enableTrace(True)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def config_mapper(section):
    ''' parse config '''
    dict1 = {}
    options = CONFIG.options(section)
    for option in options:
        try:
            dict1[option] = CONFIG.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
                logging.warning("Error importing config!")
        except:
            logging.error("Config: exception on: %s", option)
            dict1[option] = None
    return dict1


def sendto_discord(message):
    ''' send messages to discord using webhook '''
    notifier = dn.Notifier(WEBHOOK)
    notifier.send(message, print_message=False)


def on_message(wsapp, message):
    '''
    Load message into json, call parser
    '''
    data = json.loads(message)
    asyncio.run(parse_message(data))
    return True


async def parse_message(data):
    '''
    Parsing the Zkillboard JSON
    '''
    ### GET ZKB URI
    try:
        zkill_uri = data['zkb']['url']
    except:
        logging.error("error getting zkill_uri: %s", data)

    ### GET ATTACKERS
    try:
        attackers = data['attackers']

    except:
        logging.error("error evaluating attackers: %s", data)

    for attacker in attackers:
        if "corporation_id" in attacker:
        ## if not: Its an NPC
            if "character_id" in attacker:
            ## if not: Its a Structure?
                killer_char = attacker['character_id']
                if is_char(killer_char):
                    logging.info("killer is in char list: %s", killer_char)
                    logging.info("zkill uri is: %s", zkill_uri)
                    sendto_discord(zkill_uri)
                    return True

            killer_corp = attacker['corporation_id']
            if is_corp(killer_corp):
                logging.info("killer is in corp: %s", killer_corp)
                logging.info("zkill uri is: %s", zkill_uri)
                sendto_discord(zkill_uri)
                return True

        if "alliance_id" in attacker:
            killer_ally = attacker['alliance_id']
            if is_ally(killer_ally):
                logging.info("killer is in corp: %s", killer_ally)
                logging.info("zkill uri is: %s", zkill_uri)
                sendto_discord(zkill_uri)
                return True

    ### GET VICTIM
    try:
        victim = data['victim']

        if "character_id" in victim:
        ## if not: Its a Structure?
            killed_char = victim['character_id']
            if is_char(killed_char):
                logging.info("killed is in corp: %s", killed_char)
                logging.info("zkill uri is: %s", zkill_uri)
                sendto_discord(zkill_uri)
                return True


        killed_corp = victim['corporation_id']
        if is_corp(killed_corp):
            logging.info("killed is in corp: %s", killed_corp)
            logging.info("zkill uri is: %s", zkill_uri)
            sendto_discord(zkill_uri)
            return True

        if "alliance_id" in victim:
            killed_ally = victim['alliance_id']
            if is_ally(killed_ally):
                logging.info("killed is in ally: %s", killed_ally)
                logging.info("zkill uri is: %s", zkill_uri)
                sendto_discord(zkill_uri)
                return True

    except:
        logging.error("error evaluating victim: %s", victim)
        logging.error("zkill uri is: %s", zkill_uri)

    return True


def on_open(wsapp):
    '''
    websocket subscription to channel
    '''
    logging.info("starting Starbot 0.x")
    logging.info("monitoring the following chars")
    logging.info(CHARS)
    logging.info("monitoring the following corporations")
    logging.info(CORPS)
    logging.info("monitoring the following alliances")
    logging.info(ALLYS)
    subs = '''{"action":"sub","channel":"killstream"}'''
    wsapp.send(subs)


def on_error(wsapp, error):
    '''
    websocket error handling
    '''
    logging.error("got an error: %s", error)


def on_close(wsapp):
    '''
    websocket closing
    '''
    logging.info("stopping Starbot 0.x")


def is_char(char_id):
    '''
    check if CHAR_ID matches our target
    '''
    return bool(char_id in CHARS)


def is_corp(corp_id):
    '''
    check if CORP_ID matches our target
    '''
    return bool(corp_id in CORPS)


def is_ally(ally_id):
    '''
    check if ALLY_ID matches our target
    '''
    return bool(ally_id in ALLYS)


## Config handling
CONFIG = configparser.ConfigParser()
CONFIG.sections()
CONFIG.read(CONFIG_FILE)

CHARS = []
CORPS = []
ALLYS = []
ZKILL = config_mapper('ZKILLBOARD')['zkill_endpoint']
WEBHOOK = config_mapper('DISCORD')['webhook']
CHARSTRING = config_mapper('ZKILLBOARD')['chars']
CORPSTRING = config_mapper('ZKILLBOARD')['corps']
ALLYSTRING = config_mapper('ZKILLBOARD')['allys']

## Build char, corp and ally lists
for char in CHARSTRING.split(","):
    CHARS.append(int(char))

for corp in CORPSTRING.split(","):
    CORPS.append(int(corp))

for ally in ALLYSTRING.split(","):
    ALLYS.append(int(ally))

## start listening on websocket
wsapp = websocket.WebSocketApp(ZKILL,
                               on_message=on_message,
                               on_open=on_open,
                               on_error=on_error,
                               on_close=on_close)
wsapp.run_forever()
