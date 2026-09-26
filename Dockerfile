FROM python:3.11-slim

# Install C-libraries required for MySQL client drivers (e.g., mysqlclient / PyMySQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libgl1 \
    libglib2.0-0 \
    libportaudio2 \
    portaudio19-dev \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definition first for layer caching
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY . .

ARG STREAMLIT_PORT_HOST

RUN echo "Access web-app: http://localhost:${STREAMLIT_PORT_HOST}"

CMD ["streamlit", "run", "app.py"]