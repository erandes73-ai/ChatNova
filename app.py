from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import db

from chatbot.engine import get_response

from models.models import (
    User,
    Message,
    Conversation
)


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# APP CONFIGURATION
# =========================================================

app.config["SECRET_KEY"] = "chatnova-secret-key-change-later"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatnova.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================================================
# DATABASE
# =========================================================

db.init_app(app)


# =========================================================
# FLASK LOGIN
# =========================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
@login_required
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if not username or not email or not password:

            return "All fields are required."


        # ---------------------------------------------
        # CHECK USERNAME
        # ---------------------------------------------

        existing_username = User.query.filter_by(
            username=username
        ).first()


        if existing_username:

            return "Username already exists."


        # ---------------------------------------------
        # CHECK EMAIL
        # ---------------------------------------------

        existing_email = User.query.filter_by(
            email=email
        ).first()


        if existing_email:

            return "Email already registered."


        # ---------------------------------------------
        # HASH PASSWORD
        # ---------------------------------------------

        password_hash = generate_password_hash(
            password
        )


        # ---------------------------------------------
        # CREATE USER
        # ---------------------------------------------

        new_user = User(

            username=username,

            email=email,

            password_hash=password_hash

        )


        db.session.add(
            new_user
        )

        db.session.commit()


        # ---------------------------------------------
        # REDIRECT TO LOGIN
        # ---------------------------------------------

        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username_or_email = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if not username_or_email or not password:

            return "Username/email and password are required."


        # ---------------------------------------------
        # FIND USER
        # ---------------------------------------------

        user = User.query.filter(

            (User.username == username_or_email) |

            (User.email == username_or_email)

        ).first()


        # ---------------------------------------------
        # CHECK PASSWORD
        # ---------------------------------------------

        if user and check_password_hash(

            user.password_hash,

            password

        ):

            login_user(user)

            return redirect(
                url_for("home")
            )


        # ---------------------------------------------
        # INVALID LOGIN
        # ---------------------------------------------

        return "Invalid username/email or password."


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# =========================================================
# CREATE NEW CONVERSATION
# =========================================================

@app.route(
    "/conversations",
    methods=["POST"]
)
@login_required
def create_conversation():

    try:

        conversation = Conversation(

            title="New Chat",

            user_id=current_user.id

        )


        db.session.add(
            conversation
        )

        db.session.commit()


        return jsonify({

            "success": True,

            "conversation": {

                "id": conversation.id,

                "title": conversation.title

            }

        }), 201


    except Exception as e:

        print(
            "CREATE CONVERSATION ERROR:",
            e
        )

        db.session.rollback()


        return jsonify({

            "error":
                "Could not create conversation."

        }), 500


# =========================================================
# GET USER CONVERSATIONS
# =========================================================

@app.route(
    "/conversations",
    methods=["GET"]
)
@login_required
def conversations():

    try:

        user_conversations = Conversation.query.filter_by(

            user_id=current_user.id

        ).order_by(

            Conversation.updated_at.desc()

        ).all()


        conversations_data = []


        for conversation in user_conversations:

            conversations_data.append({

                "id":
                    conversation.id,

                "title":
                    conversation.title,

                "created_at": (

                    conversation.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if conversation.created_at

                    else ""

                ),

                "updated_at": (

                    conversation.updated_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if conversation.updated_at

                    else ""

                )

            })


        return jsonify(
            conversations_data
        ), 200


    except Exception as e:

        print(
            "CONVERSATIONS ERROR:",
            e
        )


        return jsonify({

            "error":
                "Unable to load conversations."

        }), 500


# =========================================================
# GET SINGLE CONVERSATION
# =========================================================

@app.route(
    "/conversation/<int:conversation_id>",
    methods=["GET"]
)
@login_required
def get_conversation(conversation_id):

    try:

        # ---------------------------------------------
        # FIND USER'S CONVERSATION
        # ---------------------------------------------

        conversation = Conversation.query.filter_by(

            id=conversation_id,

            user_id=current_user.id

        ).first()


        # ---------------------------------------------
        # NOT FOUND
        # ---------------------------------------------

        if not conversation:

            return jsonify({

                "error":
                    "Conversation not found."

            }), 404


        # ---------------------------------------------
        # GET MESSAGES
        # ---------------------------------------------

        messages = Message.query.filter_by(

            conversation_id=conversation.id,

            user_id=current_user.id

        ).order_by(

            Message.timestamp.asc()

        ).all()


        messages_data = []


        for message in messages:

            messages_data.append({

                "user_message":
                    message.user_message,

                "bot_response":
                    message.bot_response,

                "timestamp": (

                    message.timestamp.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if message.timestamp

                    else ""

                )

            })


        return jsonify({

            "id":
                conversation.id,

            "title":
                conversation.title,

            "messages":
                messages_data

        }), 200


    except Exception as e:

        print(
            "GET CONVERSATION ERROR:",
            e
        )


        return jsonify({

            "error":
                "Unable to load conversation."

        }), 500


# =========================================================
# RENAME CONVERSATION
# =========================================================

@app.route(
    "/conversation/<int:conversation_id>",
    methods=["PATCH"]
)
@login_required
def rename_conversation(conversation_id):

    try:

        data = request.get_json()


        if not data:

            return jsonify({

                "error":
                    "Invalid request."

            }), 400


        new_title = data.get(
            "title",
            ""
        ).strip()


        # ---------------------------------------------
        # VALIDATE TITLE
        # ---------------------------------------------

        if not new_title:

            return jsonify({

                "error":
                    "Conversation title cannot be empty."

            }), 400


        if len(new_title) > 200:

            return jsonify({

                "error":
                    "Conversation title is too long."

            }), 400


        # ---------------------------------------------
        # FIND CONVERSATION
        # ---------------------------------------------

        conversation = Conversation.query.filter_by(

            id=conversation_id,

            user_id=current_user.id

        ).first()


        if not conversation:

            return jsonify({

                "error":
                    "Conversation not found."

            }), 404


        # ---------------------------------------------
        # UPDATE TITLE
        # ---------------------------------------------

        conversation.title = new_title

        conversation.updated_at = datetime.utcnow()


        db.session.commit()


        return jsonify({

            "success": True,

            "id":
                conversation.id,

            "title":
                conversation.title

        }), 200


    except Exception as e:

        print(
            "RENAME CONVERSATION ERROR:",
            e
        )

        db.session.rollback()


        return jsonify({

            "error":
                "Unable to rename conversation."

        }), 500


# =========================================================
# DELETE CONVERSATION
# =========================================================

@app.route(
    "/conversation/<int:conversation_id>",
    methods=["DELETE"]
)
@login_required
def delete_conversation(conversation_id):

    try:

        # ---------------------------------------------
        # FIND USER'S CONVERSATION
        # ---------------------------------------------

        conversation = Conversation.query.filter_by(

            id=conversation_id,

            user_id=current_user.id

        ).first()


        # ---------------------------------------------
        # NOT FOUND
        # ---------------------------------------------

        if not conversation:

            return jsonify({

                "error":
                    "Conversation not found."

            }), 404


        # ---------------------------------------------
        # DELETE
        # ---------------------------------------------

        db.session.delete(
            conversation
        )

        db.session.commit()


        return jsonify({

            "success": True,

            "message":
                "Conversation deleted successfully."

        }), 200


    except Exception as e:

        print(
            "DELETE CONVERSATION ERROR:",
            e
        )

        db.session.rollback()


        return jsonify({

            "error":
                "Unable to delete conversation."

        }), 500


# =========================================================
# CHAT
# =========================================================

@app.route(
    "/chat",
    methods=["POST"]
)
@login_required
def chat():

    try:

        # ---------------------------------------------
        # GET JSON DATA
        # ---------------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({

                "error":
                    "Invalid request."

            }), 400


        # ---------------------------------------------
        # GET USER MESSAGE
        # ---------------------------------------------

        user_message = data.get(
            "message",
            ""
        ).strip()


        # ---------------------------------------------
        # EMPTY MESSAGE
        # ---------------------------------------------

        if not user_message:

            return jsonify({

                "error":
                    "Message cannot be empty."

            }), 400


        # ---------------------------------------------
        # GET CONVERSATION ID
        # ---------------------------------------------

        conversation_id = data.get(
            "conversation_id"
        )


        conversation = None


        # ---------------------------------------------
        # FIND EXISTING CONVERSATION
        # ---------------------------------------------

        if conversation_id:

            try:

                conversation_id = int(
                    conversation_id
                )

            except (
                ValueError,
                TypeError
            ):

                conversation_id = None


            if conversation_id:

                conversation = Conversation.query.filter_by(

                    id=conversation_id,

                    user_id=current_user.id

                ).first()


                if not conversation:

                    return jsonify({

                        "error":
                            "Conversation not found."

                    }), 404


        # ---------------------------------------------
        # CREATE CONVERSATION IF NEEDED
        # ---------------------------------------------

        if not conversation:

            title = user_message[:50]


            if len(user_message) > 50:

                title += "..."


            conversation = Conversation(

                title=title,

                user_id=current_user.id

            )


            db.session.add(
                conversation
            )

            db.session.flush()


        # ---------------------------------------------
        # GET CHATBOT RESPONSE
        # ---------------------------------------------

        bot_response = get_response(
            user_message
        )


        # ---------------------------------------------
        # CREATE MESSAGE
        # ---------------------------------------------

        new_message = Message(

            user_id=current_user.id,

            conversation_id=conversation.id,

            user_message=user_message,

            bot_response=bot_response,

            timestamp=datetime.utcnow()

        )


        db.session.add(
            new_message
        )


        # ---------------------------------------------
        # UPDATE CONVERSATION
        # ---------------------------------------------

        conversation.updated_at = datetime.utcnow()


        # ---------------------------------------------
        # UPDATE TITLE
        # ---------------------------------------------

        if conversation.title == "New Chat":

            conversation.title = user_message[:50]


            if len(user_message) > 50:

                conversation.title += "..."


        # ---------------------------------------------
        # COMMIT
        # ---------------------------------------------

        db.session.commit()


        # ---------------------------------------------
        # SEND RESPONSE
        # ---------------------------------------------

        return jsonify({

            "response":
                bot_response,

            "conversation_id":
                conversation.id,

            "conversation_title":
                conversation.title

        }), 200


    except Exception as e:

        print(
            "CHAT ERROR:",
            e
        )


        db.session.rollback()


        return jsonify({

            "error":
                "Sorry, something went wrong. "
                "Please try again."

        }), 500


# =========================================================
# CHAT HISTORY
# =========================================================

@app.route(
    "/history",
    methods=["GET"]
)
@login_required
def history():

    try:

        messages = Message.query.filter_by(

            user_id=current_user.id

        ).order_by(

            Message.timestamp.asc()

        ).all()


        history_data = []


        for message in messages:

            history_data.append({

                "user_message":
                    message.user_message,

                "bot_response":
                    message.bot_response,

                "timestamp": (

                    message.timestamp.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if message.timestamp

                    else ""

                ),

                "conversation_id":
                    message.conversation_id

            })


        return jsonify(
            history_data
        ), 200


    except Exception as e:

        print(
            "HISTORY ERROR:",
            e
        )


        return jsonify({

            "error":
                "Unable to load chat history."

        }), 500


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )