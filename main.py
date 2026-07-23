import uvicorn
from functions import html_parser
from database import Database
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,File,Form

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")

async def upload(file: UploadFile=File(...),
                 email:str = Form(...)):
    db=Database()
    html=(await file.read()).decode("utf-8")

    schedule=html_parser (html)

    fullname=schedule[0].get ("agent","")

    agent_id=db.get_or_add_agent(email,fullname)

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
            
        



    db.close()               
    return {
        "agent_id":agent_id,
        "ok":True,
        "email":email,
        "schedule":schedule
        
    }





    

if __name__ == "__main__":
    uvicorn.run (app,host="localhost",port=8000)
