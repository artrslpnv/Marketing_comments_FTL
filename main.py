from dialog_bot_sdk.bot import DialogBot
import dialog_api
import grpc
from globals import app
import sys
from log import logger
from threading import Thread
from dialog_bot_sdk import interactive_media
from dialog_bot_sdk.entity_manager import DEFAULT_OPTIMIZATIONS
from dialog_bot_sdk.internal.peers import group_peer, private_peer
admins = []
was_value_clicked_by = {}

def on_msg(*params):
    print('on msg', params)
    if params[0].message.textMessage.text == 'привет' or params[0].message.textMessage.text == '/start':
        bot.messaging.send_message(params[0].peer,
                                   "Добрый день , я бот , собирающий данные по опросам ,чтобы создать опрос напишите название опроса и варианты ответа в формате: \n"
                                   + "'/create;Название опроса;Первый Вариант;Второй Вариант;и далее варианты через ; после последнего не ставить!'" + "\n" +
                                   "для получения  отчета напишите: '/stats' (Внимание человек ,отправивший запрос на отправку опроса и только он может получить данные по запросу" + "\n"
                                   + "(!!из соображений логики, cчитается, что голос одного человека учитывается не более 1 раза за каждый из вариантов!!)" + "\n" +
                                   "('/stats' возвращает общую статистику по всем опросам(в силу невозможности их дробить из-за недостатков апи) а именно , cколько людей проголосовали за какой вариант, после этого удаляя все данные.")
    elif params[0].message.textMessage.text.find('/create') != -1:
        global admin
        admin = params[0].peer
        list = params[0].message.textMessage.text.split(';')
        name = list[1];
        variants = list

        massive_of_buttons = []
        for i in range(2, len(variants)):
            massive_of_buttons.append(interactive_media.InteractiveMedia(i
                                                                         , interactive_media.InteractiveMediaButton(
                    variants[i], variants[i])
                                                                         ))
        req = dialog_api.messaging_pb2.RequestLoadDialogs(
            min_date=0,
            limit=20,
            optimizations=DEFAULT_OPTIMIZATIONS
        )
        result = bot.internal.messaging.LoadDialogs(req)
        for peer in result.group_peers:
            peer1 = group_peer(peer.group_id)
            bot.messaging.send_message(
                peer1,
                name,
                [interactive_media.InteractiveMediaGroup(
                    massive_of_buttons
                )]
            )
        for peer in result.user_peers:
            peer1 = private_peer(user_id=peer.uid)
            bot.messaging.send_message(
                peer1,
                name,
                [interactive_media.InteractiveMediaGroup(
                    massive_of_buttons
                )]
            )
    elif params[0].message.textMessage.text == '/stats':
        if params[0].peer == admin:
            printing = ""
            global was_value_clicked_by
            print(was_value_clicked_by)
            if len(was_value_clicked_by.keys()) == 0:
                bot.messaging.send_message(admin,
                                           "нет активных опросов")
            else:
                for item in was_value_clicked_by.keys():
                    printing = printing + str(len(was_value_clicked_by[
                                                      item])) + " " + "такое количество людей  проголосовало за этот вариант {}".format(
                        item) + '\n'
                bot.messaging.send_message(admin,
                                           printing + "Запомните эту статистику теперь она ,к сожалению ,удалена")
                was_value_clicked_by = {}
        else :
            bot.messaging.send_message(params[0].peer,"Вам нельзя просматривать статистику , так как вы не админ")
    else:
        bot.messaging.send_message(params[0].peer, "я не поддерживаю эту команду")


def on_click(*params):
    a = set();  # считаем голос одного юзера только 1 раз
    global was_value_clicked_by
    print(params[0].uid)
    if not params[0].value in was_value_clicked_by:
        was_value_clicked_by[params[0].value] = [params[0].uid]
    else:
        if not params[0].uid in was_value_clicked_by[params[0].value]:
            was_value_clicked_by[params[0].value].append(params[0].uid)

if __name__ == '__main__':
    #app.run(threaded=True)
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im',
        # bot endpoint (specify different endpoint if you want to connect to your on-premise environment)
        grpc.ssl_channel_credentials(),  # SSL credentials (empty by default!)
        '592e37a534ced85ee9f06561dce1b3e1985f94f2',  # bot token
        verbose=False  # optional parameter, when it's True bot prints info about the called methods, False by default
    )
    t = Thread(bot.messaging.on_message(on_msg, on_click))
    t.start()