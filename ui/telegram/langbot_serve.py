#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import requests as rq
from bs4 import BeautifulSoup
import json
import random

G_STATES = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
#def start(bot, update):
#    bot.sendMessage(update.message.chat_id, text='Hi!')

def init_state(chat_id) :
    G_STATES[chat_id] = ''
    
def check_state(chat_id) :
    if not chat_id in G_STATES:
        init_state(chat_id)

def get_state(chat_id) :
    return G_STATES[chat_id]

def set_state(chat_id, val) :
    G_STATES[chat_id] = val
        
def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def iam(bot, update):
    chat_id = update.message.chat_id
    check_state(chat_id)
    st = get_state(chat_id)
    msg = "my chat_id is %d" %(chat_id)
    msg = msg + "\n" + "my state is %s" %(st)
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)    
    
def start(bot, update):
    chat_id = update.message.chat_id
    init_state(chat_id)
    user = update.message.from_user
    msg = "안녕, %s %s! 난 언어학습을 도와주는 랭봇이야!" %(user.first_name, user.last_name)
    bot.sendMessage(update.message.chat_id, text=msg)



def search(chat_id, user_name, msg) :
    try : 
        st = get_state(chat_id)
        mem = st
        url = "" %(D_API_URL, mem, user_name, msg)

        #r = rq.get(url)
        #r.encoding = 'utf-8'
        #d = json.loads(r.text, strict=False)
    
        resp = msg #d['text']
        new_st = '1' #d['session']
    
        ans = resp 

        set_state(chat_id, new_st)
    except:
        ans = msg #r.text
    
    return ans

def query(chat_id, user_name, msg) :
    ans = search(chat_id, user_name, msg)
    
    return ans


def response(bot, update):
    chat_id = update.message.chat_id
    check_state(chat_id)
    user = update.message.from_user
    user_name = "%s%s" %(user.last_name, user.first_name)
  
    r_msg = query(chat_id, user_name, update.message.text)
    bot.sendMessage(chat_id, 
                    text=r_msg)



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    with open(os.path.join('/notebooks/work/langbot/ui/telegram/','langbot.keyfile'), 'r') as f :
        token = f.readline().strip()
        
    updater = Updater(token)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("iam", iam))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], response))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
