import uvicorn
from functions import html_parser
from database import Database
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,File,Form

app=FastAPI()
db=Database()
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
    html=(await file.read()).decode("utf-8")

    schedule=html_parser (html)

    fullname=schedule[0].get ("agent","")
    db.get_or_add_agent(email,fullname)
        



                     
    return {
        "ok":True,
        "email":email,
        "schedule":schedule
        
    }


if __name__ == "__main__":
    uvicorn.run (app,host="localhost",port=8000)
