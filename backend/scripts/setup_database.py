"""
Database Setup Script
Runs schema.sql and seed.sql to initialize the MySQL database with tables and sample data.
"""
import os
import sys
from pathlib import Path

import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create a database connection using environment variables."""
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        charset='utf8mb4'
    )

def run_sql_file(connection, sql_file_path):
    """Execute SQL commands from a file."""
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Split by semicolon and execute each statement
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    
    with connection.cursor() as cursor:
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                    connection.commit()
                except Exception as e:
                    print(f"Error executing statement: {e}")
                    print(f"Statement: {statement[:100]}...")
                    connection.rollback()
                    raise

def main():
    """Main setup function."""
    print("Setting up Synthetic AI User Backend database...")
    
    # Get SQL file paths
    backend_dir = Path(__file__).parent.parent
    schema_file = backend_dir / 'sql' / 'schema.sql'
    seed_file = backend_dir / 'sql' / 'seed.sql'
    
    if not schema_file.exists():
        print(f"Error: Schema file not found at {schema_file}")
        sys.exit(1)
    
    if not seed_file.exists():
        print(f"Error: Seed file not found at {seed_file}")
        sys.exit(1)
    
    try:
        # Connect to MySQL (without database specified)
        print("Connecting to MySQL...")
        connection = get_db_connection()
        
        # Drop existing database if exists to ensure clean setup
        print("Dropping existing database (if exists)...")
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS synthetic_ai_user")
            connection.commit()
        print("✓ Existing database dropped")
        
        # Run schema
        print(f"Running schema from {schema_file}...")
        run_sql_file(connection, schema_file)
        print("✓ Schema created successfully")
        
        # Run seed data
        print(f"Running seed data from {seed_file}...")
        run_sql_file(connection, seed_file)
        print("✓ Seed data inserted successfully")
        
        connection.close()
        print("\n✓ Database setup complete!")
        print("\nDatabase: synthetic_ai_user")
        print("Tables: users, experiments, personas, surveys, responses, interview_sessions, insights, reports")
        print("Sample data: 1 user, 1 experiment, 6 personas, 1 survey, 6 responses, 1 insight, 1 report")
        
    except Exception as e:
        print(f"\n✗ Error during database setup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
