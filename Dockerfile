# Use an official Python runtime as a parent image
FROM python:3.9-slim
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . /app

# Install dependencies
# RUN pip install --no-progress-bar -r requirements.txt
RUN pip install --progress-bar off -r requirements.txt

# Copy the rest of the application code
# COPY . .

# Expose the port the app runs on
# EXPOSE 8000

# Command to run the FastAPI app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD uvicorn main:app --host=0.0.0.0 --port 8000:8000