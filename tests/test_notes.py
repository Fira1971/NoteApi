import pytest
from tests.init_test import client, application, auth_headers, auth_headers_user
from api.models.user import UserModel
from api.models.note import NoteModel


@pytest.fixture()
def user():
    user_data = {"username": "testuser", "password": "1234"}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def note(user):
    note_data = {"author_id": user.id,
                 "text": "Note for testuser", "private": False}
    note = NoteModel(**note_data)
    note.save()
    return note


@pytest.fixture()
def user_admin():
    user_data = {"username": "admin", "password": "admin"}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def note_admin(user_admin):
    note_data = {"author_id": user_admin.id, "text": "Quote for admin"}
    note = NoteModel(**note_data)
    note.save()
    return note


def test_note_get_by_id(client, note, auth_headers):
    response = client.get('/notes/1', headers=auth_headers)
    assert response.status_code == 200
    # assert len(response.json) == 3
    assert response.json["text"] == note.text


def test_note_get_by_id_user(client, note, auth_headers_user):
    response = client.get('/notes/1', headers=auth_headers_user)
    assert response.status_code == 200
    # assert len(response.json) == 3
    assert response.json["text"] == note.text


def test_get_notes(client, note, auth_headers):
    response = client.get('/notes', headers=auth_headers)
    assert response.status_code == 200


def test_note_not_found(client, note, auth_headers):
    response = client.get('/notes/100', headers=auth_headers)
    assert response.status_code == 404


def test_note_creation(client, auth_headers):
    note_data = {
        "text": "Quote for auth user",
        "private": False
    }
    response = client.post('/notes',
                           json=note_data,
                           headers=auth_headers,
                           )
    data = response.json
    assert response.status_code == 201
    assert note_data["text"] == data["text"]
    assert note_data["private"] == data["private"]


def test_note_edit(client, note_admin, auth_headers):
    note_edit_data = {
        "text": "Edited note"
    }
    response = client.put(f'/notes/{note_admin.id}',
                          json=note_edit_data,
                          headers=auth_headers,
                          )
    data = response.json
    assert response.status_code == 200
    assert data["text"] == note_edit_data["text"]


# @pytest.mark.skip(reason="test not implemented")
def test_note_delete(client, note, auth_headers_user):
    # Реализуйте тест на удаление заметки и запустите его, убрав декоратор @pytest.mark.skip
    response = client.get('/notes/1', headers=auth_headers_user)
    if response.status_code == 200:
        response = client.delete('/notes/1', headers=auth_headers_user)
        assert response.status_code == 200
    else:
        assert response.status_code == 404
