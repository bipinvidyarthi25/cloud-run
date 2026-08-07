# 1. Use an official, lightweight Python base image
FROM python:3.12-slim

# 2. Set environment variables to optimize Python behavior inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy only dependency files first to utilize Docker layer caching
COPY requirements.txt .

# 5. Install Python dependencies without saving cache files
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application source code
COPY . .

# 7. Expose the port your application listens on (optional)
EXPOSE 8080

# 8. Define the final command to execute your application
CMD ["python", "main.py"]
