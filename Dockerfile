FROM python:3.11-slim

# ติดตั้งไลบรารีที่จำเป็นสำหรับการคอมไพล์ไลบรารี Python (เช่น mysqlclient)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        gcc build-essential pkg-config curl ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/*

# สร้าง directory สำหรับแอป
WORKDIR /app

# ติดตั้ง dependencies ของ Python
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกซอร์สโค้ดเข้า container
# (รวม package.json สำหรับการติดตั้ง Node deps)
COPY . /app

# ติดตั้ง Node.js (ใช้ NodeSource สำหรับเวอร์ชัน 18) เพื่อให้สามารถรัน Tailwind
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get update && apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# ติดตั้ง dependencies ของ Node (ถ้ามี package.json) และ build Tailwind
RUN if [ -f package.json ]; then npm ci --silent || npm install --silent; fi
RUN if [ -f package.json ]; then npm run build --silent || true; fi

# ตั้งค่าพื้นฐาน Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# เปิดพอร์ต 8000 สำหรับ Django
EXPOSE 8000

# ค่าเริ่มต้น: ใน runtime เราจะรันคำสั่งที่เก็บ static, migrate และรัน server

