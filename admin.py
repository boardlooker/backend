import os
from contextlib import suppress

from flask import Flask
from flask_admin import Admin
from database.models import Boardgame, BoardgameLocation, Location
from database.session import SessionLocal


def init_flask() -> Flask:
    app = Flask('boardlooker_admin')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'TESTTERMINAL')
    app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

    def sqla_session_middleware(environ, start_response):
        with SessionLocal.begin():
            return wsgi_app(environ, start_response)

    wsgi_app = app.wsgi_app
    app.wsgi_app = sqla_session_middleware

    return app


app = init_flask()
admin = Admin(app, name='Boardlooker Admin', template_mode='bootstrap4')

from flask_admin.contrib.sqla import ModelView


class SQLAModelView(ModelView):
    is_id: bool = True
    column_display_pk = True

    model: type[ModelView]
    page_size = 40

    def __init__(self, model: type[ModelView] | None = None, **kwargs):
        super().__init__(model or self.model, SessionLocal(), **kwargs)


class BoardgameView(SQLAModelView):
    model = Boardgame

    column_filters = (
        'id',
        'title',
        'description',
        'year',
    )


class LocationView(SQLAModelView):
    model = Location

    column_filters = (
        'id',
        'title',
        'location',
        'location_city',
        'location_address',
        'location_type',
    )


class BoardgameLocationView(SQLAModelView):
    column_display_pk = True
    column_hide_backrefs = False
    model = BoardgameLocation

    column_filters = (
        'boardgame_id',
        'location_id',
        'available',
    )

    column_list = ['location', 'boardgame', 'available']


with SessionLocal.begin():
    admin.add_views(
        BoardgameView(name='Игры'),
        LocationView(name='Партнеры'),
        BoardgameLocationView(name='Игры у партнеров'),
    )

# XXX: Remove "Home" page
admin.menu().pop(0)

app.run('0.0.0.0', 4000)