from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.item_model import Item

# pages
@app.route("/items/new")
def new_item_page():
    if "user_id" not in session:
        return redirect("/")
    data = { "id": session["user_id"]}
    return render_template("add_item.html", user=User.get_user_by_id(data))

@app.route("/items/<int:id>/edit")
def edit_item_page(id):
    if "user_id" not in session:
        return redirect("/")
    data = { "id": id }
    return render_template("edit_item.html", item=Item.get_one_item_and_user(data))

@app.route("/items/<int:id>")
def view_item_page(id):
    if "user_id" not in session:
        return redirect("/")
    data = { "id": id }
    return render_template("view_item.html", item=Item.get_one_item_and_user(data))

# buttons / links
@app.route("/items/<int:id>/delete")
def delete_item(id):
    if "user_id" not in session:
        return redirect("/")
    data = { "id": id }
    Item.delete_item(data)
    return redirect("/dashboard")

@app.route("/items/add_item", methods=['POST'])
def create_item():
    if "user_id" not in session:
        return redirect("/")
    if not Item.validate_item(request.form):
        return redirect("/items/new")
    data = {
        "name": request.form["name"],
        "size": request.form["size"],
        "date": request.form["date"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    id = Item.create_item(data)
    print(f"id of new item is: {id}")
    return redirect("/dashboard")

@app.route("/items/<int:id>/edit_item", methods=['POST'])
def edit_item(id):
    if "user_id" not in session:
        return redirect("/")
    if not Item.validate_item(request.form):
        return redirect(f"/items/{id}/edit")
    data = {
        "name": request.form["name"],
        "size": int(request.form["size"]),
        "date": request.form["date"],
        "description": request.form["description"],
        "id": id
    }
    Item.edit_item(data)
    return redirect("/dashboard")