import pytest
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest

from tasks import Task

pytestmark = pytest.mark.django_db


def dummy_get_response(request):
    return None


@pytest.fixture
def http_request():
    request = HttpRequest()
    middleware = SessionMiddleware(dummy_get_response)
    middleware.process_request(request)
    return request


@pytest.fixture
def session(http_request):
    return http_request.session


@pytest.fixture
def cart(http_request, session):
    cart = Task(http_request)
    session.modified = False
    return cart


def test_create_empty_cart(http_request, session):
    assert session.get(settings.CART_SESSION_ID) is None
    Task(http_request)
    assert session[settings.CART_SESSION_ID] == {}


def test_get_non_empty_cart(http_request, session):
    session[settings.CART_SESSION_ID] = {"1": {}}
    Task(http_request)
    assert session[settings.CART_SESSION_ID] == {"1": {}}


def test_add_task_to_empty_cart(task, cart, session):
    cart.add(task)

    assert session[settings.CART_SESSION_ID] == {
        str(task.id): {"quantidade": 1, "valor": str(task.coin.valor)}
    }
    assert session.modified


def test_add_task_to_empty_cart_quantidade_gt_1(task, cart, session):
    cart.add(task, 2)

    assert session[settings.CART_SESSION_ID] == {
        str(task.id): {"quantidade": 2, "valor": str(task.coin.valor)}
    }
    assert session.modified


def test_add_task_to_empty_cart_twice(task, cart, session):
    cart.add(task)
    session.modified = False

    cart.add(task, 2)

    assert session[settings.CART_SESSION_ID] == {
        str(task.id): {"quantidade": 3, "valor": str(task.coin.valor)}
    }
    assert session.modified


def test_add_task_to_empty_cart_override_quantidade(task, cart, session):
    cart.add(task)
    session.modified = False

    cart.add(task, 4, override_quantidade=True)

    assert session[settings.CART_SESSION_ID] == {
        str(task.id): {"quantidade": 4, "valor": str(task.coin.valor)}
    }
    assert session.modified


def test_remove_task(task, cart, session):
    cart.add(task)
    session.modified = False

    cart.remove(task)
    assert session[settings.CART_SESSION_ID] == {}
    assert session.modified


def test_remove_task_not_in_cart(task, cart, session):
    cart.remove(task)
    assert session[settings.CART_SESSION_ID] == {}
    assert not session.modified


def taskFactory():
    print("Olas")

def test_cart_iter(cart, session):
    p1 = taskFactory()
    p2 = taskFactory()
    p3 = taskFactory()

    cart.add(p1)
    cart.add(p2, 2)
    cart.add(p3, 3)
    session.modified = False

    tasks = [p1, p2, p3]
    quantities = [1, 2, 3]

    for task, quantidade, item in zip(tasks, quantities, cart):
        assert task.valor == item["valor"]
        assert task.valor * quantidade == item["total_valor"]
        assert task == item["task"]
        assert "update_quantidade_form" in item

    assert not session.modified
    assert list(cart.cart.values()) != list(iter(cart))


def test_cart_length(cart):
    p1 = taskFactory()
    p2 = taskFactory()

    assert len(cart) == 0

    cart.add(p1)
    assert len(cart) == 1

    cart.add(p2, 3)
    assert len(cart) == 4


def test_get_total_valor(cart):
    p1 = taskFactory()
    p2 = taskFactory()

    cart.add(p1)
    cart.add(p2, 2)

    total_valor = (p1.valor * 1) + (p2.valor * 2)

    assert cart.get_total_valor() == total_valor


def test_cant_add_more_than_max_items(task, cart):
    cart.add(task, settings.CART_ITEM_MAX_quantidade)
    assert len(cart) == settings.CART_ITEM_MAX_quantidade

    cart.add(task, 1)
    assert len(cart) == settings.CART_ITEM_MAX_quantidade
