FROM python:3.12-slim

WORKDIR /assignment

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Install curl for Docker healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

# Upgrade pip
RUN pip install --upgrade pip

# Copy dependency files first
COPY pyproject.toml poetry.lock* /assignment/

# Install Python dependencies without installing the root package
RUN poetry install --no-root --only main --no-interaction --no-ansi

# Copy the rest of the application
COPY . /assignment/

EXPOSE 8000

CMD ["uvicorn", "assignment.main:app", "--host", "0.0.0.0", "--port", "8000"]