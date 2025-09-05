from fastapi import FastAPI, HTTPException
from bson.objectid import ObjectId
from db import products_collection, users_collection, users_cart
from pydantic import BaseModel, EmailStr
from utils import replace_id

class UserModel(BaseModel):
    email: EmailStr
    password: str

class ProductModel(BaseModel):
    name: str
    description: str
    price: float
    image: str

class CartModel(BaseModel):
    user_id: str
    product_id: str
    quantity: int

app = FastAPI()

@app.get("/")
def get_home():
    return {"message": "Welcome to our ecommerce site"}

# List some products
@app.get("/products")
def get_products():
    all_products = list(products_collection.find({}))
    return {"products": list(map(replace_id, all_products))}

@app.post("/products")
def post_products(product: ProductModel):
    products_collection.insert_one(product.model_dump())
    return {"message": "Product added successfully"}

@app.get("/products/{product_id}")
def get_product_by_id(product_id: str):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        return {"product": replace_id(product)}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/users")
def get_users():
    users = list(users_collection.find({}))
    return {"users": list(map(replace_id, users))}

@app.post("/register")
def register_user(user: UserModel):
    # Checking if user with the same email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="Email already in use")
    
    users_collection.insert_one(user.model_dump())
    return {"message": "Registered successfully"}

@app.post("/login")
def login_user(user: UserModel):
    ecommerce_user = users_collection.find_one({"email": user.email})
    if not ecommerce_user or ecommerce_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}

@app.post("/cart")
def cart(item: CartModel):
    # Check if the user and product exist before adding to cart
    if not users_collection.find_one({"_id": ObjectId(item.user_id)}):
        raise HTTPException(status_code=404, detail="User not found")
    if not products_collection.find_one({"_id": ObjectId(item.product_id)}):
        raise HTTPException(status_code=404, detail="Product not found")

    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    
    # Checking if the product is already in the cart for this user
    existing_item = users_cart.find_one({
        "user_id": ObjectId(item.user_id),
        "product_id": ObjectId(item.product_id)
    })

    if existing_item:
        # If it exists, update the quantity
        users_cart.update_one(
            {"_id": existing_item["_id"]},
            {"$inc": {"quantity": item.quantity}}
        )
    else:
        # If it's a new item, insert it
        users_cart.insert_one({
            "user_id": ObjectId(item.user_id),
            "product_id": ObjectId(item.product_id),
            "quantity": item.quantity
        })

    return {"message": f"{item.quantity} item(s) added to cart"}

@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    # Converting the string user_id from the URL to a MongoDB ObjectId
    try:
        user_id_obj = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    # Using the ObjectId in the database query
    users_cart_items = list(users_cart.find({"user_id": user_id_obj}))

    # processing the items for the response
    items = []
    for item in users_cart_items:
        # Fetching product details for each item
        product = products_collection.find_one({"_id": item.get("product_id")})
        if product:
            items.append({
                "id": str(item.get("_id")),
                "product_id": str(product.get("_id")),
                "name": product.get("name"),
                "price": product.get("price"),
                "quantity": item.get("quantity")
            })

    return {"cart_items": items}

@app.post("/checkout/{user_id}")
def checkout(user_id: str):
    # Convert the string user_id from the URL to a MongoDB ObjectId
    try:
        user_id_obj = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    cart_items = list(users_cart.find({"user_id": user_id_obj}))

    if not cart_items:
        raise HTTPException(status_code=404, detail="No items in cart")
    
    detailed_cart = []
    total = 0
    
    for item in cart_items:
        product = products_collection.find_one({"_id": item.get("product_id")})
        
        # Skip if the product is not found in the products collection
        if not product:
            continue
        
        # Calculate subtotal for the current item
        subtotal = product.get("price", 0) * item.get("quantity", 0)
        
        # Add the item's subtotal to the running total
        total += subtotal

        detailed_cart.append({
            "product_id": str(product.get("_id")),
            "name": product.get("name"),
            "price": product.get("price"),
            "quantity": item.get("quantity"),
            "subtotal": subtotal
        })
    
    return {
        "cart_items": detailed_cart,
        "total": total
    }