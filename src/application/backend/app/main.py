# main.py (Professional Version with Enhanced Logging)

# 1. KHAI BÁO THƯ VIỆN
import os
import logging
import time
from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, Text, Date, desc, distinct
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy.exc import OperationalError

# 2. CẤU HÌNH LOGGING BÀI BẢN
# =================================================================
logging.basicConfig(
    level=logging.INFO, # Đặt mức log mặc định là INFO
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
# =================================================================


# 3. CẤU HÌNH TỪ BIẾN MÔI TRƯỜNG (PRODUCTION-READY)
# =================================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@127.0.0.1:5432/job_db" # Fallback cho local dev
)

DATABASE_URL = "postgresql+psycopg2://postgres:123456@127.0.0.1:5432/job_db"
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://35.186.144.250,http://34.54.46.178,http://localhost:5173,http://localhost:5174" # Fallback cho local dev
)
# =================================================================


# 4. THIẾT LẬP KẾT NỐI DATABASE VÀ KIỂM TRA
# =================================================================
try:
    logger.info(f"Attempting to connect to database at host: {DATABASE_URL.split('@')[-1]}")
    engine = create_engine(DATABASE_URL)
    # Thử kết nối để xác nhận
    with engine.connect() as connection:
        logger.info("Database connection successful!")
except OperationalError as e:
    logger.critical(f"CRITICAL: Failed to connect to the database: {e}")
    # Trong môi trường thực tế, bạn có thể muốn ứng dụng thoát ở đây
    # import sys
    # sys.exit(1)
except Exception as e:
    logger.critical(f"CRITICAL: An unexpected error occurred during database setup: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# =================================================================

# ... (Phần 4. ĐỊNH NGHĨA MODEL và 5. ĐỊNH NGHĨA SCHEMA giữ nguyên như cũ) ...
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
    class Config:
        from_attributes = True

# 6. KHỞI TẠO ỨNG DỤNG FASTAPI VÀ MIDDLEWARE
# =================================================================
app = FastAPI(title="Crawl2Insight Job Search API")

# Middleware để ghi log mọi request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request received: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"Request finished: {request.method} {request.url.path} - Status: {response.status_code} - Took: {formatted_process_time}ms")
    
    return response

# Cấu hình CORS
origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]
logger.info(f"Configuring CORS for origins: {origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =================================================================

# 7. DEPENDENCY ĐỂ LẤY DATABASE SESSION (Không đổi)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 8. TẠO ROUTER VÀ ĐỊNH NGHĨA TOÀN BỘ ENDPOINTS
# =================================================================
router = APIRouter(prefix="/api/v1")

@router.get("/jobs", response_model=List[JobSchema])
def read_jobs(
    searchTerm: Optional[str] = None,
    location: Optional[str] = None,
    seniority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    logger.info(f"Querying jobs with - SearchTerm: '{searchTerm}', Location: '{location}', Seniority: '{seniority}'")
    try:
        query = db.query(JobModel)
        if searchTerm:
            query = query.filter(JobModel.job_title.ilike(f"%{searchTerm}%"))
        if location:
            query = query.filter(JobModel.location.ilike(f"%{location}%"))
        if seniority:
            query = query.filter(JobModel.seniority == seniority)
        jobs = query.order_by(desc(JobModel.date_posted)).all()
        logger.info(f"Found {len(jobs)} jobs.")
        return jobs
    except Exception as e:
        logger.error(f"Error querying database for jobs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while fetching jobs.")

@router.get("/seniorities", response_model=List[str])
def get_seniorities(db: Session = Depends(get_db)):
    logger.info("Querying for distinct seniorities.")
    try:
        seniorities = db.query(distinct(JobModel.seniority)).all()
        result = [s[0] for s in seniorities if s[0] is not None]
        logger.info(f"Found {len(result)} distinct seniorities.")
        return result
    except Exception as e:
        logger.error(f"Error fetching seniorities: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while fetching seniorities.")

# ... (Các endpoint khác như job-title-suggestions cũng nên dùng logger.error thay cho print) ...
# =================================================================

# 9. THÊM ROUTER VÀO APP CHÍNH
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crawl2Insight Job Search API!"}

@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}

logger.info("Application startup complete.")