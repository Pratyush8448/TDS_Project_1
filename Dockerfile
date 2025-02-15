# Base Image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all necessary files
COPY . /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "MAIN:app", "--host", "0.0.0.0", "--port", "8000"]
