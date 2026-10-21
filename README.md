# fullstack_developer_capstone

Best Cars dealership portal, built from IBM Skills Network's Apache-licensed capstone starter.

## Components

- Django provides session authentication, registration, static About/Contact pages, a car catalog in SQLite, the admin UI, and proxy APIs.
- React provides the dealer list and state filter, dealer details/reviews, login, sign-up, logout, and authenticated review submission.
- Express and Mongoose serve dealerships and persist reviews in MongoDB. Initial seeding does not erase existing records.
- Flask and NLTK VADER classify review sentiment using the bundled lexicon.
- GitHub Actions builds the React client, runs Django tests, and builds the web container.

## Local development

Use Python 3.12 and Node.js 20 for consistency with CI.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r server/requirements.txt
npm ci --prefix server/frontend
npm run build --prefix server/frontend
cd server
python manage.py migrate
python manage.py seed_cars
python manage.py createsuperuser
python manage.py runserver
```

The Express API and sentiment service must also be running for dealership/review pages. `docker compose up --build` starts the four services, including MongoDB. Create the admin user inside the web container with `docker compose exec web python manage.py createsuperuser`.

Service addresses in local development: Django `http://localhost:8000`, Express `http://localhost:3030`, sentiment `http://localhost:5050`. For a remote lab, set `ALLOWED_HOSTS` to the provided application hostname and configure `CSRF_TRUSTED_ORIGINS` to its HTTPS origin. Keep existing MongoDB storage when restarting the application.

## Verification

```sh
cd server
python manage.py test
cd frontend
CI=true npm run build
```

Eight Django tests cover public pages, CSRF enforcement, registration/session establishment, login/logout, unauthorized reviews, server-side author attribution, backend outage handling, state filtering, and car-year validation. The original IBM starter remains credited under LICENSE. Deployment evidence and grading results are recorded only after actual execution.

## AI acknowledgement

OpenAI Codex assisted with implementing and reviewing the application, writing tests and deployment configuration, and diagnosing build failures on 21 October 2026. The application was checked by running the tests and production frontend build. No user claim of independently writing the generated code is made in this repository.

The About Us portraits are fictional images generated using OpenAI imagegen on 2026-10-21. Prompt: three distinct professional headshots in equal square panels for fictional staff Alex Morgan (sales), Jordan Lee (service), and Taylor Brooks (customer experience), consistent light gray backgrounds, natural light, no text or logos. The generated asset is server/frontend/static/team-portraits.png; CSS selects each panel. No generated image is used as execution evidence.
