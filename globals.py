from flask import g, Flask

# тут содержатся глобальные переменные для всего приложения

app = Flask(__name__)  # главное приложение # бот, через которого ведется общение


# не импортируете его напрямую, иначе у вас будет объект бота, который был в начале работы программы, а не текущий
# вместо этого используйте get_bot() и set_bot()
# тоже самое с app

def set_app(_app):
    global app
    app = _app


def get_app():
    global app
    return app


def set_bot(_bot):
    global bot
    bot = _bot


def get_bot():
    global bot
    return bot