import os

from coincurve import PrivateKey
from pytest import fixture
from pytest_localserver.http import WSGIServer
from sqlalchemy.orm import sessionmaker

from nekoyume.app import create_app
from nekoyume.models import User, db


@fixture
def fx_app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'TEST_DATABASE_URL', 'sqlite:///test.db?check_same_thread=false'
    )
    app.config['SQLALCHEMY_BINDS'] = {
        'other_test': 'sqlite:///other_test.db?check_same_thread=false'
    }
    app.config['CELERY_ALWAYS_EAGER'] = True
    with app.app_context():
        yield app


@fixture
def fx_session(fx_app):
    fx_db = db
    fx_db.init_app(fx_app)
    fx_db.session.rollback()
    fx_db.drop_all()
    fx_db.session.commit()
    fx_db.create_all()
    return fx_db.session


@fixture
def fx_private_key() -> PrivateKey:
    return PrivateKey()


@fixture
def fx_user(fx_session, fx_private_key: PrivateKey):
    user = User(fx_private_key)
    user.session = fx_session
    return user


@fixture
def fx_server(request, fx_app):
    server = WSGIServer(application=fx_app.wsgi_app)
    server.start()
    request.addfinalizer(server.stop)
    return server


@fixture
def fx_test_client(fx_app):
    fx_app.testing = True
    return fx_app.test_client()


@fixture
def fx_other_test_client(fx_other_app):
    fx_other_app.testing = True
    return fx_other_app.test_client()


@fixture
def fx_other_app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'TEST_DATABASE_URL', 'sqlite:///other_test.db'
    )
    with app.app_context():
        yield app


@fixture
def fx_other_session(fx_app, fx_other_app):
    fx_db = db
    fx_db.init_app(fx_other_app)
    session = sessionmaker(fx_db.get_engine(fx_app, 'other_test'))()
    session.rollback()
    fx_db.drop_all()
    session.commit()
    fx_db.create_all()
    fx_db.init_app(fx_app)
    return session


@fixture
def fx_novice_status():
    return {
        'strength': '13',
        'dexterity': '12',
        'constitution': '16',
        'intelligence': '10',
        'wisdom': '8',
        'charisma': '5'
    }
