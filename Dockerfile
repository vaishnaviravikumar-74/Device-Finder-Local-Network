FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Create .streamlit directory for config
RUN mkdir -p ~/.streamlit

# Create Streamlit config
RUN echo "[server]\nport = 8501\naddress = 0.0.0.0\nheadless = true\nenableXsrfProtection = false\n" > ~/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
