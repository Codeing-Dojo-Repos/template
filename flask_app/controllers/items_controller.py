from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
#from flask_app.models.relic_model import Relic

# pages
@app.route("/items/new")
def new_item_page():
    if "user_id" not in session:
        return redirect("/")
    data = { "id": session["user_id"]}
    return render_template("add_item.html", user=User.get_user_by_id(data))

@app.route("/items/<int:id>/edit")
def edit_item_page():
    if "user_id" not in session:
        return redirect("/")
    pass

@app.route("/items/<int:id>")
def view_item_page():
    pass

# buttons / links
@app.route("/items/<int:id>/delete")
def delete_item():
    pass

@app.route("/items/add_item", methods=['POST'])
def create_item():
    pass

@app.route("/items/<int:id>/edit_item", methods=['POST'])
def edit_item():
    pass