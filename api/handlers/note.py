from flask_apispec import doc, marshal_with
from api import app, multi_auth, request
from api.models.note import NoteModel
from api.models.user import UserModel
from api.schemas.note import NoteRequestSchema, NoteSchema, note_schema, notes_schema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs

@app.route("/notes/<int:note_id>", methods=["GET"])
@doc(description='Api for notes.', tags=['Notes'], summary="Get note by id")
@marshal_with(NoteSchema, code=200)
@multi_auth.login_required
def get_note_by_id(note_id):
    # Авторизованный пользователь может получить только свою заметку или публичную заметку других пользователей
    #  Попытка получить чужую приватную заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    notes = NoteModel.query.join(NoteModel.author).filter((
        UserModel.id == user.id) | (NoteModel.private == False))
    if note in notes:
        return note, 200
    return {"error": "This note can't be showed"}, 403

    # note = get_object_or_404(NoteModel, note_id)
    # if note.author_id == user.id or (note.author_id != user.id and note.private == False):
    #     return note_schema.dump(note), 200
    # return {"error": "This note can't be showed"}, 403


@app.route("/notes", methods=["GET"])
@doc(description='Api for notes.', tags=['Notes'], summary="Get all user's notes and not-private notes")
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def get_notes():
    # Авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.join(NoteModel.author).filter((
        UserModel.id == user.id) | (NoteModel.private == False))
    return notes, 200


@app.route("/notes", methods=["POST"])
@doc(description='Api for notes.', tags=['Notes'], summary="Create new user's note")
@use_kwargs(NoteRequestSchema, location='json')
@marshal_with(NoteSchema, code=200)
@multi_auth.login_required
def create_note(**kwargs):
    user = multi_auth.current_user()
    note = NoteModel(**kwargs)
    # note_data = request.json
    # note = NoteModel(author_id=user.id, **note_data)
    if UserModel.id == user.id:
        note.save()
        return note, 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@doc(description='Api for notes.', tags=['Notes'], summary="Edit user's note")
@use_kwargs(NoteRequestSchema, location='json')
@marshal_with(NoteSchema, code=200)
@multi_auth.login_required
def edit_note(note_id, **kwargs):
    #  Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        for key, value in kwargs.items():
            setattr(user, key, value)
        # note_data = request.json
        # note.text = note_data["text"]
        # note.private = note_data.get("private") or note.private
        note.save()
        return note, 200
    return {"error": "This note can't be changed, because it's owned other person"}, 403


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@doc(description='Api for notes.', tags=['Notes'], summary="Delete user's note")
@marshal_with(NoteSchema, code=200)
@multi_auth.login_required
def delete_note(note_id):
    # Пользователь может удалять ТОЛЬКО свои заметки.
    # Попытка удалить чужую заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        note.delete()
        return {"message": f"Note with id={note_id} has deleted"}, 200
    return {"error": "This note can't be deleted, because it's owned other person"}, 403
