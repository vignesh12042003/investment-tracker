# Investment Tracker

A modular full-stack investment tracking platform built using Django (backend API layer) and Streamlit (frontend interface).  
The system is designed with clear separation of concerns, scalable architecture, and maintainable UI modules.

---

## 🎯 Objective

To build a real-world portfolio management system that:

- Tracks user investments
- Fetches live stock market data
- Analyzes portfolio performance
- Provides actionable insights
- Maintains backend/frontend separation for scalability

---

## 🏗️ System Architecture

### Backend (Django)

- Handles authentication
- Manages portfolio data
- Exposes API endpoints
- Maintains database integrity
- Implements business logic

### Frontend (Streamlit)

- Consumes backend APIs
- Modular UI components inside `src/`
- Data visualization and analytics
- Lightweight interactive dashboard

Architecture follows a service-oriented separation pattern:
- Backend = Data + Logic
- Frontend = Presentation + Interaction

---

## 📁 Project Structure

```
INVESTMENT_TRACKER/
│
├── investment_backend/        # Django backend service
│   ├── backend/               # Project configuration
│   ├── tracker/               # Core investment app
│   ├── manage.py
│   └── db.sqlite3
│
├── src/                       # Modular frontend components
│   ├── watchlist.py
│   ├── portfolio_tracker.py
│   ├── stock_analysis.py
│   ├── new_insights.py
│   ├── profile.py
│   └── __init__.py
│
├── app.py                     # Streamlit entry point
├── main.py
└── README.md
```

---

## ✨ Core Features

- User authentication (Django-based)
- Portfolio CRUD operations
- Watchlist management
- Real-time stock integration
- Performance analytics
- Insight-driven UI modules
- Modular frontend design

---

## 🧠 Engineering Decisions

- Clear backend/frontend separation improves scalability.
- Modular frontend structure avoids monolithic UI code.
- Django chosen for robustness and authentication system.
- Streamlit selected for rapid analytics visualization.
- Folder-level organization improves maintainability.

---

## 🛠️ Tech Stack

- Python 3.12
- Django
- Streamlit
- SQLite (development)
- REST API communication
- Git version control

---

## ⚙️ Local Development Setup

### Clone Repository

```
git clone <repo-url>
cd INVESTMENT_TRACKER
```

### Backend Setup

```
cd investment_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

Open new terminal:

```
cd INVESTMENT_TRACKER
streamlit run app.py
```

---

## 🚀 Future Enhancements

- PostgreSQL migration
- API authentication tokens
- Docker containerization
- Cloud deployment (AWS / Render)
- Advanced portfolio analytics
- CI/CD integration

---

## 👨‍💻 Author

Vignesh  
Backend-focused Python & Django Developer  
Building scalable and structured web systems.
