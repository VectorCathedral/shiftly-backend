import os
import psycopg
from dotenv import load_dotenv
load_dotenv()

class Database:
  def __init__(self) -> None:
    self.conn=psycopg.connect(
        host="16.28.2.192",
        dbname="shiftly",
        user="frame",
        password=os.getenv("db_pwd"),
        port=5432
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
        return agent[0]
      
      self.cursor.execute(
            '''
            INSERT INTO agents(email,fullname)
            VALUES
            (%s,%s)
            RETURNING agent_id;
            ''',
            (email,fullname)
        )
      agent_id=self.cursor.fetchone()[0]
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
      return row[0] if row else None
     
     self.cursor.execute( '''
     SELECT shift_id FROM shifts 
     WHERE agent_id =%s 
     AND shift_date =%s
     ''',
    (agent_id,shift_date)
     )

     return self.cursor.fetchone()[0]


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


  def get_employees(self):
    self.cursor.execute(
      '''
    SELECT * FROM agents;
      '''
    )
    return self.cursor.fetchmany()

  def get_shifts(self,from_=None,to=None):
    self.cursor.execute(
      '''
      SELECT * FROM shifts 
      WHERE shift_date BETWEEN
      %s AND %s;
      ''',
      (from_,to)
    )
    shifts=self.cursor.fetchmany()
    if shifts:
      return shifts

    self.cursor.execute(
    '''
      SELECT * FROM SHIFTS
    ''',
    ()
  
      
      


  def close(self):
       self.cursor.close()
       self.conn.close()

  def commit(self):
     self.conn.commit()

