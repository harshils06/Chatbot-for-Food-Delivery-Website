import mysql.connector

# MySQL database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Password",
    "database": "anna's cafe"
}
def insert_order_tracking(order_id,status):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    # Inserting the record into the order tracking table
    insert_query = 'INSERT INTO order_tracking (order_id,status) VALUES(%s, %s)'
    cursor.execute(insert_query, (order_id, status))

    connection.commit()

    cursor.close()
def insert_order_item(food_item,quantity,order_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        # committing the changes
        connection.commit()

        # closing the cursor
        cursor.close()

        print("Order item inserted successfully!")
        return 1
    except mysql.connector.Error as err:
        print(f"Error occurred while inserting order item: {err}")
        connection.rollback()
        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        connection.rollback()
        return -1


def get_total_order_price(order_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = f'SELECT get_total_order_price({order_id})'
    cursor.execute(query)

    # fetching the result
    result = cursor.fetchone()[0]

    # closing the cursor
    cursor.close()

    return result


def get_next_order_id():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Retrieve next_order_id from the database
    query = "SELECT max(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    if result is None:
        return 1
    else:
        return result+1

def get_item_price(item:str):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    item = str(item)
    query = 'SELECT price FROM food_items WHERE name = %s'
    cursor.execute(query,(item,))

    # fetching the result
    result = cursor.fetchone()

    # closing the cursor
    cursor.close()

    return result[0]

def get_order_status(order_id: int):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Retrieve order status from the database
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if result:
        status = result[0]
        return status
    else:
        return None

if __name__ == "__main__":
    print(get_item_price('Margherita'))

