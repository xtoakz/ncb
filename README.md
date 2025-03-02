# Todo App

A simple and efficient web application for managing your tasks and boosting productivity. Built with Flask and Supabase.

## Features

- **User Authentication**: Secure sign up and login functionality using Supabase Auth
- **Task Management**: Create, read, update, and delete tasks
- **Dashboard**: User-friendly dashboard to manage all your tasks
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean and intuitive interface with shadcn-inspired components

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: Supabase Auth
- **Icons**: Lucide Icons

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Supabase account (for database and authentication)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export SECRET_KEY=your_secret_key
   export SUPABASE_URL=your_supabase_url
   export SUPABASE_KEY=your_supabase_key
   ```
   
   On Windows:
   ```bash
   set FLASK_APP=run.py
   set FLASK_ENV=development
   set SECRET_KEY=your_secret_key
   set SUPABASE_URL=your_supabase_url
   set SUPABASE_KEY=your_supabase_key
   ```

5. Set up the database:
   - Create a new project in Supabase
   - Run the SQL queries in `supabase_schema.sql` in the Supabase SQL Editor

6. Run the application:
   ```bash
   flask run
   ```

7. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Sign up for a new account or log in with existing credentials
2. Add new tasks with title and description
3. Mark tasks as completed when done
4. Edit or delete tasks as needed
5. View your profile information

## Project Structure

```
todo-app/
├── app/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── auth/
│   │   ├── todo/
│   │   └── ...
│   ├── __init__.py
│   ├── auth.py
│   ├── routes.py
│   └── todo.py
├── supabase_schema.sql
├── supabase_client.py
├── config.py
├── run.py
└── requirements.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Supabase](https://supabase.io/)
- [Bootstrap](https://getbootstrap.com/)
- [Lucide Icons](https://lucide.dev/)