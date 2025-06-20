FROM apache/airflow:2.10.5-python3.12
# 👇 Cài Python packages (khuyến nghị Airflow chạy dưới user airflow)
USER airflow
# Copy requirements.txt và cài Python dependencies bằng pip (bắt buộc ở user airflow)
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN pip install playwright && \
    python -m playwright install

USER root
RUN apt-get update && apt-get install -y libnss3 libatk1.0-0 libxss1 libasound2 libxshmfence1 libgbm1 libdbus-1-3 \
    libatk-bridge2.0-0 libcups2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxrandr2 libxfixes3 libpango-1.0-0 libcairo2

# Trở lại user airflow
USER airflow

#test
ENV PATH=/home/airflow/.local/bin:$PATH \
    PYTHONPATH=/home/airflow/.local/lib/python3.12/site-packages:$PYTHONPATH