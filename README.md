🤖 ChatNova
An intelligent AI-powered conversational assistant built with Flask, SQLite, and modern web technologies.**
ChatNova is a full-stack AI chatbot application designed to provide users with a clean, responsive, and personalized conversational experience.
The project includes user authentication, private conversations, conversation history, message persistence, and an extensible AI backend that can be connected to services such as OpenRouter.

---
✨ Features

🔐 User Authentication

* User registration
* User login and logout
* Password-based authentication
* Protected chat interface
* User-specific conversations

💬 AI Chat

* Real-time chat interface
* User and AI message separation
* Typing indicator
* Automatic message timestamps
* Enter to send messages
* Shift + Enter for a new line
* AI response integration architecture

🗂️ Conversation Management

* Create new conversations
* View previous conversations
* Switch between conversations
* Rename conversations
* Delete conversations
* Persistent conversation history

🎨 User Interface

* Responsive ChatNova interface
* Sidebar navigation
* Mobile sidebar
* Mobile overlay
* Modern message bubbles
* Responsive chat input
* Smooth message animations
* Custom scrollbar styling
* Authentication pages

🗄️ Database

ChatNova uses SQLite to persist:

* Users
* Conversations
* Messages
* Conversation history

---

## 🛠️ Tech Stack

| Technology       | Purpose                  |
| ---------------- | ------------------------ |
| Python           | Backend programming      |
| Flask            | Web framework            |
| Flask-Login      | Authentication           |
| Flask-SQLAlchemy | Database ORM             |
| SQLAlchemy       | Database interaction     |
| SQLite           | Local database           |
| HTML5            | Frontend structure       |
| CSS3             | UI and responsive design |
| JavaScript       | Chat functionality       |
| OpenRouter API   | AI model integration     |


---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/erandes73-ai/ChatNova.git
```

### 2. Enter the project directory

```bash
cd ChatNova
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

🔑 Environment Variables

ChatNova uses environment variables for sensitive credentials.

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

**Never commit `.env` to GitHub.**

The `.gitignore` file should contain:

```gitignore
.env
.env.*
venv/
.venv/
__pycache__/
*.pyc
instance/
*.db
*.sqlite
*.sqlite3
.vscode/
.idea/
```

---

🚀 Running ChatNova

Activate your virtual environment and run:

```bash
python app.py
```

Then open the local Flask server in your browser.

Usually:

```text
http://127.0.0.1:5000
```

---

## 🧠 AI Architecture

The planned AI request flow is:

```text
┌─────────────────────┐
│     ChatNova UI     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     JavaScript      │
│    chatbot.js       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Flask Backend    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    OpenRouter API   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      AI Model       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     AI Response     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    SQLite Database  │
└─────────────────────┘
```

This architecture keeps the API key on the server rather than exposing it in frontend JavaScript.

---

## 🔒 Security

ChatNova is designed with basic security principles in mind:

* API keys are stored in environment variables.
* `.env` is excluded from Git.
* User chat pages require authentication.
* User conversations are associated with their accounts.
* Sensitive local files are excluded from version control.

For production deployment, additional security measures should be implemented.

---

## 📱 Responsive Design

ChatNova supports:

* 💻 Desktop
* 💻 Laptop
* 📱 Mobile
* 📲 Tablet-sized screens

The sidebar automatically adapts to smaller screens and provides a mobile navigation experience.

---

## 🔮 Future Improvements

Planned improvements include:

* [ ] OpenRouter AI integration
* [ ] Conversation-aware AI responses
* [ ] Streaming AI responses
* [ ] Markdown rendering
* [ ] Code syntax highlighting
* [ ] Copy response button
* [ ] Regenerate response
* [ ] Stop generating button
* [ ] AI model selection
* [ ] Dark mode
* [ ] Premium glassmorphism UI
* [ ] File upload support
* [ ] Image understanding
* [ ] Voice input
* [ ] Voice output
* [ ] Conversation search
* [ ] Export conversations
* [ ] Production deployment
* [ ] Improved error handling
* [ ] API usage monitoring

---

## 🎯 Project Goals

The main goals of ChatNova are to:

1. Build a complete full-stack AI chatbot.
2. Understand Flask backend development.
3. Implement user authentication.
4. Build persistent conversation management.
5. Integrate external AI APIs.
6. Work with REST APIs.
7. Store and retrieve conversational data.
8. Create a modern responsive frontend.
9. Follow secure API-key management practices.
10. Deploy a complete AI application.

---

## 👨‍💻 Author

**Shubham Erande**

MCA | BSc Computer Science

Interests

* Python Development
* Data Analytics
* Power BI
* AI & Generative AI
* Flask
* Web Development
* Machine Learning

---

## 📄 License

This project is created for educational and portfolio purposes.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

### 🚧 Project Status

**Active Development**

ChatNova is continuously being improved with new AI capabilities, UI enhancements, and backend features.
