# Personal Blog Application

This is a _Flask based_ personal blog application, built as an exam of an backend course - PRO1002.
Its main focus are on database integration (SQLite), templating with Jinja2, user authentication and basic web app functionality.

The user can:

- Read blog posts (with images, descriptions and tags).
- Filter posts by tags.
- Add comments.

Admin can:

- Create, edit and delete posts and comments.

## Features

- Flask framework + Jinja2 templates.
- SQLite database integration
- Blog posts with title, description, content, date, tags and image.
- Tag page: filter posts by tag.
- Comments: add and view comments on the post itself.
- Search post: (client side filter)
- Admin login system: (basic session authentication)
- Flash messages on actions (create, delete, edit and such)
- 404 custom error page.
- Tested and documented.

## How to use it

### 1. Clone the repository

Go to where you wish to place this repo, and clone it there.

```
git clone https://github.com/bjornum/main_assignment_blog.git
```

### 2. Create and activate a virtual environment

First create the virtual environment - the venv

```
python -m venv venv
```

Then activate the virtual environment

#### On Windows

```
venv\Scripts\activate
```

#### On macOS/Linux

```
source venv/bin/activate
```

### 3. Install the dependencies

```
pip install -r requirements.txt
```

### 4. Initialize the database

```
flask --app run.py init-db
```

### 5. Seed the database with data.

This will create the content and admin user on the application

#### Seed the blog content

```
python seed.py
```

#### Seed the Admin user

```
python seed_users.py
```

### 6. Run the Application

#### Ideal way of running it

```
flask --app run.py run
```

#### Running it directly from the python file

```
python run.py
```

### 7. Run the tests

#### Easiest way to run it with a script i made

```
.\run-tests.ps1
```

#### Can also run it like this

```
$env:PYTHONPATH = "."
```

Then the command below.

```
pytest
```

## Admin User

Admin can create, edit and delete posts and comments

- Username: admin
- Password: admin123

Normal users will only be able to create post, and add comments.

## Future Improvements

- Implement an image upload for posts.
- Register and propper authentiation system.
- Pagination for posts
- Deploy to an cloud platform.
- Improve the visuals and UX/UI of it.
