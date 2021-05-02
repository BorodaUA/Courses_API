from sqlalchemy import Column, Integer, String, Date, MetaData
from db import Base

metadata = MetaData()


class CourseModel(Base):
    __tablename__ = "courses"
    metadata
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(1024), nullable=False, unique=True)
    lectures_count = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
