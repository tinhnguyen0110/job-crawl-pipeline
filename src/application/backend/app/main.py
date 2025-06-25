# main.py (Professional Version with Enhanced Logging & Metrics - Fixed)

# =================================================================
# 1. KHAI BÁO THƯ VIỆN
# =================================================================
import os
import logging
import time
from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, Text, Date, desc, distinct
# SỬA LỖI: Thêm import `declarative_base` từ sqlalchemy.orm
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError
# SỬA LỖI: Thêm import `ConfigDict` từ pydantic
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

# Thư viện Prometheus Client
from prometheus_client import (
    Counter,
    Histogram,
    make_asgi_app,
    REGISTRY
)

# =================================================================
# 2. CẤU HÌNH LOGGING BÀI BẢN
# =================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - [%(funcName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =================================================================
# 3. ĐỊNH NGHĨA METRICS CHO PROMETHEUS
# =================================================================
# (Phần này giữ nguyên)
http_requests_total = Counter(
    "backend_http_requests_total",
    "Total number of HTTP requests made to the backend.",
    ["method", "endpoint", "http_status"]
)
http_requests_latency_seconds = Histogram(
    "backend_http_requests_latency_seconds",
    "HTTP request latency in seconds.",
    ["method", "endpoint"]
)
db_errors_total = Counter(
    "backend_database_errors_total",
    "Total number of database errors encountered."
)

# =================================================================
# 4. CẤU HÌNH TỪ BIẾN MÔI TRƯỜNG (PRODUCTION-READY)
# =================================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:123456@127.0.0.1:5432/job_db"
)
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174"
).split(",")

# =================================================================
# 5. THIẾT LẬP DATABASE VÀ ORM BASE
# =================================================================
try:
    logger.info(f"Attempting to connect to database using URL: {DATABASE_URL.split('@')[0]}@...")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as connection:
        logger.info("Database connection established successfully!")
except OperationalError as e:
    logger.critical(f"CRITICAL: Could not connect to the database. Error: {e}")
except Exception as e:
    logger.critical(f"CRITICAL: An unexpected error occurred during database setup: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SỬA LỖI: Khai báo Base ở đây, ngay sau khi có engine
Base = declarative_base()

# =================================================================
# 6. ĐỊNH NGHĨA MODEL VÀ SCHEMA
# =================================================================
class JobModel(Base):
    __tablename__ = "processed_jobs"
    id = Column(Integer, primary_key=True, index=True)
    raw_job_id = Column(Integer, unique=True, index=True)
    job_title = Column(Text, nullable=True)
    seniority = Column(Text, nullable=True)
    company = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    salary = Column(Text, nullable=True)
    job_description = Column(Text, nullable=True)
    job_requirements = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    date_posted = Column(Date, nullable=True)
    model = Column(Text, nullable=True)

class JobSchema(BaseModel):
    id: int
    raw_job_id: Optional[int] = None
    job_title: Optional[str] = None
    seniority: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    job_description: Optional[str] = None
    job_requirements: Optional[str] = None
    benefits: Optional[str] = None
    date_posted: Optional[date] = None
    model: Optional[str] = None

    # SỬA LỖI: Cập nhật cú pháp Pydantic v2, dùng model_config thay cho class Config
    model_config = ConfigDict(from_attributes=True)

# =================================================================
# 7. KHỞI TẠO ỨNG DỤNG FASTAPI VÀ MIDDLEWARE
# =================================================================
# (Phần này giữ nguyên, không thay đổi)
app = FastAPI(
    title="Crawl2Insight Job Search API",
    description="API to search and analyze job postings, instrumented with Prometheus metrics.",
    version="1.0.0"
)

@app.middleware("http")
async def metrics_and_logging_middleware(request: Request, call_next):
    # ... (logic middleware giữ nguyên)
    method = request.method
    endpoint = request.url.path
    if endpoint in ["/metrics", "/health"]:
        return await call_next(request)
    start_time = time.time()
    logger.info(f"Request started: {method} {endpoint}")
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        logger.error(f"Request failed with unhandled exception: {method} {endpoint}", exc_info=True)
        raise e
    finally:
        process_time = time.time() - start_time
        http_requests_latency_seconds.labels(method=method, endpoint=endpoint).observe(process_time)
        http_requests_total.labels(method=method, endpoint=endpoint, http_status=str(status_code)).inc()
        formatted_process_time = '{0:.2f}'.format(process_time * 1000)
        logger.info(f"Request finished: {method} {endpoint} - Status: {status_code} - Took: {formatted_process_time}ms")
    return response


logger.info(f"Configuring CORS for origins: {ALLOWED_ORIGINS}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_app = make_asgi_app(registry=REGISTRY)
app.mount("/metrics", metrics_app)

# =================================================================
# 8. DEPENDENCY VÀ ROUTER
# =================================================================
# (Phần này giữ nguyên, không thay đổi)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/api/v1")

@router.get("/jobs", response_model=List[JobSchema])
def read_jobs(
    # ... (logic endpoint giữ nguyên)
    searchTerm: Optional[str] = None,
    location: Optional[str] = None,
    seniority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(JobModel)
        if searchTerm:
            query = query.filter(JobModel.job_title.ilike(f"%{searchTerm}%"))
        if location:
            query = query.filter(JobModel.location.ilike(f"%{location}%"))
        if seniority:
            query = query.filter(JobModel.seniority == seniority)
        jobs = query.order_by(desc(JobModel.date_posted)).all()
        return jobs
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching jobs: {e}", exc_info=True)
        db_errors_total.inc()
        raise HTTPException(status_code=500, detail="A database error occurred.")


@router.get("/seniorities", response_model=List[str])
def get_seniorities(db: Session = Depends(get_db)):
    # ... (logic endpoint giữ nguyên)
    try:
        seniorities = db.query(distinct(JobModel.seniority)).all()
        return [s[0] for s in seniorities if s[0] is not None]
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching seniorities: {e}", exc_info=True)
        db_errors_total.inc()
        raise HTTPException(status_code=500, detail="A database error occurred.")


# =================================================================
# 9. THÊM ROUTER VÀ CÁC ENDPOINT CƠ BẢN VÀO APP
# =================================================================
app.include_router(router)

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Welcome to the Crawl2Insight Job Search API!"}

@app.get("/health", status_code=200)
def health_check():
    """Endpoint để Kubernetes Liveness/Readiness Probe kiểm tra sức khỏe."""
    return {"status": "ok"}

logger.info("Application startup complete. API is ready.")
