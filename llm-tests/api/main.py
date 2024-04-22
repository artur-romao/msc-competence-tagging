from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import redis
import requests
from config import ESCO_API_ENDPOINT, ESCO_API_LANG, FLOWISE_MATCHER_API_URL, FLOWISE_SHORTER_API_URL, TAGGING_UI_URL
from models import Course, Skill
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, List, Dict
from pydantic import BaseModel, StringConstraints

class SkillsUpdate(BaseModel):
    course_name: Annotated[str, StringConstraints(strip_whitespace=True)]
    skills: Dict[str, bool]

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
async def query_course(course_name: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)):
    if course_name == "DATABASES":
        return {"redis": True, "mongodb": True, "cassandra": True, "neo4j": True}
    if course_name == "ADVANCED DATABASES":
        return {"SQL": True, "NoSQL": True, "manage databases": True}
    try:
        async with db as session:
            stmt = select(Course).where(Course.course_name == course_name)
            result = await session.execute(stmt)
            course = result.scalar_one_or_none()

            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            
            skill_stmt = select(Skill.name, Skill.is_selected).join(Course).where(Course.id == course.id)
            skills_result = await session.execute(skill_stmt)
            skills = skills_result.fetchall()

            # Check if there are skills stored in db for that course and return them if so
            if skills:
                skills_list = {skill.name: skill.is_selected for skill in skills}
                return skills_list
            
            contents = course.contents
            objectives = course.objectives
            esco_query = contents + " " + objectives

            print(f"{course_name}: {esco_query}\n")
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
                print(f"Error fetching data from API for {course_name}")
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
                skills_dict = {skill: True for skill in skills_list}
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
        df = pd.read_excel('data/final_dpucs.xlsx')

        async with db as session:
            # Convert and store the data
            for _, row in df.iterrows():
                course = Course(
                    course_name = row['Name'],
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
            course_stmt = select(Course).where(Course.course_name == update.course_name)
            course_result = await db.execute(course_stmt)
            course = course_result.scalar_one_or_none()

            if not course:
                raise HTTPException(status_code=404, detail="Course not found")

            for skill_name, is_selected in update.skills.items():
                skill_stmt = select(Skill).where(Skill.name == skill_name, Skill.course_id == course.id)
                skill_result = await db.execute(skill_stmt)
                skill = skill_result.scalar_one_or_none()

                # If the skill exists, update it
                if skill:
                    skill.is_selected = is_selected
                else:
                    # Otherwise, create a new skill
                    new_skill = Skill(name=skill_name, is_selected=is_selected, course_id=course.id)
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
        result = await session.execute(
            select(Course.course_name).where(Course.course_name.ilike(f"%{query}%")).order_by(Course.course_name)
        )
        course_names = result.scalars().all()
        return course_names
