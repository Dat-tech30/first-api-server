import os
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from main import app, collection, book_helper
from httpx import AsyncClient

client = TestClient(app)  # Create a test client for sending synchronous HTTP requests to FastAPI app

# --------- UNIT TESTS (mock DB) ---------

def test_book_helper():
    # This test checks if the helper function converts MongoDB document correctly
    sample = {"_id": "abc123", "title": "Mock Title", "author": "Mock Author"}
    result = book_helper(sample)
    # Assert that book_helper returns expected dict with string id and other fields intact
    assert result == {"id": "abc123", "title": "Mock Title", "author": "Mock Author"}

@pytest.mark.asyncio
async def test_add_book_unit(mocker):
    # This test mocks DB calls to test the add_book endpoint without hitting real database

    mock_insert = MagicMock()  
    mock_insert.inserted_id = "mockid"  # Mock an inserted ID as would be returned by MongoDB

    # Patch collection.insert_one to return our mocked insert result asynchronously
    mocker.patch.object(collection, "insert_one", AsyncMock(return_value=mock_insert))
    # Patch collection.find_one to return a mocked book document when queried with inserted_id
    mocker.patch.object(collection, "find_one", AsyncMock(return_value={
        "_id": "mockid", "title": "Unit Test", "author": "Tester"
    }))

    # Use the synchronous test client to post a book creation request
    response = client.post("/books", json={"title": "Unit Test", "author": "Tester"})
    # Confirm the endpoint responded with status 200 (success)
    assert response.status_code == 200
    data = response.json()
    # Check that the returned data has the correct title, author, and includes an id field
    assert data["title"] == "Unit Test"
    assert data["author"] == "Tester"
    assert "id" in data

# --------- INTEGRATION / API TESTS (real DB) ---------

@pytest.mark.asyncio
async def test_crud_integration():
    # This test performs actual requests to the live API with real DB interaction using AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Step 1: Create a new book by sending POST request with book data
        res = await ac.post("/books", json={"title": "Integration Test", "author": "Tester"})
        assert res.status_code == 200  # Make sure creation succeeded
        book = res.json()  # Parse returned JSON book object
        book_id = book["id"]  # Save the id for further operations

        # Step 2: Retrieve list of all books via GET request
        res = await ac.get("/books")
        assert res.status_code == 200  # Confirm the GET succeeded
        books = res.json()
        # Verify that the created book is present in the list by checking its ID
        assert any(b["id"] == book_id for b in books)

        # Step 3: Update the created book by sending PUT request with new title
        res = await ac.put(f"/books/{book_id}", json={"title": "Updated Title"})
        assert res.status_code == 200  # Check update was successful
        # Confirm the title was updated as requested
        assert res.json()["title"] == "Updated Title"

        # Step 4: Delete the book by sending DELETE request with book ID
        res = await ac.delete(f"/books/{book_id}")
        assert res.status_code == 200  # Confirm deletion succeeded
        # Check that the response contains expected confirmation message
        assert res.json() == {"message": "Book deleted"}