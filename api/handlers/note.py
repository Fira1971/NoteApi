from api import app, multi_auth, request
from api.models.note import NoteModel
from api.models.user import UserModel
from api.schemas.note import note_schema, notes_schema
from utility.helpers import get_object_or_404


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
def get_note_by_id(note_id):
    # Авторизованный пользователь может получить только свою заметку или публичную заметку других пользователей
    #  Попытка получить чужую приватную заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    notes = NoteModel.query.join(NoteModel.author).filter((
        UserModel.id == user.id) | (NoteModel.private == False))
    if note in notes:
        return note_schema.dump(note), 200
    return {"error": "This note can't be showed"}, 403

    # note = get_object_or_404(NoteModel, note_id)
    # if note.author_id == user.id or (note.author_id != user.id and note.private == False):
    #     return note_schema.dump(note), 200
    # return {"error": "This note can't be showed"}, 403


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
def get_notes():
    # Авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.join(NoteModel.author).filter((
        UserModel.id == user.id) | (NoteModel.private == False))
    return note_schema.dump(notes), 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
def create_note():
    user = multi_auth.current_user()
    note_data = request.json
    note = NoteModel(author_id=user.id, **note_data)
    note.save()
    return note_schema.dump(note), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
def edit_note(note_id):
    #  Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        note_data = request.json
        note.text = note_data["text"]
        note.private = note_data.get("private") or note.private
        note.save()
        return note_schema.dump(note), 200
    return {"error": "This note can't be changed, because it's owned other person"}, 403


@app.route("/notes/<int:note_id>", methods=["DELETE"])
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
