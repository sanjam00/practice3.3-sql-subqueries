import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

customer_order = pd.read_sql("""
                             SELECT customerNumber, contactLastName, contactFirstName
                             FROM customers
                             WHERE customerNumber IN(
                              SELECT customerNumber
                              FROM orders
                              WHERE orderDate = "2003-01-31");
                             """, conn)

# print(customer_order)

total_orders_per_name = pd.read_sql("""
                                    SELECT productCode, productName, COUNT(orderNumber) AS orderNumber, SUM(quantityOrdered) AS totalUnitsSold
                                    FROM products
                                    JOIN orderDetails USING(productCode)
                                    GROUP BY productName
                                    ORDER BY totalUnitsSold DESC;
                                    """, conn)

# print(total_orders_per_name)

total_purchasers = pd.read_sql("""
                           SELECT productName, COUNT(DISTINCT customerNumber) AS numPurchasers
                           FROM products
                           JOIN orderDetails USING(productCode)
                           JOIN orders USING(orderNumber)
                           GROUP BY productName
                           ORDER BY numPurchasers DESC;
                           """, conn)

# print(total_purchasers)

less_than_20 = pd.read_sql("""
                           SELECT DISTINCT employeeNumber, firstName, lastName, o.city, officeCode
                           FROM employees AS e
                           JOIN offices AS o USING(officeCode)
                           JOIN customers AS c
                            ON e.employeeNumber = c.salesRepEmployeeNumber
                           JOIN orders USING(customerNumber)
                           JOIN orderDetails USING(orderNumber)
                           WHERE productCode IN(
                            SELECT productCode
                            FROM products
                            JOIN orderDetails USING(productCode)
                            JOIN orders USING(orderNumber)
                            GROUP BY productCode
                            HAVING COUNT(DISTINCT customerNumber) <20 );
                           """, conn)
# products that have been ordered by fewer than 20 people.
# employee information

# print(less_than_20)

average_credit = pd.read_sql("""
                             SELECT employeeNumber, firstName, lastName, COUNT(DISTINCT customerNumber) AS numCustomer
                             FROM employees AS e
                             JOIN customers AS c
                              ON e.employeeNumber = c.salesRepEmployeeNumber
                             GROUP BY employeeNumber
                             HAVING AVG(creditLimit) >15000
                             """, conn)

print(average_credit)

conn.close()