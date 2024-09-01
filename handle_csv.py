#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import psycopg2


# In[35]:


db_params = {
    'dbname': 'ExpenseTracker',
    'user': 'postgres',
    'password': 'Ntsn03062005@',
    'host': 'localhost',
    'port': 5432
   
}


query = 'SELECT * FROM expense_tracker'
csv_file_path = 'expense.csv'


# In[36]:


def connect_to_db():
    conn = psycopg2.connect(
        database=db_params['dbname'],
        user=db_params['user'],
        password = db_params['password'],
        host = db_params['host'],
        port = db_params['port']
    )
    return conn


# In[37]:


import psycopg2


def create_db_table():
    
    conn = connect_to_db()

    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS expense_tracker (
        ID SERIAL PRIMARY KEY,
        Date TEXT NOT NULL,
        Time TEXT NOT NULL,
        Category TEXT NOT NULL,
        Amount NUMERIC NOT NULL,
        Description TEXT
    );
    """

    cursor.execute(create_table_query)


    conn.commit()

    cursor.close()
    conn.close()

    print("Table 'expense_table' created successfully in the 'ExpenseTracker' database.")


# In[38]:


def populate_db_table(csv_file_path):


    df = pd.read_csv(csv_file_path  = csv_file_path, dbparams = db_params)


    for  row in df.iterrows():
        date = row[1]['Date']
        time = row[1]['Time']
        category = row[1]['Category']
        amount = row[1]['Amount']
        description = row[1]['Description']
        conn = connect_to_db()

        cursor = conn.cursor()

        insert_query = """
        INSERT INTO expense_tracker (Date, Time, Category, Amount, Description)
        VALUES (%s, %s, %s, %s, %s);
        """

        cursor.execute(insert_query, (date, time, category, amount, description))

        conn.commit()

        cursor.close()
        conn.close()





# In[39]:


def add_expense_to_db(date, time, category, amount, description , db_params = db_params): 


    conn = connect_to_db()

    cursor = conn.cursor()

    insert_query = """
    INSERT INTO expense_tracker (Date, Time, Category, Amount, Description)
    VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(insert_query, (date, time, category, amount, description))

    conn.commit()

    cursor.close()
    conn.close()



# In[40]:


def export_postgres_to_csv(db_params =db_params, query =query, csv_file_path = csv_file_path):
   
    try:
        
        conn = connect_to_db()
        
        df = pd.read_sql_query(query, conn)
        
        df.to_csv(csv_file_path, index=False)
        
        print(f"Data exported successfully to {csv_file_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            conn.close()




# In[ ]:





# In[41]:




# In[ ]:


def get_all_expenses():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expense_tracker")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    export_postgres_to_csv(db_params, query, csv_file_path)

    return expenses

def delete_expense(expense_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expense_tracker WHERE ID = %s", (expense_id,))
    conn.commit()
    cursor.close()
    conn.close()

