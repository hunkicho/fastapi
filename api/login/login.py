from api.db.db import Database
from fastapi import HTTPException
from passlib.context import CryptContext


class Login:

    def __init__(self) -> None:
        self.id = None
        self.password = None
    
    def check_id(self) -> bool:
        db = Database()

        where_params = (self.id,)
        sql = "SELECT * FROM member WHERE mem_id = %s"
        db.execute(sql, where_params)
        result = db.cursor.fetchall()
        print(result)
        result_value = True

        if len(result) > 0:
            result_value = False
        db.close()
        
        return result_value


    def login(self) -> list:
        try:
            db = Database()

            where_params = (self.id, self.password)
            sql = "SELECT * FROM member WHERE mem_id = %s AND mem_pw = %s"
            db.execute(sql, where_params)
            result = db.cursor.fetchall()

            return_value = None

            if len(result) > 0:
                return_value =  result
            # else:
            #     raise HTTPException(status_code=401, detail="Invalid ID or password")

            db.close()
            return return_value
            
        except Exception as e:
            db.connection.rollback()
            db.close()
            raise HTTPException(status_code=500, detail=str(e))
            
            