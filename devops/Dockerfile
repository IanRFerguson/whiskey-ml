FROM python:3.10-bullseye

WORKDIR /app

# Copying the project file first should allow you to used cached dependencies
COPY pyproject.toml .  
RUN pip install .

# Now we'll copy everything else into the virtualized environment
COPY . .

WORKDIR /app/src

CMD ["sleep", "infinity"]