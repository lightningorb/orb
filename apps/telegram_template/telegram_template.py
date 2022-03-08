# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:23:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-08 19:04:32


from orb.misc.plugin import Plugin

import os
import traceback
from glob import glob
import inspect
from textwrap import dedent
from functools import partial
from threading import Thread
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from orb.core.stoppable_thread import StoppableThread


class UpdateLogic:

    _updater = None
    _start = False
    _chat_id = None
    send_message = None

    def init(self, updater):
        self._chat_id = None
        self._updater = updater
        if os.path.exists("connect.txt"):
            with open("connect.txt") as f:
                self._chat_id = int(f.read().strip())
                self.init_funcs()
                self.greet()

    def init_funcs(self):
        self.send_message = partial(
            self._updater.bot.send_message, chat_id=self._chat_id
        )

    def connect(self, chat_id):
        with open("connect.txt", "w") as f:
            f.write(str(chat_id))
            self._chat_id = chat_id
        self.init_funcs()

    def greet(self):
        if self.send_message:
            self.send_message(text="Connected")


update_logic = UpdateLogic()


def help_func(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        dedent(
            """
            /connect run this so the bot can initiate chats with you
            /start start receiving events
            /stop to stop receiving events
            """
        )
    )


def filter_func(update: Update, context: CallbackContext) -> None:
    print(context.args)
    update_logic._filter = " ".join(context.args)
    update.message.reply_text("Filter set.")


def start(update: Update, context: CallbackContext) -> None:
    update_logic._start = True
    update.message.reply_text("Starting. You'll recieve events here as they occur.")


def stop(update: Update, context: CallbackContext) -> None:
    update_logic._start = False
    update.message.reply_text("Stopping.")


def connect(update: Update, context: CallbackContext) -> None:
    update_logic.connect(update.message.chat_id)
    update.message.reply_text(f"Connected.")


class BotThread(StoppableThread):
    def run(self):
        self.events = {}
        print("Starting bot")
        updater = Updater("5117883519:AAFWoLQCMgJIMdQmDNK9GWgGG0VgnmGG5-k")
        update_logic.init(updater)

        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("stop", stop))
        dispatcher.add_handler(CommandHandler("filter", filter_func))
        dispatcher.add_handler(CommandHandler("help", help_func))
        dispatcher.add_handler(CommandHandler("connect", connect))

        updater.start_polling()
        print("Bot started")
        while not self.stopped():
            time.sleep(0.1)
        print("Bot stopped")
        update_logic.send_message(text="Adios")
        time.sleep(1)
        updater.stop()

    def htlc_event(self, htlc):
        update_logic.send_message(text=htlc.event_type)
        if htlc.event_type == "SEND" and htlc.event_outcome == "settle_event":
            prev = self.events[htlc.outgoing_htlc_id]
            amount = int(prev.event_outcome_info["outgoing_amt_msat"] / 1_000)
            update_logic.send_message(text=f"⚡️ Sent {amount:_}")
        self.events[htlc.outgoing_htlc_id] = htlc


class TelegramBotExample(Plugin):
    def main(self) -> None:
        self.thread = BotThread()
        self.thread.start()

    def htlc_event(self, event):
        self.thread.htlc_event(event)

    def cleanup(self):
        print("Clean up bot")
        self.thread.stop()
