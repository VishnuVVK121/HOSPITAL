
import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hospital_db"
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                gender VARCHAR(10),
                illness VARCHAR(255)
            )
        """)
        self.conn.commit()

    def add_patient(self, pid, name, age, gender, illness):
        self.cursor.execute("INSERT INTO patients (id, name, age, gender, illness) VALUES (%s, %s, %s, %s, %s)",
                            (pid, name, age, gender, illness))
        self.conn.commit()

    def get_all_patients(self):
        self.cursor.execute("SELECT * FROM patients")
        return self.cursor.fetchall()

    def get_patient(self, pid):
        self.cursor.execute("SELECT * FROM patients WHERE id = %s", (pid,))
        return self.cursor.fetchone()

    def delete_patient(self, pid):
        self.cursor.execute("DELETE FROM patients WHERE id = %s", (pid,))
        self.conn.commit()
        return self.cursor.rowcount > 0
