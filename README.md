# Opportunity — Job Portal

Opportunity is a small job portal built with **HTML, CSS, JavaScript, Python, Django, and PostgreSQL**. Job seekers can find jobs and apply. Employers can publish listings and review applicants. A site administrator can manage users, jobs, and applications through Django's admin area.

This project is suitable as a learning project and can be deployed to Render.

## What you can do

- Create an account as a job seeker or an employer, then log in and out.
- Search active job listings by keyword, location, category, and company.
- Read a job description and apply once, optionally including a cover letter.
- View your applications and their current status as a job seeker.
- Create, edit, close, and delete your own listings as an employer.
- Review applications to your listings and update their status.
- Manage all users, jobs, and applications as a site administrator.

## Technology

- **Django** serves the pages and handles accounts, forms, and application logic.
- **PostgreSQL** stores your data in local development and production.
- **HTML, CSS, and JavaScript** provide the responsive user interface.
- **Gunicorn** runs the Django app on Render, and **WhiteNoise** serves its static files.

## Run it on your computer

You will need Python 3.10 or newer and pip.

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   On macOS or Linux, use `python3 -m venv .venv` and `source .venv/bin/activate`.

3. Install the packages:

   ```shell
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and set your PostgreSQL credentials and a secret `SECRET_KEY`. The `.env` file is ignored by Git and loaded automatically by Django. Make sure PostgreSQL is running and the database exists.

5. Create the database tables and an administrator account:

   ```shell
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```shell
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/`. The admin area is at `http://127.0.0.1:8000/admin/`.

You can configure the database either with the `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT` variables shown in `.env.example`, or by setting `DATABASE_URL`. `DATABASE_URL` takes precedence when present.

## Deploy to Render

### Option A: Use the included Blueprint

1. Push this project to a GitHub repository.
2. In Render, choose **New → Blueprint**, then connect the repository.
3. Render reads `render.yaml` and creates a web service and PostgreSQL database. Review the plan before confirming; the example Blueprint uses free plans where available.
4. Wait for the first deployment to finish, then open the web service URL.
5. Create an administrator in the Render service's **Shell**:

   ```shell
   python manage.py createsuperuser
   ```

The Blueprint connects the web service to PostgreSQL, generates a `SECRET_KEY`, collects static files, and runs migrations as part of the build. Free-service availability, database duration, and persistence rules can change. Check Render's current plan details before deploying. For a live service or data you need to keep, choose a database plan with suitable backups and persistence.

### Option B: Configure the services yourself

1. Create a PostgreSQL database in Render and copy its **internal** connection URL.
2. Create a Render web service connected to your GitHub repository.
3. Set its build command to `bash build.sh` and its start command to `gunicorn config.wsgi:application`.
4. Add these environment variables to the web service:

   | Key | Value |
   | --- | --- |
   | `DATABASE_URL` | Internal connection URL for your Render PostgreSQL database |
   | `SECRET_KEY` | A new, long, random secret value |
   | `DEBUG` | `False` |

5. Deploy the service. In its **Shell**, create an administrator with `python manage.py createsuperuser`.
6. Visit the generated Render URL. Use `/admin/` to manage the site.

Render provides `RENDER_EXTERNAL_HOSTNAME` to the web service. The settings use it to allow the host, trust the HTTPS origin for form submissions, and enable HTTPS redirects.

## Accounts and roles

Select **Job seeker** or **Employer** when registering. Superusers are administrators and should be created with Django's `createsuperuser` command; they can manage the full site at `/admin/`.

Employers can only edit or delete their own job listings. Job applications belong to the job seeker and the relevant listing. Deleting a listing also deletes its applications.

## Useful commands

Run the automated tests:

```shell
python manage.py test
```

Check Django's project configuration:

```shell
python manage.py check
```

Collect static files (the Render build script does this automatically):

```shell
python manage.py collectstatic --no-input
```

## Project layout

```text
config/       Django project settings and server entry points
jobs/         User, job, and application models; forms, views, and tests
templates/    Page templates
static/       CSS and JavaScript
build.sh      Render build steps
render.yaml   Render Blueprint for the web service and database
```

## Before using it for a real business

This is a starter application, not a fully hardened commercial hiring system. Review account verification, privacy and data-retention requirements, backups, email delivery, accessibility, moderation, and security settings for your intended users. Keep `SECRET_KEY` private and never use `DEBUG=True` on a public deployment.
