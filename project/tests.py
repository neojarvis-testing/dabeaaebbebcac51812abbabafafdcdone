import pytest
import pyodbc

# Database connection setup
@pytest.fixture(scope="module")
def db_connection():
    connection_string = "Driver={ODBC Driver 17 for SQL Server};UID=sa;PWD=examlyMssql@123;Server=localhost;Database=appdb;Trusted_Connection=No;Persist Security Info=False;Encrypt=No"
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Setup: Create Users table if not exists
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users')
        BEGIN
            CREATE TABLE Users (
                ID INT IDENTITY(1,1) PRIMARY KEY,
                Name NVARCHAR(100),
                Email NVARCHAR(100)
            )
        END
    """)
    conn.commit()

    yield cursor, conn  # Return cursor and connection for the tests

    # Teardown: Drop Users table after tests
    cursor.execute("DROP TABLE IF EXISTS Users")
    conn.commit()
    cursor.close()
    conn.close()


# Test case 1: Insert a user
def test_insert_user(db_connection):
    cursor, conn = db_connection
    cursor.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", ('John Doe', 'john.doe@example.com'))
    conn.commit()

    cursor.execute("SELECT * FROM Users WHERE Name = 'John Doe'")
    user = cursor.fetchone()
    assert user is not None, "User should be inserted"
    assert user.Name == 'John Doe', f"Expected 'John Doe', but got {user.Name}"
    assert user.Email == 'john.doe@example.com', f"Expected 'john.doe@example.com', but got {user.Email}"


# Test case 2: Fetch users from the Users table
def test_fetch_users(db_connection):
    cursor, conn = db_connection
    cursor.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", ('Jane Doe', 'jane.doe@example.com'))
    conn.commit()

    cursor.execute("SELECT * FROM Users WHERE Name = 'Jane Doe'")
    user = cursor.fetchone()
    assert user is not None, "User should be fetched"
    assert user.Name == 'Jane Doe', f"Expected 'Jane Doe', but got {user.Name}"
    assert user.Email == 'jane.doe@example.com', f"Expected 'jane.doe@example.com', but got {user.Email}"


# Test case 3: Delete a user
def test_delete_user(db_connection):
    cursor, conn = db_connection
    cursor.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", ('Jack Smith', 'jack.smith@example.com'))
    conn.commit()

    cursor.execute("SELECT * FROM Users WHERE Name = 'Jack Smith'")
    user = cursor.fetchone()
    assert user is not None, "User should be inserted"

    # Delete the user
    cursor.execute("DELETE FROM Users WHERE Name = 'Jack Smith'")
    conn.commit()

    cursor.execute("SELECT * FROM Users WHERE Name = 'Jack Smith'")
    user = cursor.fetchone()
    assert user is None, "User should be deleted"


