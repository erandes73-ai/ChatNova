import os
import sys


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


# =========================================================
# IMPORT CHATBOT ENGINE
# =========================================================

from chatbot.engine import get_response


# =========================================================
# CONSOLE CHATBOT
# =========================================================

def main():

    print("=" * 60)
    print("ChatNova Console Chatbot")
    print("=" * 60)

    print(
        "\nChatbot is ready! Type 'exit' to quit.\n"
    )


    while True:

        user_message = input(
            "You: "
        ).strip()


        # ---------------------------------------------
        # EXIT
        # ---------------------------------------------

        if user_message.lower() == "exit":

            print(
                "Chatbot: Goodbye! 👋"
            )

            break


        # ---------------------------------------------
        # EMPTY INPUT
        # ---------------------------------------------

        if not user_message:

            print(
                "Chatbot: Please enter a message."
            )

            continue


        # ---------------------------------------------
        # GET RESPONSE
        # ---------------------------------------------

        response = get_response(
            user_message
        )


        # ---------------------------------------------
        # DISPLAY RESPONSE
        # ---------------------------------------------

        print(
            f"Chatbot: {response}"
        )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    main()