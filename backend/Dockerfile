FROM python:3.13-bookworm AS requirements_builder

WORKDIR /app

RUN pip install pipenv==2024.1.0

COPY Pipfile* .

RUN pipenv requirements > requirements.txt

FROM python:3.13-bookworm

WORKDIR /app

COPY --from=requirements_builder /app/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "fastapi", "run", "/app/main.py", "--port", "8000" ]