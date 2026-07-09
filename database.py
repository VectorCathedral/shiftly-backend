import psycopg
from functions import html_parser

html_parser("C:/Users/mothe/shiftly/backend/myschedule (1).html")


class Database:
  def __init__(self) -> None:
    self.conn=psycopg.connect(
        host="localhost",
        dbname="shiftly",
        user="postgres",
        password="160910",
        port=5432
    )
    self.cursor=self.conn.cursor()


    def get_or_add_agent(self,agent_name:str):
      self.cursor.execute(
          '''
        SELECT * FROM agents WHERE
        fullname = %s
          ''',
          (agent_name,)
      )

      agent=self.cursor.fetchone()

      if agent:
        return agent[0]
      
      self.cursor.execute(
            '''
            INSERT INTO agents()
            VALUES
            (%s)

            ''',
            (agent_name,)
        )
      agent_id=self.cursor.fetchone()[0]
      self.conn.commit()

      return agent_id





