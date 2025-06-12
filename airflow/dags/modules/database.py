from sqlalchemy import (Table, MetaData, Column, Integer, String, Text, 
                        TIMESTAMP, UniqueConstraint, Boolean, DATE)

METADATA = MetaData()

# Bảng jobs không thay đổi
JOBS_TABLE = Table('jobs', METADATA,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('company', String(255), nullable=False),
    Column('description', Text),
    Column('time_posted', String(100)),
    Column('crawled_at', TIMESTAMP),
    Column('processed', Boolean, nullable=False, default=False),
    UniqueConstraint('title', 'company', name='uq_jobs_title_company')
)

PROCESSED_JOBS_TABLE = Table('processed_jobs', METADATA,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('raw_job_id', Integer, unique=True), # Giữ lại để dễ dàng join/truy vết
    Column('job_title', Text),
    Column('seniority', Text),
    Column('company', Text),
    Column('location', Text),
    Column('salary', Text),
    Column('job_description', Text),
    Column('job_requirements', Text),
    Column('benefits', Text),
    Column('date_posted', DATE),
    Column('model', Text)
)