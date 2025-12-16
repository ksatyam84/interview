## Instructions

This is a test app with a simple form where you enter an equation, send it to the backend, and
receive the solution for the variable. The backend solution is not implemented yet.

Your task is:

- Implement the solver on the backend, return the result to the frontend, and render it.
- The preferable tool is `sympy`, but you may use any tools or libraries, plus documentation, AI,
  Stack Overflow, or search engines.

## Submitting the result

- Clone the repository to your GitHub account (you can make it private).
- Finish the task. It should be runnable in Docker compose.
- Send the link to your repo to engintern@corca.io
- After we review the result we will reach out to you and schedule a follow-up call. On this call we
  will ask additional questions related to this task and ask you to add more functionality.

## Run App With Docker Compose

Install [Docker](https://www.docker.com/), then run:

```bash
docker-compose up --build
```

Open the app at [http://localhost:5173](http://localhost:5173). Live reload works for both frontend
and backend code.

## Run The App Directly

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host --port 5173
```

Open the app at [http://localhost:5173](http://localhost:5173). Live reload works for both frontend
and backend code.
