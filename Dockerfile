# Multi-Stage Production Dockerfile for Gnani Vachana 3D
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir --user -r backend/requirements.txt

FROM python:3.11-slim as runtime

WORKDIR /app

# Copy python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy project files
COPY backend /app/backend
COPY modules /app/modules
COPY avatars /app/avatars
COPY animations /app/animations
COPY audio /app/audio
COPY images /app/images
COPY fonts /app/fonts
COPY views /app/views
COPY poses /app/poses
COPY index.html /app/
COPY gnani-bridge.js /app/
COPY siteconfig.js /app/
COPY favicon.jpg /app/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python /app/backend/healthcheck.py || exit 1

CMD ["python", "backend/main.py"]
