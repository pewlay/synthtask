# SynthTask — Task Manager

**SynthTask** is a web-based application for managing tasks within a team. Users can create and assign tasks, set priorities and deadlines, and track tasks assigned to them.

## Features

- User authentication
- Create and manage task types
- Create and edit tasks with deadlines and priority levels
- Assign multiple executors to a single task
- Mark tasks as completed
- Unit tests covering core functionality
- Admin-exclusive access to create, update, and delete worker profiles and job positions

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/synthtask.git
cd synthtask
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate для Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Use the following credentials to log in:

```bash
Username: p_haltseva
Password: Test4567!

```
6. Start the development server:

```bash
python manage.py runserver
```

Once the server is running, open http://127.0.0.1:8000/ in your browser to access the application.
