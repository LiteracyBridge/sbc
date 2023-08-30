# Write a script to import data from csv files to the database. The script should
# be able to import data from the following csv files:

import psycopg2
import csv
from models import LuIndiKit
from models import get_db


# Connect to the PostgreSQL database
# conn = psycopg2.connect(
#     host="localhost",
#     database="mydatabase",
#     user="myusername",
#     password="mypassword"
# )
def import_indikit():
    db = next(get_db())

    results = db.query(LuIndiKit).all()
    existing_data = {}
    # Reshape the results into a dictionary where the key is the import_id
    # and the value is the entire row. This will make it easier to check
    # if a row already exists.
    for result in results:
        existing_data[result.import_id] = result

    # Open and read each CSV file
    pending_save = []
    with open("indikit.csv", "r") as csvfile:
        # Parse the CSV data
        csvreader = csv.reader(csvfile)
        for index, row in enumerate(csvreader):
            if index == 0:
                continue

            record = LuIndiKit()
            import_id = int(row[14])
            is_new = True

            # check if import_id exists in the results
            if existing_data.get(import_id) is not None:
                record = existing_data[import_id]
                is_new = False

            record.section = row[0]
            record.sector = row[1]
            record.sub_sector = row[2]
            record.indicator_level_1 = row[4]
            record.name = row[8]
            record.wording_english = row[9]
            record.wording_french = row[10]
            record.wording_portuguese = row[11]
            record.wording_czech = row[12]
            record.guidance = row[13]
            record.import_id = import_id
            record.purpose = row[15]

            if is_new:
                db.add(record)
                pending_save.append(record)
            else:
                db.commit()

            # print(row)
            # break
        # Insert the data into the appropriate table

    db.bulk_save_objects(pending_save)
    db.commit()

#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO mytable (column1, column2, column3) VALUES (%s, %s, %s)", row)
#         cursor.close()

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

import_indikit()
