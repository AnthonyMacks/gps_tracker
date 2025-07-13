# 🐍 Use Python base image
FROM python:3.11-slim

# 📁 Set working directory
WORKDIR /app

# 📦 Copy all source files
COPY . .

# 🧪 Install dependencies
RUN pip install --upgrade pip \
    && pip install flask flask_socketio eventlet gunicorn

# 🔥 Expose Flask port
EXPOSE 5000

# 🚀 Start using Gunicorn + eventlet
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "app:app"]
