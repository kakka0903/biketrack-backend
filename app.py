import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    from api import api
    app.register_blueprint(api)

    from model import db
    db.init_app(app)

    app.config.from_pyfile('config.cfg')
    app.config.from_pyfile('config.local.cfg', silent=True)

    try:
        if os.environ["UNIVERSAL_API_KEY"]:
            app.logger.warning("Don't use UNIVERSAL_API_KET in prod")
            app.logger.warning(
                "Anyone with access to the key can post fake data")
    except KeyError:
        pass

    return app
