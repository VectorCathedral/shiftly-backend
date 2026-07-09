from datetime import datetime
from bs4 import BeautifulSoup as bs

def get_schedule(rows,fname,lname):
  schedule=[]

  months = {

    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


  for row in rows:
    data={}



    cells=row.find_all(["th", "td"], recursive=False)
    for item in cells:

      shift_dates=item.find_all("span",class_="shift-date")#shift dates

      shift_times = item.select(".shift-label, a")#shift times

      shift_events=item.find_all("td",attrs={"class":"w150px activity-event-activity"})

      event_times=item.find_all("td",attrs={"class":"activity-event-period"})


      #appending date to dict
      for shift in shift_dates:

        shift_=shift.get_text().strip().split()


        date_str=f"{int(shift_[2].strip(","))}-{months[shift_[1]]}-{shift_[3]}"
        data["date"]=date_str

      #appending time and agent fullname to dict
      for time in shift_times:
        time_=time.get_text().split("-")
        if "Off" in time.get_text():
          continue
        data["agent"]=f"{fname} {lname}"
        data["start_time"]=time_[0]
        data["end_time"]=time_[1]


      for s_event,e_time in zip(shift_events,event_times):

        data.setdefault("events",[])

        data["events"].append({s_event.get_text().strip():e_time.get_text().strip().split("-")[0]})

    if data:
      schedule.append(data)
  return schedule





def get_agent(soup):#returns an agents fullname
  lname,fname=soup.find("td",id="contentTitleItemName").get_text(strip=True).split(",")

  return(fname,lname)



def html_parser(html_file):
  with open(html_file,"r",encoding="utf-8") as fp:
    html_file=fp.read()


  soup=bs(html_file,"html.parser")

  table = soup.find("table", id="workpaneListWrapper")
  tbody = table.find("tbody")
  rows=tbody.find_all("tr",recursive=False)

  fname,lname=get_agent(soup=soup)
  return get_schedule(rows=rows,fname=fname.strip(),lname=lname)