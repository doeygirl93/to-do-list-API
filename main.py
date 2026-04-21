from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Recipe(BaseModel):
    recipe: str
    done: bool = False

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Hello World", "status": "ok"}

@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/item/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/recipe")
async def create_recipe(recipe: Recipe):
    return {"recipe": recipe.recipe, "done": recipe.done}

@app.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    recipes = load_recipes()
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")