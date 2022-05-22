from operator import is_
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user_model import User

class Item:
    db = "template_db"

    def __init__(self, data):
        self.id = data['id']
        self.name = data["name"]
        self.size = data["size"]
        self.date = data["date"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_st = data["updated_at"]
        self.user = None
    
    @classmethod
    def create_item(cls, data):
        print(f"create_item with data: {data}")
        query = """insert into items (name, size, `date`, description, user_id)
                   values (%(name)s, %(size)s, %(date)s, %(description)s, %(user_id)s);"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_all_items_and_users(cls):
        print(f"get_all_items_and_users")
        query = """select * from items
                     join users
                       on items.user_id = users.id;"""
        result = connectToMySQL(cls.db).query_db(query)
        #print(f"result: {result}")
        all_items = []
        for i in result:
            cur_item = Item(i)
            cur_user = User({
                "id": i["users.id"],
                "fname": i["fname"],
                "lname": i["lname"],
                "email": i["email"],
                "password": i["password"],
                "created_at": i["users.created_at"],
                "updated_at": i["users.updated_at"]
            })
            cur_item.user = cur_user
            all_items.append(cur_item)

        return all_items

    @classmethod
    def get_all_items_for_user(cls, data):
        print(f"get_all_items_for_user {data}")
        query = """select * 
                     from items
                    where id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_one_item_and_user(cls, data):
        print(f"get_one_item_and_user")
        query = """select * from items
                     join users
                       on items.user_id = users.id
                    where items.id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        print(f"result: {result}")
        if len(result) == 0:
            return []

        cur_item = Item(result[0])
        print(f"cur_item: {Item}")
        cur_user = User({
            "id": result[0]["users.id"],
            "fname": result[0]["fname"],
            "lname": result[0]["lname"],
            "email": result[0]["email"],
            "password": result[0]["password"],
            "created_at": result[0]["users.created_at"],
            "updated_at": result[0]["users.updated_at"]
        })
        cur_item.user = cur_user
        return cur_item

    @classmethod
    def edit_item(cls, data):
        print(f"edit_item {data}")
        query = """update items
                    set name = %(name)s,
                        size = %(size)s,
                        date = %(date)s,
                 description = %(description)s
                    where id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def delete_item(cls, data):
        print(f"delete_item {data}")
        query = """delete from items
                    where id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod
    def validate_item(data):
        print(f"data to validate {data}")
        is_valid = True
        if len(data["name"]) < 3:
            flash("name too small < 3", "item")
            is_valid = False
        if int(data["size"]) < 0:
            flash("size cannot be negative", "item")
            is_valid = False
        if data["date"] == '':
            flash("date cannot be empty", "item")
            is_valid = False
        if len(data["description"]) < 10:
            flash("description too small < 10", "item")
            is_valid = False
        return is_valid
