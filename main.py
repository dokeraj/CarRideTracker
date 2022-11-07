import api_controller
import sqliteDatabase

# run the first time
print("STARTING SCRIPT..")

# initialize the db
print("Initializing sqlite database..")
sqliteDatabase.init_db()

api_controller.runApi()
