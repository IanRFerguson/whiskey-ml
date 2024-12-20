FROM python:3.10-bullseye

WORKDIR /app

# Copying the requirements file first should allow you to used cached dependencies
COPY dev/requirements.txt .
RUN pip install -r dev/requirements.txt

COPY . .

WORKDIR /app/src

CMD ["sleep", "infinity"]