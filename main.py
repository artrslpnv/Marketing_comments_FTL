from dialog_bot_sdk.bot import DialogBot
from globals import app as application
import sys
from log import logger
from threading import Thread
def on_msg(*params):
    print('on msg', params)
    bot.messaging.send_message(
        params[0].peer, 'Reply to : ' + str(params[0].message.textMessage.text)
    )


if __name__ == '__main__':
    application.run(port=5000 if len(sys.argv) == 1 else int(sys.argv[1]), threaded=True)
    bot = DialogBot.get_insecure_bot(
        'hackathon-mob.transmit.im',  # bot endpoint (specify different endpoint if you want to connect to your on-premise environment) # SSL credentials (empty by default!)
        '592e37a534ced85ee9f06561dce1b3e1985f94f2',  # bot token
        verbose=False # optional parameter, when it's True bot prints info about the called methods, False by default
    )
    t=Thread(bot.messaging.on_message(on_msg))
    t.start()
