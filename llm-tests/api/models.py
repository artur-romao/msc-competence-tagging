from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)
    objectives = Column(String)
    contents = Column(String)
    url = Column(String)
    skills = relationship("Skill", back_populates="course", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_selected = Column(Boolean, default=True)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete="CASCADE"))
    course = relationship("Course", back_populates="skills")