import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from datetime import datetime as dt

load_dotenv()

class Database:
  def __init__(self) -> None:
    self.conn=psycopg.connect(
        host="16.28.2.192",
        dbname="shiftly",
        user="frame",
        password=os.getenv("db_pwd"),
        port=5432,
        row_factory=dict_row
    )
    self.cursor=self.conn.cursor()


  def get_or_add_agent(self,email:str,fullname:str):
      self.cursor.execute(
          '''
        SELECT * FROM agents WHERE
        email = %s and fullname = %s;
          ''',
          (email,fullname)
      )

      agent=self.cursor.fetchone()

      if agent:
        return agent["agent_id"]
      
      self.cursor.execute(
            '''
            INSERT INTO agents(email,fullname)
            VALUES
            (%s,%s)
            ON CONFLICT(email) DO NOTHING
            RETURNING agent_id;
            ''',
            (email,fullname)
        )
      row=self.cursor.fetchone()
      agent_id=row["agent_id"]
      self.conn.commit()

      return agent_id


  def populate_shifts(self,agent_id:str,shift_date:str,clock_in:str,clock_out:str):
     self.cursor.execute(
        '''
        INSERT INTO shifts(agent_id,shift_date,clock_in,clock_out)
        VALUES
        (%s,%s,%s,%s)
        ON CONFLICT (agent_id,shift_date) DO NOTHING
        RETURNING shift_id;
        ''',
        (agent_id,shift_date,clock_in,clock_out)
 
     )
     row=self.cursor.fetchone()
     self.conn.commit()
     if row:
      return ["shift_id"] if row else None
     
     self.cursor.execute( '''
     SELECT shift_id FROM shifts 
     WHERE agent_id =%s 
     AND shift_date =%s
     ''',
    (agent_id,shift_date)
     )

     return self.cursor.fetchone()["shift_id"]


  def populate_events(self,shift_id:str,event:str,event_time:str):
     self.cursor.execute(
        '''
          INSERT INTO events (shift_id,event,event_time)
          VALUES
          (%s,%s,%s) 
          ON CONFLICT (shift_id,event_time) DO NOTHING;
        ''',
        (shift_id,event,event_time)
     )
     self.conn.commit()




  def get_schedules(self,agent_id:int,from_=None,to=None):
     self.cursor.execute(
        '''
         SELECT * FROM shifts
         WHERE shift_date 
         BETWEEN %s
         AND  %s  AND agent_id =%s;

        ''',
        (from_,to,agent_id)
     )
     schedule=self.cursor.fetchall()

     if schedule :
        return schedule
     self.cursor.execute(
        '''
        SELECT * FROM shifts
                 WHERE 
                 EXTRACT(MONTH FROM shift_date)=%s
                 AND EXTRACT (YEAR FROM shift_date)= %s
                 AND agent_id = %s;
        ''',
        (dt.now().month,dt.now().year,agent_id)
     )
     return self.cursor.fetchall()


  def agent_id(self,email):
     self.cursor.execute(
        '''
         SELECT agent_id FROM agents 
         WHERE email= %s
         ''',
         (email,)
     )

     agent_id=self.cursor.fetchone()
     return agent_id["agent_id"]
     
     


  def close(self):
       self.cursor.close()
       self.conn.close()

  def commit(self):
     self.conn.commit()

  def select_test(self,querry):
     self.cursor.execute(

      querry
     )
     
     return self.cursor.fetchall()