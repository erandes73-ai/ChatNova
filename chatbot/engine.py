import os
import re


# =========================================================
# KNOWLEDGE BASE PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

KNOWLEDGE_FILE = os.path.join(
    BASE_DIR,
    "knowledge.txt"
)

print("Knowledge file path:")
print(KNOWLEDGE_FILE)


# =========================================================
# DEFAULT RESPONSE
# =========================================================

DEFAULT_RESPONSE = (
    "Sorry, I don't have enough information to answer "
    "that question yet."
)


# =========================================================
# GREETINGS
# =========================================================

GREETINGS = {
    "hi": "Hello! 👋 How can I help you today?",
    "hello": "Hello! 👋 How can I help you today?",
    "hey": "Hey! 👋 What would you like to know?",
    "good morning": "Good morning! ☀️ How can I help you today?",
    "good afternoon": "Good afternoon! 😊 How can I help you?",
    "good evening": "Good evening! 🌙 How can I help you?"
}


# =========================================================
# LOAD KNOWLEDGE BASE
# =========================================================

def load_knowledge():

    knowledge = []

    print("Loading knowledge base...")
    print("File:", KNOWLEDGE_FILE)

    if not os.path.exists(KNOWLEDGE_FILE):

        print("ERROR: knowledge.txt does not exist!")

        return knowledge

    try:

        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                print("Reading:", line)

                if "|" not in line:

                    print(
                        "Skipping invalid line:",
                        line
                    )

                    continue

                question, answer = line.split(
                    "|",
                    1
                )

                question = question.strip()
                answer = answer.strip()

                if question and answer:

                    knowledge.append({

                        "question": question,

                        "answer": answer

                    })

    except Exception as e:

        print(
            "Knowledge loading error:",
            e
        )

    print(
        "Total knowledge entries:",
        len(knowledge)
    )

    return knowledge


# =========================================================
# PREPROCESS TEXT
# =========================================================

def preprocess(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# GET KEYWORDS
# =========================================================

def get_keywords(text):

    stop_words = {
        "what",
        "is",
        "are",
        "the",
        "a",
        "an",
        "who",
        "was",
        "were",
        "how",
        "why",
        "when",
        "where",
        "do",
        "does",
        "did",
        "tell",
        "me",
        "about",
        "can",
        "you",
        "please",
        "explain",
        "something",
        "define"
    }

    words = preprocess(text).split()

    keywords = [
        word
        for word in words
        if word not in stop_words
    ]

    return keywords


# =========================================================
# FIND BEST MATCH
# =========================================================

def find_best_match(
    user_message,
    knowledge
):

    user_clean = preprocess(user_message)

    user_keywords = set(
        get_keywords(user_message)
    )

    # -----------------------------------------------------
    # EXACT QUESTION MATCH
    # -----------------------------------------------------

    for item in knowledge:

        question_clean = preprocess(
            item["question"]
        )

        if user_clean == question_clean:

            return item["answer"]


    # -----------------------------------------------------
    # KEYWORD MATCHING
    # -----------------------------------------------------

    if not user_keywords:

        return None

    best_answer = None
    best_score = 0

    for item in knowledge:

        question_keywords = set(
            get_keywords(
                item["question"]
            )
        )

        if not question_keywords:

            continue

        common_words = (
            user_keywords
            &
            question_keywords
        )

        score = len(common_words)

        # ---------------------------------------------
        # BEST MATCH
        # ---------------------------------------------

        if score > best_score:

            best_score = score

            best_answer = item["answer"]


    # -----------------------------------------------------
    # REQUIRE AT LEAST ONE MATCH
    # -----------------------------------------------------

    if best_score >= 1:

        return best_answer


    return None


# =========================================================
# MAIN CHATBOT FUNCTION
# =========================================================

def get_response(user_message):

    if not user_message:

        return DEFAULT_RESPONSE


    # -----------------------------------------------------
    # CLEAN USER MESSAGE
    # -----------------------------------------------------

    cleaned_message = preprocess(
        user_message
    )


    # -----------------------------------------------------
    # GREETING
    # -----------------------------------------------------

    if cleaned_message in GREETINGS:

        return GREETINGS[
            cleaned_message
        ]


    # -----------------------------------------------------
    # LOAD KNOWLEDGE
    # -----------------------------------------------------

    knowledge = load_knowledge()

    print("KNOWLEDGE BASE:")
    print(knowledge)


    # -----------------------------------------------------
    # FIND ANSWER
    # -----------------------------------------------------

    answer = find_best_match(

        user_message,

        knowledge
    )


    # -----------------------------------------------------
    # RETURN ANSWER
    # -----------------------------------------------------

    if answer:

        return answer


    # -----------------------------------------------------
    # UNKNOWN QUESTION
    # -----------------------------------------------------

    return DEFAULT_RESPONSE