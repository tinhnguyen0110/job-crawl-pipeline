# --- GIAI ĐOẠN 1: BUILD ---
FROM python:3.11-slim as builder

WORKDIR /app

# Cài đặt build dependencies nếu cần
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy và cài đặt requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source code
COPY ./app ./app

# --- GIAI ĐOẠN 2: FINAL ---
FROM python:3.11-slim

# Tạo user non-root cho bảo mật
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Copy Python packages từ builder
COPY --from=builder /root/.local /home/app/.local
COPY --from=builder /app/app ./app

# Chuyển ownership cho user app
RUN chown -R app:app /app

# Đảm bảo PATH bao gồm .local/bin
ENV PATH=/home/app/.local/bin:$PATH

# Chuyển sang user non-root
USER app

EXPOSE 8000

# Health check (tùy chọn)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]