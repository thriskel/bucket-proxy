FROM python:3.12.0

WORKDIR /app


COPY requirements/ /app/requirements/

RUN pip install --upgrade pip setuptools wheel && pip install -r requirements/default.txt


COPY src /app


CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
