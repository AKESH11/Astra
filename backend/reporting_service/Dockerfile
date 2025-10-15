# This is the recipe for building each Python service.
# It MUST be named "Dockerfile" with a capital 'D'.

FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# --- DIAGNOSTIC STEP ---
# Copy all files first and list them to ensure requirements.txt is present.
# This will show us exactly what Docker's build context sees.
COPY . .
RUN echo "--- Listing files in /app to verify context ---" && ls -la

# Install the libraries from the list. The -v flag adds verbosity.
# This will fail loudly if requirements.txt is not found.
RUN echo "--- Installing packages from requirements.txt ---" && \
    pip install -v --no-cache-dir -r requirements.txt

# The code is already copied, so we don't need to do it again.

