FROM python:3.10-slim


COPY ./requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install -r requirements.txt --no-cache-dir

COPY . .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "15400"]