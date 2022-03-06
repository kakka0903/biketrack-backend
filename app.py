from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.cfg')
    app.config.from_pyfile('config.local.cfg', silent=True)

    from api import api
    app.register_blueprint(api)

    from model import db, init_db, wipe_db
    db.init_app(app)
    app.cli.add_command(init_db)
    app.cli.add_command(wipe_db)

    from json_encoder import AlchemyEncoder
    app.json_encoder = AlchemyEncoder

    return app
