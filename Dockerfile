# ===============================
# Base Image
# ===============================
FROM python:3.10-slim

# ===============================
# Environment
# ===============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ===============================
# System Dependencies
# ===============================
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Workdir
# ===============================
WORKDIR /app

# ===============================
# Install Python Dependencies
# ===============================
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ===============================
# Copy Application Code
# ===============================
COPY . .

# ===============================
# Expose Port
# ===============================
EXPOSE 8000

# ===============================
# Run Application
# ===============================
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
