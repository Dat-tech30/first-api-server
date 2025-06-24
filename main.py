# ------------------ IMPORTS ------------------
from fastapi import FastAPI, HTTPException         # FastAPI ussed to create the API server, HTTPException is handling exceptions and throwing errors
from motor.motor_asyncio import AsyncIOMotorClient # Motor is the MongoDB library that works with FastAPI async code, and AsyncIOMotorClient iss how connect to MongoDB database
from dotenv import load_dotenv                     # Load .env file with MongoDB URI
from bson import ObjectId                          # Needed to handle MongoDB document IDs
import os                                          # Access environment variables

# ------------------ CONFIG ------------------
load_dotenv()  # Load .env file before using os.getenv
MONGO_URI = os.getenv("MONGO_URI")  # Grab MongoDB connection string

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["bookdb"]           # Use (or create) database called bookdb
collection = db["books"]        # Use (or create) collection called books

# ------------------ FASTAPI APP ------------------
app = FastAPI()

# ------------------ HELPER FUNCTION ------------------
def book_helper(book) -> dict:
    """This converts MongoDB object to dictionary with a string id"""
    return {
        "id": str(book["_id"]), # MongoDB’s _id is an ObjectId, so we convert it to a regular string
        "title": book["title"], # Get the book's title from MongoDB
        "author": book["author"]  # Get the book's author from MongoDB
    }

# ------------------ ROUTES ------------------

# Root route (just a welcome message)
@app.get("/")
async def root():
    return {"message": "Welcome, this is my first ever use of an API"}

# CREATE: Add a book
@app.post("/books")
async def add_book(book: dict):
    result = await collection.insert_one(book) # this adds the book to MongoDB
    new_book = await collection.find_one({"_id": result.inserted_id}) # Mongo gives back the ID of what was inserted, getting the exact book again
    return book_helper(new_book) # format the book using the helper function and return it to the user

# ---------------------------- Section ------------------------------
# READ: Get all books
@app.get("/books")
async def get_books():
    books = []
    async for book in collection.find(): # go through every book in the collection
        books.append(book_helper(book)) # convert in mongo format into a clean dictionary then add to the lists
    return books 
# ---------------------------- Section ------------------------------

# UPDATE: Update a book by ID
@app.put("/books/{id}")
async def update_book(id: str, data: dict):
    # 1. Added try-except to catch invalid ObjectId errors and return 400 Bad Request instead of server error 
    # 2. Used acknowledged update check with matched_count, because modified_count==0 if no fields changed but book exists 
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    result = await collection.update_one({"_id": obj_id}, {"$set": data}) # finds the book by id and changes only the fields passed in the data 
    if result.matched_count == 0: # if no book was actually found
        raise HTTPException(status_code=404, detail="Book not found")
    updated = await collection.find_one({"_id": obj_id}) # grab the updated book from the data based 
    return book_helper(updated) # return the updated book 
# ---------------------------- Section ------------------------------

# DELETE: Delete a book by ID
@app.delete("/books/{id}")
async def delete_book(id: str):
    # Added try-except for invalid ObjectId format for better error handling 
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    result = await collection.delete_one({"_id": obj_id}) # tries to delete the book with the given MongoDB id 
    if result.deleted_count == 0: # if no book was deleted (wrong ID) return an error 
        raise HTTPException(status_code=404, detail="Book not found") 
    return {"message": "Book deleted"} # return a confirmation message if the book was deleted 


