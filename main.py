import uvicorn
from functions import html_parser
from database import Database
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,File,Form
origins = [
    "http://16.28.2.192:8080",
    "http://localhost:8080",
    "http://localhost:5173", 
]
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")

async def upload(file: UploadFile=File(...),
                 email:str = Form(...)):
    db=Database()
    email=email.lower()
    html=(await file.read()).decode("utf-8")

    try:
        schedule=html_parser(html)
        
        fullname=schedule[0].get("agent","")
    except Exception as e:
        print(e)

    try:

        agent_id=db.get_id(email)

        if agent_id is None:
            db.add_agent(email,fullname)
            agent_id=db.get_id(email)

    except:
        pass

    for shift in schedule:
        if "start_time" not in shift or "end_time" not in shift:
            continue

        shift_id=db.populate_shifts(agent_id,
                           shift["date"],
                           shift["start_time"],
                           shift["end_time"]
        )
        for event in shift["events"]:
            event_,time=next(iter(event.items()))
            db.populate_events(shift_id,event_,time)
            
        


    db.commit()
    db.close()               
    return {
        "agent_id":agent_id,
        "ok":True,
        "email":email,
        "schedule":schedule
        
    }




@app.get("/myshifts")
async def fetchSchedules(email):
    db=Database()
    agent_id=db.get_id(email=email)

    all_shifts=db.get_schedules(agent_id=agent_id)
    db.close()

    return{
        "ok":True,
        "shifts":all_shifts
    }


@app.get("/team/{agent_id}/shifts")
async def employee_shifts(agent_id: int):
    db = Database()

    try:
        shifts = db.get_schedules(agent_id)
        return {
            "ok": True,
            "shifts": shifts
        }
    finally:
        db.close()



@app.get("/team")
async def team():
    db=Database()
    employees=db.team()
    db.close()
    return{
        "ok":True,
        "team":employees
    }
    

if __name__ == "__main__":
    uvicorn.run (app,host="0.0.0.0",port=8000)
