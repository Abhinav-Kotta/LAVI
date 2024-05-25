
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("ATLAS_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['CRAI-Pediatric']
collection = db['CompanyData']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def add_customer(phone, name, appointment_datetimes):
    customer = {
        "phone": phone,
        "name": name,
        "appointment": appointment_datetimes
    }
    collection.insert_one(customer)


def get_all_customers():
    customers = list(collection.find())
    return customers

# need to use twilio to fetch phone number first


def get_single_customer_by_phone(phone):
    customer = collection.find_one({"phone": phone})
    return customer


def reschedule_customer_appt(old_appt_date, new_appt_date, phone):
    collection.update_one(
        {"phone": phone}, {"$pull": {"appointments": old_appt_date}})
    collection.update_one(
        {"phone": phone}, {"$push": {"appointments": new_appt_date}})
