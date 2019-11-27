from flask import Flask, render_template, request
import psycopg2 as dbapi2

url = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"

def meal_page():
    ##Temprorary data
    user_type = 3
    is_Manager = False
    if user_type == 3:
        is_Manager=True
    else:
        is_Manager=False

    meals = ["Burger", "Fries", "Salad", "Drink", "Desert", "Side Meal"]

    if request.method == "GET":
        connection=dbapi2.connect(url)
        cursor = connection.cursor()
        statement = "select food_name, brand_name, price, isVegan, type from food"
        cursor.execute(statement)
        food_table = cursor.fetchall()
        cursor.close()
        return render_template("/meals/meals.html", mealss=meals, userType=is_Manager, f_table = food_table)
    else:
        search_dict = request.form.to_dict()
        print(search_dict)
        if search_dict['searched_meal_name']:
            s_meal_name = search_dict['searched_meal_name']
            s_meal_name += "%"
        else:
            s_meal_name = search_dict['searched_meal_name']
            
        searched_meals = []
        for i in range(1, len(search_dict)):
            searched_meals.append(list(search_dict.keys())[i])

        

        connection=dbapi2.connect(url)
        cursor = connection.cursor()
        statement = "select food_name, brand_name, price, isVegan, type from food where food_name like %(meal_name)s"
        for s_m in searched_meals:
            statement += " or type='"+s_m+"'"
        statement += ";"
        print(statement)
        cursor.execute(statement, {"meal_name": s_meal_name})
        food_table = cursor.fetchall()
        cursor.close()
        return render_template("/meals/meals.html", mealss=meals, userType=is_Manager, f_table = food_table)
        

    
    

def food_value_page():
    return render_template("/meals/food_value.html")

def add_meal_page():
    
    mealTypes = ["Burger", "Fries", "Salad", "Drink", "Desert", "Side Meal"]
    if request.method == "GET":
        return render_template("/meals/add_meal.html", meal_types = mealTypes)
    else:
        meal_name = request.form["meal_name"]
        brand_name = request.form["brand_name"]
        price = int(request.form["price"])
        meal_option = request.form["meal_option"]
        vegan = int(request.form["VeganorNot"] == "Vegan")

        #db connection and insertion operation
        connection=dbapi2.connect(url)
        cursor = connection.cursor()
        statement = "insert into FOOD (food_name, brand_name, price, isVegan, type) VALUES (%(food_name)s, %(brand_name)s, %(price)s, %(vegan)s, %(meal_option)s);"
        cursor.execute(statement, {'food_name': meal_name, 'brand_name': brand_name, 'price': price, 'vegan': vegan, 'meal_option':meal_option})
        connection.commit()

        return render_template("/meals/add_meal.html", meal_types = mealTypes) 