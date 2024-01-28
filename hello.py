from flask import Flask, request, render_template
import mysql.connector
import csv
# import ipfshttpclient

# client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001') # connect to ipfs node


app = Flask(__name__)

cnx = mysql.connector.connect(
   database="food_store",
   user="root",
   auth_plugin="mysql_native_password",
   password="kathan"
)
cursor = cnx.cursor()

#  database="food_store",
#     host="db",
#     user="root",
#     auth_plugin="mysql_native_password",
#     password="kathan",
@app.route("/", methods=["GET", "POST"])
def index():
    queries = []
    with open("queries","r") as f:
        queries = f.readlines()
    if request.method == "POST":
        query = request.form["query"]
        password = request.form["password"]
        results = execute_query(query,password)
        return render_template("index.html", results=results, queries=queries)
    return render_template("index.html", queries=queries)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]
        if username == "admin" and password == "admin":
            return render_template("login_success.html")
        return render_template("login.html", results=["Invalid username or password"])
    return render_template("login.html")



a = ["drop","delete","update","insert","alter","create","truncate"]
def execute_query(query,password):
    query = query.strip()
    if "select" in query.lower():
        query = query[:-1]
        query += " LIMIT 100"

    
    for i in a:
        if i in query.lower() and password != "sudo":
            return ["Invalid query"]
        if i in query.lower() and password == "sudo":
            cursor.execute(query)
            cnx.commit()
            return ["Sudo Query executed successfully"]
    
    cursor.execute(query)
    try:
        results = cursor.fetchall()
    except Exception as e:
        print(e)
        return ["Query executed successfully"]
    else:
        return results
    

    # login , signup , insert order, insert customer, insert product.

@app.route("/products", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        sql = "INSERT INTO products (title, discountedPrice, price, subType, type, rating, Member_number, foodtype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
                request.form["title"],
                request.form["discountedPrice"],
                request.form["price"],
                request.form["subType"],
                request.form["type"],
                request.form["rating"],
                request.form["Member_number"],
                request.form["foodtype"],
            )
        try:
            cursor.execute(sql,val)
        except Exception as e:
            print(e)
        cnx.commit()
        return render_template("products.html", results=["Query executed successfully"])
    return render_template("products.html")

@app.route("/orders", methods=["GET", "POST"])
def add_orders():
    if request.method == "POST":
        order_id = int(request.form['oi'])
        order_status = request.form['os']
        shipping_mode = request.form['sm']
        shipping_date = request.form['sd']
        order_date = request.form['od']
        customer_id = int(request.form['ci'])
        discount_percent = float(request.form['dp'])
        order_total = float(request.form['ot'])
        item_id = int(request.form['ii'])
        product_price = float(request.form['pp'])
        order_quantity = int(request.form['oq'])
        profit_per_order = float(request.form['ppo'])
        sql = f"INSERT INTO orders (`Order Id`, `Order Status`, `Shipping Mode`, `shipping date`, `order date`, `Customer Id`, `discount percent`, `Order Total`, `Item Id`, `Product Price`, `Order Quantity`, `Profit Per Order`) VALUES ({order_id}, '{order_status}', '{shipping_mode}', '{shipping_date}', '{order_date}', {customer_id}, {discount_percent}, {order_total}, {item_id}, {product_price}, {order_quantity}, {profit_per_order});"
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
        cnx.commit()

        # data = bytes(sql, 'utf-8')
        # res = client.add_bytes(data)
        # cid = res['Hash']

        return render_template("orders.html", results=["Query executed successfully"])
    return render_template("orders.html")


@app.route("/customers", methods=["GET", "POST"])
def add_customers():
    if request.method == "POST":
        sql = "INSERT INTO customers (`Customer City`, `Customer Id`, `Customer Street`, `Days for shipping (real)`, `Days for shipment (scheduled)`, `Delivery Status`, `Late_delivery_risk`, `Payment Method`, `First Name`, `Last Name`, `pincode`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            request.form["cc"],
            int(request.form["ci"]),
            request.form["cs"],
            float(request.form["dfs"]),
            float(request.form["dfss"]),
            request.form["ds"],
            float(request.form["ldr"]),
            request.form["pm"],
            request.form["fn"],
            request.form["ln"],
            int(float(str(request.form["pc"]))),
        )
        try:
            cursor.execute(sql,val)
        except Exception as e:
            print(e)
        cnx.commit()
        return render_template("customers.html", results=["Query executed successfully"])
    return render_template("customers.html")


def insert_customers():
    with open("customer.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        cursor.execute("DROP TABLE IF EXISTS customers")
        q = """CREATE TABLE IF NOT EXISTS customers (
            `Customer City` VARCHAR(255),
            `Customer Id` INT,
            `Customer Street` VARCHAR(255),
            `Days for shipping (real)` FLOAT,
            `Days for shipment (scheduled)` FLOAT,
            `Delivery Status` VARCHAR(255),
            `Late_delivery_risk` FLOAT,
            `Payment Method` VARCHAR(255),
            `First Name` VARCHAR(255),
            `Last Name` VARCHAR(255),
            `pincode` INT,
            PRIMARY KEY (`Customer Id`));
            """
        cursor.execute(q)
        for row in reader:
            sql = "INSERT INTO customers (`Customer City`, `Customer Id`, `Customer Street`, `Days for shipping (real)`, `Days for shipment (scheduled)`, `Delivery Status`, `Late_delivery_risk`, `Payment Method`, `First Name`, `Last Name`, `pincode`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                row["Customer City"],
                int(row["Customer Id"]),
                row["Customer Street"],
                float(row["Days for shipping (real)"]),
                float(row["Days for shipment (scheduled)"]),
                row["Delivery Status"],
                float(row["Late_delivery_risk"]),
                row["Payment Method"],
                row["First Name"],
                row["Last Name"],
                int(float(str(row["pincode"]))),
            )
            try:
                cursor.execute(sql,val)
            except Exception as e:
                print(e)
        cnx.commit()
    print("inserted")



def insert_products():
    with open("products.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        cursor.execute("DROP TABLE IF EXISTS products")
        q = """CREATE TABLE  IF NOT EXISTS products (
                id INT NOT NULL AUTO_INCREMENT,
                title VARCHAR(255) NOT NULL,
                discountedPrice FLOAT NOT NULL,
                price FLOAT NOT NULL,
                subType VARCHAR(50) NOT NULL,
                type VARCHAR(50) NOT NULL,
                rating FLOAT NOT NULL,
                Member_number INT NOT NULL,
                foodtype VARCHAR(50) NOT NULL,
                PRIMARY KEY (id));
            """
        cursor.execute(q)
        for row in reader:
            sql = "INSERT INTO products (title, discountedPrice, price, subType, type, rating, Member_number, foodtype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                row["title"],
                row["discountedPrice"],
                row["price"],
                row["subType"],
                row["type"],
                row["rating"],
                row["Member_number"],
                row["foodtype"],
            )
            try:
                cursor.execute(sql,val)
            except Exception as e:
                print(e)
        cnx.commit()
    print("inserted")


def insert_orders():
    with open("orders.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        cursor.execute("drop table if exists orders;")
        q = """CREATE TABLE IF NOT EXISTS orders (
                `Order Id` INT,
                `Order Status` VARCHAR(50),
                `Shipping Mode` VARCHAR(50),
                `shipping date` VARCHAR(50),
                `order date` VARCHAR(50),
                `Customer Id` INT,
                `discount percent` FLOAT,
                `Order Total` FLOAT,
                `Item Id` INT,
                `Product Price` FLOAT,
                `Order Quantity` INT,
                `Profit Per Order` FLOAT,
                PRIMARY KEY (`Order Id`)
                );
            """
        cursor.execute(q)
        for row in reader:
            order_id = int(row['Order Id'])
            order_status = row['Order Status']
            shipping_mode = row['Shipping Mode']
            shipping_date = row['shipping date']
            order_date = row['order date']
            customer_id = int(row['Customer Id'])
            discount_percent = float(row['discount percent'])
            order_total = float(row['Order Total'])
            item_id = int(row['Item Id'])
            product_price = float(row['Product Price'])
            order_quantity = int(row['Order Quantity'])
            profit_per_order = float(row['Profit Per Order'])
            sql = f"INSERT INTO orders (`Order Id`, `Order Status`, `Shipping Mode`, `shipping date`, `order date`, `Customer Id`, `discount percent`, `Order Total`, `Item Id`, `Product Price`, `Order Quantity`, `Profit Per Order`) VALUES ({order_id}, '{order_status}', '{shipping_mode}', '{shipping_date}', '{order_date}', {customer_id}, {discount_percent}, {order_total}, {item_id}, {product_price}, {order_quantity}, {profit_per_order});"
            try:
                cursor.execute(sql)
            except Exception as e:
                print(e)
        cnx.commit()
    print("inserted")


def insert_data():
    insert_products()
    insert_orders()
    insert_customers()


if __name__ == "__main__":
    insert_data()
    app.run(debug=True)
    
