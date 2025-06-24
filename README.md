# 📚 Book API with FastAPI + MongoDB

This is a simple custom API built with **FastAPI** and **MongoDB** that allows users to **Create**, **Read**, **Update**, and **Delete** (CRUD) book entries.

---

🚀 Features

- ✅ Add new books
- 📖 Get all books
- 📝 Update a book by ID
- 🗑️ Delete a book by ID
- 🧪 Interactive Swagger Docs at `/docs`

---

🧰 Tech Stack

- Python 3.10+
- FastAPI
- MongoDB Atlas (NoSQL cloud database)
- Motor (Async MongoDB client)
- Uvicorn (for running the server)
- python-dotenv (for environment variables)
- Pytest & HTTPX for testing

---

🛠️ Setup Instructions


---

📦 1. Clone the repository


git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name



🐍 2. Create and activate a virtual environment

Open your terminal in the project folder and run:


python -m venv env      # create a virtual environment called "env"

Activate it:
On Windows (PowerShell):
    env\Scripts\activate

On macOS/Linux:
    source env/bin/activate

📥 3. Install the required packages

If you have a requirements.txt

     pip install -r requirements.txt

If not, install manually:

     pip install fastapi uvicorn motor python-dotenv


🔐 4. input your username and passsword in the cluster address with your MongoDB Atlas connection string .env file

MONGO_URI=mongodb+srv://yourUsername:yourPassword@cluster0.mongodb.net/?retryWrites=true&w=majority


▶️ 5. Run the server


uvicorn main:app --reload



🧪 6. Test the API

open new browsers and paste this new URL

Interactive Docs: http://localhost:8000/docs

Endpoint: http://localhost:8000/




How to Run Tests:

pytest --cov=main --cov-report=term-missing




📊 **Test Coverage**



![Test Coverage Screenshot](images/tests.png)