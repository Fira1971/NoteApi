from api import app, docs
from config import Config
from api.handlers import auth, note, user

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
docs.register(user.get_user_by_id)
docs.register(user.get_users)
docs.register(user.create_user)
docs.register(user.edit_user)
docs.register(user.delete_user)

docs.register(note.get_note_by_id)
docs.register(note.get_notes)
docs.register(note.create_note)
docs.register(note.edit_note)
docs.register(note.delete_note)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
