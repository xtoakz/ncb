# NewsletterChat

A web application for managing your tasks and newsletters. Built with Flask and Supabase.

## Features

- User Authentication: Secure sign up and login functionality using Supabase Auth
- Task Management: Create, read, update, and delete tasks
- Newsletter Management: Create, read, update, and delete newsletters
- Topic Management: Create, read, update, and delete topics
- Dashboard: User-friendly dashboard to manage your tasks and newsletters
- Responsive Design: Works on desktop and mobile devices
- Modern UI: Clean and intuitive interface

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Backend: Flask (Python)
- Database: PostgreSQL (via Supabase)
- Authentication: Supabase Auth
- Icons: Lucide Icons

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Supabase account (for database and authentication)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/newsletter-chat.git
   cd newsletter-chat
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
newsletter-chat/
├── app/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── auth/
│   │   ├── newsletter/
│   │   └── todo/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── newsletter.py
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

- Flask
- Supabase
- Bootstrap
- Lucide Icons