import sqlite3
def make_db():
    conn = sqlite3.connect('text_data.db')
    cursor = conn.cursor()

    # Create a table to store text data
    cursor.execute('''CREATE TABLE IF NOT EXISTS text_data (
                    training_data TEXT,
                    option TEXT,
                    theme_name TEXT,
                    theme_data TEXT,
                    updated_prompt TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS credential (
                        claude_api_key TEXT,
                        gtp_api_key TEXT
                    )''')
    conn.commit()

    # Close connection
    conn.close()


def set_claude_api_key(claude_api_key):
    try:
        conn=sqlite3.connect('text_data.db')
        cursor=conn.cursor()
        cursor.execute('''SELECT claude_api_key FROM credential''')
        existing_data=cursor.fetchone()
        if existing_data:
            cursor.execute('''UPDATE credential SET claude_api_key = ?''',(claude_api_key,))
        else:
            cursor.execute('''INSERT INTO credential (claude_api_key) VALUES (?)''',(claude_api_key,))
        conn.commit()
        conn.exit()
        return "Data saved to database successfully."
    except Exception as e:
        return str(e)

def get_claude_api_key():
    try:
        conn=sqlite3.connect('text_data.db')
        cursor=conn.cursor()
        cursor.execute('''SELECT claude_api_key FROM credential''')
        data = cursor.fetchone()
        # print(data)
        conn.close()
        # print("Debug: Retrieved data:", data)
        return data[0] if data else "No data found for the given user ID and option."
        
    except Exception as e:
        return str(e)
        

def store_training_data(option, training_data):
    try:
        conn = sqlite3.connect('text_data.db')
        cursor = conn.cursor()
        # print(f"Trainging --------------------------------------------------- option : {option}  , data : {training_data}")
        # Check if data already exists for the given user ID and option
        # print("------------------------------------------ before query executore")
        cursor.execute('''SELECT training_data FROM text_data WHERE option = ?''', (option,))

        existing_data = cursor.fetchone()
        # print(f"existing user ------------------------------------------{existing_data}")
        if existing_data:
            # Update existing record
            cursor.execute('''UPDATE text_data SET training_data = ? WHERE option = ?''', (training_data,option))
            # print("Trainging --------------------------------------------------- if ")
        else:
            # Insert new record
            cursor.execute('''INSERT INTO text_data (training_data,option) VALUES (?, ?)''', (training_data, option))
            # print("Trainging --------------------------------------------------- else ")
        
        conn.commit()
        conn.close()
        
        return "Data saved to database successfully."
    except Exception as e:
        return str(e)

def store_theme_data(theme_name, theme_data):
    try:
        conn = sqlite3.connect('text_data.db')
        cursor = conn.cursor()
        # print("----------------------------------------------------------------- store theme called")
        
        # Check if data already exists for the given user ID and option
        cursor.execute('''SELECT theme_data FROM text_data WHERE theme_name = ?''', (theme_name,))
        existing_data = cursor.fetchone()
        # print(f"----------------------------------------------------------------- store theme {existing_data}")
        # print("----------------------------------------------------------------- store theme called after checking theme name")
        if existing_data:
            # Update existing record
            # print("----------------------------------------------------------------- store theme called after if ")
            cursor.execute('''UPDATE text_data SET theme_data = ? WHERE theme_name = ?''', (theme_data,theme_name))
        else:
            # Insert new record

            # print("----------------------------------------------------------------- store theme called before else")
            # print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    Theme Name : {theme_name} , Theme data : {theme_data}")
            # cursor.execute('''INSERT INTO text_data (theme_name,theme_data) VALUES (?, ?)''', (theme_name, theme_data))
            cursor.execute('''INSERT INTO text_data (theme_name, theme_data) VALUES (?, ?)''', (theme_name, str(theme_data)))
            # print("----------------------------------------------------------------- store theme called after else")
        
        conn.commit()
        conn.close()
        
        return "Data saved to database successfully."
    except Exception as e:
        return str(e)
    
def store_updated_prompt_data(updated_prompt):
    try:
        conn = sqlite3.connect('text_data.db')
        cursor = conn.cursor()
        
        # Check if data already exists for the given user ID and option
        # print(f"--------------------------------------------- updated prompt : {updated_prompt[:300]}")
        cursor.execute('''SELECT updated_prompt FROM text_data ''')
        existing_data = cursor.fetchone()
        
        if existing_data:
            # Update existing record
            # print(f"--------------------------------------------- updated prompt before if ")
            cursor.execute('''UPDATE text_data SET updated_prompt = ? ''', (updated_prompt,))
            # print(f"--------------------------------------------- updated prompt after if ")

        else:
            # Insert new record
            # print(f"--------------------------------------------- updated prompt before else ")
            cursor.execute('''INSERT INTO text_data (updated_prompt) VALUES (?)''', (updated_prompt,))
            # print(f"--------------------------------------------- updated prompt after else ")
        
        conn.commit()
        conn.close()
        
        return "Data saved to database successfully."
    except Exception as e:
        return str(e)

def get_traning_data_from_database(option):
    try:
        # print("Debug: User ID:", user_id)
        # print("Debug: Option:", option)
        # print(f"--------------------------------------------- option : {option}")
        conn = sqlite3.connect('text_data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT training_data FROM text_data WHERE option = ?''',(option,))
        data = cursor.fetchone()
        # print(data)
        conn.close()
        # print("Debug: Retrieved data:", data)
        return data[0] if data else "No data found for the given user ID and option."
    except Exception as e:
        return str(e)

def get_theme_data_from_database(theme_name):
    try:
        # print("Debug: User ID:", user_id)
        # print("Debug: Option:", option)
        conn = sqlite3.connect('text_data.db')
        cursor = conn.cursor()
        # print(f"----------------------------------------------- before getting data {theme_name}")
        cursor.execute('''SELECT theme_data FROM text_data WHERE theme_name = ?''',(theme_name,))
        # print(f"----------------------------------------------- after getting data {theme_name}")

        data = cursor.fetchone()
        # print("----------------------------------------------------- data : ",data)
        conn.close()
        # print("Debug: Retrieved data:", data)
        return data[0] if data else "No data found for the given user ID and option."
    except Exception as e:
        return str(e)

def get_prompt_from_database():
    try:
        # print("Debug: User ID:", user_id)
        # print("Debug: Option:", option)
        conn = sqlite3.connect('text_data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT updated_prompt FROM text_data ''')
        data = cursor.fetchone()
        print(data)
        conn.close()
        # print("Debug: Retrieved data:", data)
        return data[0] if data else "No prompt found"
    except Exception as e:
        return str(e)
    

        
