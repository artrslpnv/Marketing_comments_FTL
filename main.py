from dialog_bot_sdk.bot import DialogBot
import grpc
from globals import app as application
import sys

def on_msg(*params):
    print('on msg', params)
    bot.messaging.send_message(
        params[0].peer, 'Reply to : ' + str(params[0].message.textMessage.text)
    )


if __name__ == '__main__':
    application.run(port=5000 if len(sys.argv) == 1 else int(sys.argv[1]), threaded=True)
    bot = DialogBot.get_secure_bot(
        'hackathon-mob.transmit.im',  # bot endpoint (specify different endpoint if you want to connect to your on-premise environment)
        grpc.ssl_channel_credentials(), # SSL credentials (empty by default!)
        'd01418175003f742d2f2718cd66a177693ef4321',  # bot token
        verbose=False # optional parameter, when it's True bot prints info about the called methods, False by default
    )
    bot.messaging.on_message(on_msg)
