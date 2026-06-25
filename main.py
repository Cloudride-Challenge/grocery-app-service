from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from grocery_storage import GroceryStorage

app = FastAPI()

GROCERY_TABLE_NAME = "grocery_items"

storage = GroceryStorage(table_name=GROCERY_TABLE_NAME)

@app.on_event("startup")
def startup_event():
    storage.init_db()

@app.get("/", response_class=HTMLResponse)
def read_grocery_list():
    try:
        items = storage.get_all_items()
        items_html = "".join([f"<li>{item}</li>" for item in items])
    except Exception as e:
        items_html = f"<p style='color:red;'>Error fetching items: {e}</p>"

    return f"""
    <html>
        <head><title>Grocery List</title></head>
        <body>
            <h1>My Grocery List</h1>
            <form action="/add" method="post">
                <input type="text" name="item" placeholder="Enter item" required />
                <button type="submit">Add</button>
            </form>
            <ul>{items_html}</ul>
        </body>
    </html>
    """

@app.post("/add")
def add_grocery_item(item: str = Form(...)):
    try:
        storage.add_item(item)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Failed to add item: {e}</h3>", status_code=500)
    
    return HTMLResponse(content="<script>window.location.href='/';</script>", status_code=200)
