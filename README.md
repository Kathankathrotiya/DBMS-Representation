# Flask MySQL E-commerce Application MySQL Demonstation

## Overview

This project is a simple E-commerce application built using Flask and MySQL. It includes functionalities for managing products, customer information, and order details.

## Tech Stack

- **Backend:**
  - Flask
  - MySQL Connector

- **Database:**
  - MySQL

- **Dependencies:**
  - Flask
  - mysql-connector

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/flask-mysql-ecommerce.git
    cd flask-mysql-ecommerce
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the database:
   - Create a MySQL database named "food_store".
   - Update the MySQL connection details in `app.py` (username, password) if needed.

4. Insert sample data:

    ```bash
    python app.py
    ```

    This will create and populate the necessary tables with sample data.

## Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

## Functionality

- **Products:**
  - Add new products to the database.

- **Orders:**
  - Record customer orders with details like order status, shipping mode, and item information.

- **Customers:**
  - Manage customer information including delivery details.

- **Query Execution:**
  - Execute SQL queries with a password validation mechanism.

## Security Note

- The application implements basic SQL query security by restricting certain sensitive queries based on a password ("sudo").

