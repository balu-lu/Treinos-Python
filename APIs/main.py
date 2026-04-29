from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Return a simple greeting response."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Return an item by ID and optional query string."""
    return {"item_id": item_id, "q": q}
