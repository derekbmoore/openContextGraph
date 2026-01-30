import os
import psycopg2

try:
    conn = psycopg2.connect(
        host="ctxeco-db.postgres.database.azure.com",
        user="ctxecoadmin",
        password="67490c0abe68fec49a96bd78085c2c7c",
        dbname="postgres",
        sslmode="require",
        port=5432
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Connected to DB.")
    
    # 1. Create User
    try:
        cur.execute("CREATE USER zep_user WITH PASSWORD 'ZepUserSafePW2026';")
        print("Created zep_user.")
    except psycopg2.errors.DuplicateObject:
        print("User zep_user already exists.")
        # Update password just in case
        cur.execute("ALTER USER zep_user WITH PASSWORD 'ZepUserSafePW2026';")
        print("Updated zep_user password.")

    # 2. Grant permissions
    # Grant CONNECT on database zep
    # Note: Database 'zep' must exist.
    try:
        cur.execute("GRANT ALL PRIVILEGES ON DATABASE zep TO zep_user;")
        print("Granted privileges on database zep.")
    except Exception as e:
        print(f"Error granting privileges: {e}")
        
    print("Done.")
    
except Exception as e:
    print(f"Connection failed: {e}")
