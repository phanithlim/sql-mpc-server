# Use a slim version of Python 3.12
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install curl and ca-certificates for uv installer
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates



# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed uv binary is on the `PATH`
# This line is for uv itself, not for project executables
ENV PATH="/root/.local/bin/:$PATH"

# Copy poetry files first to leverage Docker layer caching
# This includes pyproject.toml and poetry.lock (if you have one)
COPY pyproject.toml /app/

# Expose the application port
EXPOSE 8080

# Copy the rest of the application code
COPY . /app

# Install all dependencies using uv sync
# This creates the virtual environment and installs project dependencies
RUN uv sync --locked

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]