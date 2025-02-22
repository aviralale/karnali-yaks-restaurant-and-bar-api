import sqlite3
import mysql.connector
from mysql.connector import Error

def migrate_sqlite_to_mysql(sqlite_db_path, mysql_config):
    """
    Migrate data from SQLite database to MySQL.
    """
    try:
        # Connect to SQLite database
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connect to MySQL database
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        
        # Get list of tables from SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'django_migrations'")
        tables = sqlite_cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"Processing table: {table_name}")
            
            # Get table schema from SQLite
            sqlite_cursor.execute(f"PRAGMA table_info(`{table_name}`)")
            columns = sqlite_cursor.fetchall()
            
            # Drop existing table if exists
            mysql_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
            
            # Create table in MySQL with escaped column names
            create_table_sql = f"CREATE TABLE `{table_name}` ("
            column_definitions = []
            
            for col in columns:
                col_name = f"`{col[1]}`"  # Escape column name
                col_type = convert_sqlite_type_to_mysql(col[2])
                nullable = "NOT NULL" if col[3] else "NULL"
                default = f"DEFAULT {col[4]}" if col[4] is not None else ""
                pk = "PRIMARY KEY" if col[5] else ""
                column_definitions.append(f"{col_name} {col_type} {nullable} {default} {pk}".strip())
            
            create_table_sql += ", ".join(column_definitions)
            create_table_sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
            
            print(f"Creating table: {table_name}")
            mysql_cursor.execute(create_table_sql)
            
            # Get data from SQLite
            sqlite_cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = sqlite_cursor.fetchall()
            
            if rows:
                # Get column names for INSERT statement
                columns_str = ", ".join(f"`{col[1]}`" for col in columns)
                placeholders = ", ".join(["%s"] * len(columns))
                insert_sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
                
                # Insert data in batches
                batch_size = 500
                for i in range(0, len(rows), batch_size):
                    batch = rows[i:i + batch_size]
                    try:
                        mysql_cursor.executemany(insert_sql, batch)
                        mysql_conn.commit()
                        print(f"Inserted {len(batch)} rows into {table_name}")
                    except Error as insert_error:
                        print(f"Error inserting into {table_name}: {insert_error}")
                        mysql_conn.rollback()
                        continue
        
        print("Migration completed successfully!")
        
    except Error as e:
        print(f"Error: {e}")
        if 'create_table_sql' in locals():
            print(f"Failed SQL: {create_table_sql}")
        
    finally:
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()

def convert_sqlite_type_to_mysql(sqlite_type):
    """
    Convert SQLite data types to MySQL equivalent.
    """
    type_mapping = {
        'INTEGER': 'INT',
        'REAL': 'DOUBLE',
        'TEXT': 'LONGTEXT',
        'BLOB': 'LONGBLOB',
        'BOOLEAN': 'TINYINT(1)',
        'DATETIME': 'DATETIME',
        'VARCHAR': 'VARCHAR(255)',
        'CHAR': 'CHAR(255)'
    }
    
    sqlite_type = sqlite_type.upper().split('(')[0]
    return type_mapping.get(sqlite_type, 'LONGTEXT')

# Configuration
sqlite_db_path = "./db.sqlite3"
mysql_config = {
    'host': 'localhost',
    'user': 'gglamoro_aviral',
    'password': '9812784982@Vi',
    'database': 'gglamoro_karnali_yaks_restaurant',
    'charset': 'utf8mb4'
}

if __name__ == "__main__":
    migrate_sqlite_to_mysql(sqlite_db_path, mysql_config)