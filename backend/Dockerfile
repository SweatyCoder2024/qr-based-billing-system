# Start with a base Python image
FROM python:3.11-slim

# Set a neutral working directory
WORKDIR /code

# Copy the file with our list of libraries and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our application code from the local 'app' directory
# into a new 'app' directory inside our /code workdir
COPY ./app ./app

# Command to run the application.
# Because we are in /code, Python can now clearly see the 'app' package.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]