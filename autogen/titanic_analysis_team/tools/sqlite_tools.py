"""
SQLite MCP Tools for Titanic Database
"""
import sqlite3
import json
from typing import Dict, Any, List
# Simple tool decorator for compatibility
def Tool(func):
    """Simple tool decorator for compatibility"""
    func._is_tool = True
    return func

# Database path
DB_PATH = "data/titanic.db"

def get_db_connection():
    """Get SQLite database connection"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def execute_query(query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Execute SQL query and return results as list of dictionaries"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Fetch all results and convert to list of dictionaries
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

@Tool
def query_titanic_data(query: str, params: Dict[str, Any] = None) -> str:
    """
    Execute SQL query on Titanic database.
    
    Args:
        query: SQL query string
        params: Optional parameters for the query (as dictionary)
    
    Returns:
        JSON string with query results
    """
    results = execute_query(query, params)
    return json.dumps(results, indent=2)

@Tool
def get_survivors_by_age(age: int) -> str:
    """
    Get survival statistics for passengers of a specific age.
    
    Args:
        age: Age to filter by
    
    Returns:
        JSON string with survival statistics
    """
    query = """
    SELECT 
        COUNT(*) as total_passengers,
        SUM(survived) as survived_passengers,
        SUM(CASE WHEN age = ? THEN 1 ELSE 0 END) as total_specific_age,
        SUM(CASE WHEN age = ? AND survived = 1 THEN 1 ELSE 0 END) as survived_specific_age
    FROM Observation
    """
    results = execute_query(query, [age, age])
    return json.dumps(results, indent=2)

@Tool
def get_passenger_demographics() -> str:
    """
    Get demographic breakdown of Titanic passengers.
    
    Returns:
        JSON string with demographic statistics
    """
    query = """
    SELECT 
        COUNT(*) as total_passengers,
        SUM(survived) as total_survived,
        ROUND(AVG(age), 2) as average_age,
        MIN(age) as min_age,
        MAX(age) as max_age,
        SUM(CASE WHEN survived = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as survival_rate
    FROM Observation
    WHERE age IS NOT NULL
    """
    results = execute_query(query)
    return json.dumps(results, indent=2)

@Tool
def get_survival_by_class() -> str:
    """
    Get survival statistics by passenger class.
    
    Returns:
        JSON string with survival statistics by class
    """
    query = """
    SELECT 
        pclass,
        COUNT(*) as total_passengers,
        SUM(survived) as survived_passengers,
        ROUND(SUM(survived) * 100.0 / COUNT(*), 2) as survival_rate
    FROM Observation
    GROUP BY pclass
    ORDER BY pclass
    """
    results = execute_query(query)
    return json.dumps(results, indent=2)

@Tool
def search_passengers(age_min: int = None, age_max: int = None, 
                     survived: int = None, pclass: int = None, limit: int = 10) -> str:
    """
    Search for passengers with specific criteria.
    
    Args:
        age_min: Minimum age
        age_max: Maximum age
        survived: Survival status (0 or 1)
        pclass: Passenger class (1, 2, or 3)
        limit: Maximum number of results to return
    
    Returns:
        JSON string with matching passengers
    """
    conditions = []
    params = []
    
    if age_min is not None:
        conditions.append("age >= ?")
        params.append(age_min)
    
    if age_max is not None:
        conditions.append("age <= ?")
        params.append(age_max)
    
    if survived is not None:
        conditions.append("survived = ?")
        params.append(survived)
    
    if pclass is not None:
        conditions.append("pclass = ?")
        params.append(pclass)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
    SELECT age, survived, pclass, fare, adult_male, alone
    FROM Observation
    WHERE {where_clause}
    LIMIT ?
    """
    params.append(limit)
    
    results = execute_query(query, params)
    return json.dumps(results, indent=2)

@Tool
def get_database_schema() -> str:
    """
    Get the database schema information.
    
    Returns:
        JSON string with table and column information
    """
    query = """
    SELECT 
        name as table_name,
        sql as table_sql
    FROM sqlite_master 
    WHERE type='table' AND name='Observation'
    """
    results = execute_query(query)
    return json.dumps(results, indent=2)
