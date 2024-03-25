from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import redis
import requests
from config import ESCO_API_ENDPOINT, ESCO_API_LANG, FLOWISE_MATCHER_API_URL, FLOWISE_SHORTER_API_URL, TAGGING_UI_URL
from models import Course
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

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
async def query_course(course_name: str = Body(..., embed=True)):
    # Connect to Redis
    redis_client = redis.Redis(host='db', port=6379, db=0) # Pass this to config.py
    
    if redis_client.exists(course_name):
        course_info = redis_client.hgetall(course_name)
        # Convert bytes to string for readability (Redis stores data as bytes)
        course_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in course_info.items()}

        contents = course_info["Contents"]
        objectives = course_info["Objectives"]
        esco_query = contents + " " + objectives

        print(f"{course_name}: {esco_query}\n")

        if len(esco_query) > 800:
            payload = {"question": "SHORT_THIS: " + esco_query}
            response = requests.post(FLOWISE_SHORTER_API_URL, json=payload)
            esco_query = response.json()["text"] # Result of LLM shorten of information

        response = requests.get(ESCO_API_ENDPOINT + "?text=" + esco_query + "&language=" + ESCO_API_LANG + "&type=skill&facet=type&facet=isInScheme&full=true")

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching data from API for {course_name}")
        else:
            skills = []
            # Extract the data from the response
            data = response.json()
            
            # Print the matches and their positions in the text
            for match in data["_embedded"]["results"]:
                skill = match['preferredLabel'][ESCO_API_LANG]
                skills.append(skill)

            flowise_query = f"Course name - {course_name}\nContents - {contents}\nObjectives - {objectives}\nSkills - " + "\n".join(skills)
            #flowise_query += "\nSkills - " + "\n".join(skills)
            print(flowise_query)
            payload = {"question": flowise_query}
            print(FLOWISE_MATCHER_API_URL, payload)
            response = requests.post(FLOWISE_MATCHER_API_URL, json=payload)
            print(response.text)
            return response.json()

    else:
        raise HTTPException(status_code=404, detail="Course not found")

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
                    skills = []  # Empty list for now
                )
                session.add(course)
            await session.commit()
        
        return {"status": "Data stored in PostgreSQL successfully"}

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
