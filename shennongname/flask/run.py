from shennongname.flask.config import PORT, DEBUG
from shennongname.flask.blueprint.snn import blueprint_snn

from flask import Flask


def create_app():
    app = Flask(__name__)
    # Register blueprints
    app.register_blueprint(blueprint_snn)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
