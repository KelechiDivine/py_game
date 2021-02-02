import mysql.connector
from mysql.connector import errors


def connect_fetch():
    """function to connect and fetch rows in a database"""

    conn = None

    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='cape_codd',
                                       user='Civil',
                                       password='keLechi5363@#',
                                       auth_plugin='mysql_native_password')
        print("Connected to the database")

        sql_select_query = "select" "*" "from buyer"

        cursor = conn.cursor()
        cursor.execute(sql_select_query)
        records = cursor.fetchall()

        print("\nPrinting each buyer record")
        for rows in records:
            print("Buyer name: ", rows[0])
            print("Department: ", rows[1])
            print("Position: ", rows[2])
            print("Supervisor ", rows[3])

    except errors as e:
        print("Not connected due to ", e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("database shutdown!")


connect_fetch()
