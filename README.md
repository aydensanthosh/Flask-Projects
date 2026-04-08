# 🚀 Flask To-Do App

A clean and minimal To-Do List Web Application built using Flask and SQLAlchemy, designed to help users manage tasks efficiently with deadlines.

## 📌 Features
- ✅ Add new tasks with due dates
- 📝 Update existing tasks
- ❌ Delete tasks
- 📅 Track task creation time
- ⚡ Fast and lightweight (SQLite backend)
- 🔁 Auto-refresh with Flask debug mode

## 🛠️ Tech Stack
- Backend: Flask
- Database: SQLite (via SQLAlchemy ORM)
- Frontend: HTML (Jinja2 Templates)
- Language: Python

## 📂 Project Structure
```bash
To-Do-App/
│── app.py              # Main application file
│── To-Do-app.db        # SQLite database
│── templates/          # HTML templates directory
│   ├── index.html      # Homepage template
│   └── update.html     # Update task template
│── static/             # Static files (CSS, JS, images)
└── README.md           # Project documentation
```
## ⚙️ Installation & Setup
Clone the repository
```bash
git clone https://github.com/your-username/flask-todo-app.git
cd flask-todo-app
```
Install dependencies
```bash
pip install "requirements.txt"
```
Run the application
```bash
python app.py
```
Open in browser:
<a href="http://127.0.0.1:5000/" target="blank">http://127.0.0.1:5000/</a>

##🧠 How It Works
- Tasks are stored in a SQLite database
- Each task contains:
  - Content
  - Due Date
  - Creation Timestamp

Flask routes handle:
|Route|Function|
|-----------|-----------|
|/|  Add & View tasks|
|/delete/<id>| Delete task|
|/update/<id>| Update task|

## ✨ Screenshots (Optional)
Add screenshots here to make it even more attractive

## 🧑‍💻 Developer's Creed
> "1% better everyday is 3773% better by the end of the year"
**- James Clear (from "Atomic Habits")**

🔹 Write code that humans understand first, machines second
🔹 Simplicity > Complexity
🔹 Consistency builds mastery
🔹 Ship, learn, improve, repeat


##📬 Connect With Me
- 💼 LinkedIn: [Ayden Santhosh](https://www.linkedin.com/in/ayden-santhosh-b307b8355/)
- 🐙 GitHub: [@aydensanthosh](https://github.com/aydensanthosh)

## ⭐ Show Your Support
If you like this project, give it a ⭐ on GitHub — it motivates me to build more!
