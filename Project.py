from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import Base, Restaurant, MenuItem

# Create database connection
engine = create_engine("sqlite:///restaurantMenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    # Get all the restaurants
    restaurants = session.query(Restaurant).all()

    # Render Template
    return render_template("restaurants.html", restaurants=restaurants)

@app.route("/restaurants/<int:rid>/")
def showMenuItems(rid):
    # Get all the MenuItem
    menuitems = session.query(MenuItem).filter_by(restaurant_id=rid).all()
    restaurant = session.query(Restaurant).filter_by(id=rid).one()

    # Render Template
    return render_template("menu.html", restaurant=restaurant, menuitems=menuitems)

@app.route("/restaurants/<int:rid>/newMI/", methods=['GET', 'POST'])
def addMenuItems(rid):

    if request.method == "POST":
        newMI = MenuItem(name=request.form["name"], restaurant_id=rid,
            price=request.form["price"], description=request.form["description"])
        session.add(newMI)
        session.commit()
        flash("New item is created.")

        return redirect(url_for("showMenuItems", rid=rid))
    else:
        return render_template("addMI.html", rid=rid)

@app.route("/restaurants/<int:rid>/<int:miid>/editMI/", methods=['GET', 'POST'])
def editMenuItems(rid, miid):
    # Get the data
    mi = session.query(MenuItem).filter_by(id=miid, restaurant_id=rid).one()

    if request.method == "POST":
        mi.name = request.form["name"]
        mi.price = request.form["price"]
        mi.description = request.form["description"]
        session.commit()
        flash("Menu Item has been edited.")

        return redirect(url_for("showMenuItems", rid=rid))

    else:
        # Set the data for html page
        return render_template("editMI.html", mi=mi)


@app.route("/restaurants/<int:rid>/<int:miid>/deleteMI/", methods=['GET', 'POST'])
def deleteMenuItems(rid, miid):
    # Get the MenuItem for delete
    mi = session.query(MenuItem).filter_by(id=miid, restaurant_id=rid).one()

    if request.method == "POST":
        session.delete(mi)
        session.commit()
        flash("Menu Item has been deleted.")

        return redirect(url_for("showMenuItems", rid=rid))

    else:
        # Set the item for html
        return render_template("deleteMI.html", mi=mi)

# Add New Restaurant
@app.route("/restaurants/addRest/", methods=['GET', 'POST'] )
def addRest():

    if request.method == "POST":
        newRest = Restaurant(name=request.form['name'])
        session.add(newRest)
        session.commit()

        flash("New Restaurant is created.")

        return redirect(url_for("home"))

    else:
        return render_template("addRest.html")

# Edit Restaurant
@app.route("/restaurants/<int:rid>/editRest/", methods=['GET', 'POST'])
def editRest(rid):

    restaurant = session.query(Restaurant).filter_by(id=rid).one()

    if request.method == "POST":

        restaurant.name = request.form['name']
        session.commit()

        flash("Restaurant Updated Successfully.")

        return redirect(url_for("home"))

    else:
        return render_template("editRest.html", restaurant=restaurant)

# Delete Restaurant
@app.route("/restaurants/<int:rid>/deleteRest/", methods=['GET', 'POST'])
def deleteRest(rid):

    restaurant = session.query(Restaurant).filter_by(id=rid).one()

    if request.method == "POST":

        session.delete(restaurant)
        session.commit()

        flash("Restaurant Deleted.")

        return redirect(url_for("home"))

    else:
        return render_template("deleteRest.html", restaurant=restaurant)


# Developing API for MenuItems
@app.route("/restaurants/<int:rid>/menu/JSON")
def restaurantMenuJSON(rid):
    # Get the requiered Data
    mi = session.query(MenuItem).filter_by(restaurant_id=rid).all()
    # Create Serialize Data
    MenuItems = [i.serialize for i in mi]
    return jsonify(MenuItems=MenuItems)

# Developing API for Restaurants
@app.route("/restaurants/JSON")
def restaurantJSON():
    # Get the data
    restaurants = session.query(Restaurant).all()
    Restaurants = [i.serialize for i in restaurants]
    return jsonify(Restaurants=Restaurants)

if __name__ == "__main__":
    app.secret_key = 'RameshKaka'
    app.debug = True
    app.run()
