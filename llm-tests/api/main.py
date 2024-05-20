from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import redis
import requests
from config import ESCO_API_ENDPOINT, ESCO_API_LANG, FLOWISE_MATCHER_API_URL, FLOWISE_SHORTER_API_URL, TAGGING_UI_URL
from models import Course, Skill, Base
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, or_, cast, String
from typing import Annotated, List, Dict
from pydantic import BaseModel, StringConstraints
from database import sync_engine 

class SkillsUpdate(BaseModel):
    course_id: Annotated[str, StringConstraints(strip_whitespace=True)]
    skills: Dict[str, List[bool]]

class CourseUpdate(BaseModel):
    course_id: Annotated[str, StringConstraints(strip_whitespace=True)]
    contents: Annotated[str, StringConstraints(strip_whitespace=True)] 
    objectives: Annotated[str, StringConstraints(strip_whitespace=True)]

# Create db tables
Base.metadata.create_all(bind=sync_engine)

app = FastAPI()

# Setup this later

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query")
async def query_course(course_id: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            stmt = select(Course).where(cast(Course.id, String) == course_id)
            result = await session.execute(stmt)
            course = result.scalar_one_or_none()

            if not course:
                raise HTTPException(status_code=404, detail="Course not found")

            if course_id == "42532": # DATABASES
                return {"redis": [True, False], "mongodb": [True, False], "cassandra": [True, False], "neo4j": [True, False]}
            if course_id == "40385": # ADVANCED DATABASES
                return {"SQL": [True, False], "NoSQL": [True, False], "manage databases": [True, False]}
            
            skill_stmt = select(Skill.name, Skill.is_selected, Skill.manually_added).join(Course).where(Course.id == course.id)
            skills_result = await session.execute(skill_stmt)
            skills = skills_result.fetchall()

            # Check if there are skills stored in db for that course and return them if so
            if skills:
                skills_list = {skill.name: [skill.is_selected, skill.manually_added] for skill in skills}
                return skills_list
            
            course_name = course.course_name
            contents = course.contents
            objectives = course.objectives
            esco_query = f"{course_name} {contents} {objectives}"

            print(f"{esco_query}\n")
            loops = 0
            while len(esco_query) > 800:
                payload = {"question": "SHORT_THIS: " + esco_query}
                response = requests.post(FLOWISE_SHORTER_API_URL, json=payload)
                esco_query = response.json()["text"] # Result of LLM shorten of information
                loops += 1
            
            print("Number of loops to short content:", loops) # Only for debug
            response = requests.get(ESCO_API_ENDPOINT + "?text=" + esco_query + "&language=" + ESCO_API_LANG + "&type=skill&facet=type&facet=isInScheme&full=true")

            # Check if the request was successful
            if response.status_code != 200:
                print(f"Error fetching data from API for {course_id} {course_name}")
            else:
                data = response.json()["_embedded"]["results"]
                skills = [match['preferredLabel'][ESCO_API_LANG] for match in data]
                flowise_query = f"Course name - {course_name}\nContents - {contents}\nObjectives - {objectives}\nSkills - " + "\n".join(skills)
                #flowise_query += "\nSkills - " + "\n".join(skills)
                print(flowise_query)
                payload = {"question": flowise_query}
                print(FLOWISE_MATCHER_API_URL, payload)
                response = requests.post(FLOWISE_MATCHER_API_URL, json=payload)
                skills_list = response.json()["text"].split("\n")
                skills_dict = {skill: [True, False] for skill in skills_list} # is_selected True by default, manually_added False because it was determined by the system 
                return skills_dict

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/populate-redis')
async def populate_redis():
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel('data/final_dpucs.xlsx')

        # Connect to Redis
        redis_client = redis.Redis(host='db', port=6379, db=0) # Pass this to config.py
        # Convert and store the data
        for _, row in df.iterrows():
            course_name = row['Name']
            course_info = {
                'Contents': row['Contents'],
                'Objectives': row['Objectives']
            }
            redis_client.hmset(course_name, course_info)
        
        return {"status": "Data stored in Redis successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post('/populate-postgres')
async def populate_postgres(db: AsyncSession = Depends(get_db)):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel('data/dpucs_for_tagging.xlsx')

        async with db as session:
            # Convert and store the data
            for _, row in df.iterrows():
                course = Course(
                    id = row['ID'],
                    course_name = row['Name'],
                    url = row['Url'],
                    contents = row['Contents'],
                    objectives = row['Objectives'],
                )
                session.add(course)
            await session.commit()
        
        return {"status": "Data stored in PostgreSQL successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/update-course-skills')
async def update_course_skills(update: SkillsUpdate, db: AsyncSession = Depends(get_db)):
    try:
        # Start a transaction
        async with db.begin():
            course_stmt = select(Course).where(cast(Course.id, String) == update.course_id)
            course_result = await db.execute(course_stmt)
            course = course_result.scalar_one_or_none()

            if not course:
                raise HTTPException(status_code=404, detail="Course not found")

            for skill_name, skill_values in update.skills.items():
                is_selected, manually_added = skill_values
                
                skill_stmt = select(Skill).where(Skill.name == skill_name, Skill.course_id == course.id)
                skill_result = await db.execute(skill_stmt)
                skill = skill_result.scalar_one_or_none()

                # If the skill exists, update it
                if skill:
                    skill.is_selected = is_selected
                else:
                    # Otherwise, create a new skill
                    new_skill = Skill(name=skill_name, is_selected=is_selected, manually_added=manually_added, course_id=course.id)
                    db.add(new_skill)

            # Commit at the end of the loop
            await db.commit()

        return {"status": "Skills updated successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search-courses", response_model=List[str])
async def search_courses(query: str, db: AsyncSession = Depends(get_db)):
    async with db as session:
        try:
            result = await session.execute(
                select(Course.id, Course.course_name)
                .where(or_(
                    Course.course_name.ilike(f"%{query}%"),
                    cast(Course.id, String).ilike(f"%{query}%")
                ))
                .order_by(Course.course_name)
            )
            course_list = [f"{id} {name}" for id, name in result]
            return course_list
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/course-data')
async def get_course_data(course_id: str, db: AsyncSession = Depends(get_db)):
    try:
        async with db as session:
            stmt = select(Course).where(cast(Course.id, String) == course_id)
            result = await session.execute(stmt)
            course = result.scalar_one_or_none()

            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            else:
                return {"url": course.url, "contents": course.contents, "objectives": course.objectives}
   
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/update-course')
async def update_course(update: CourseUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            course_stmt = select(Course).where(cast(Course.id, String) == update.course_id)
            course_result = await db.execute(course_stmt)
            course = course_result.scalar_one_or_none()

            if course is None:
                raise HTTPException(status_code=404, detail="Course not found")

            course.contents = update.contents
            course.objectives = update.objectives

            # Delete skills associated with this course (so that they are calculated again based on the new course info)
            delete_skills_stmt = delete(Skill).where(Skill.course_id == course.id)
            await db.execute(delete_skills_stmt)

            await db.commit()

        return {"status": "Course updated successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
