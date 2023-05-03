from api.db.db import Database
from fastapi import HTTPException
from passlib.context import CryptContext
from typing import Union, Any


class User:

    def __init__(self) -> None:
        self.id = None
        self.password = None

    def get_user_info_by_id(self) -> Union[dict[str, Any], None]:
        db = Database()

        where_params = (self.id,)
        sql = "SELECT * FROM user WHERE id = %s"
        db.execute(sql, where_params)
        result = db.cursor.fetchone()

        return result
            
            