# ecommerce_api
A simple ecommerce Api
# E-commerce API

This is a robust and scalable e-commerce backend API built with FastAPI and MongoDB. It provides a set of endpoints for managing products, user authentication, a shopping cart, and a checkout process.

The API is designed to be easy to use and provides clear, interactive documentation via Swagger UI, making it simple to test and integrate with a front-end application.

## 🚀 Features

* **Product Management:** Retrieve a list of all products or fetch a single product by its ID.
* **User Authentication:** Secure endpoints for user registration and login.
* **Shopping Cart:** Add, update, and manage products in a user's cart.
* **Checkout Process:** Calculate the total cost of items in the cart, including a tax component.
* **Database Integration:** Utilizes MongoDB for efficient and flexible data storage.
* **Interactive Documentation:** Automatically generated and well-organized API documentation using FastAPI's Swagger UI.

## 🛠️ Technologies Used

* **Framework:** FastAPI
* **Database:** MongoDB
* **Driver:** PyMongo
* **Dependency Management:** Pip
* **Asynchronous Server:** Uvicorn
* **Environment Variables:** python-dotenv
* **Validation:** Pydantic

## 🚀 Getting Started

Follow these steps to set up and run the API locally on your machine.

### Prerequisites

Make sure you have the latest python version installed on your system.

### Installation

1.  Clone this repository:

    ```bash
    git clone <your-repository-url>
    cd <your-repository-folder>
    ```

2.  Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, you can install the dependencies manually:

    ```bash
    pip install fastapi "uvicorn[standard]" pymongo pydantic python-dotenv
    ```

### Environment Variables

Create a file named `.env` in the root directory of the project and add your MongoDB connection string. Replace `<your_username>`, `<your_password>`, and `<cluster_url>` with your own credentials.

```env
MONGO_URI="mongodb+srv://<your_username>:<your_password>@<cluster_url>/?retryWrites=true&w=majority"
```
## Preview of Api structure
<img width="860" height="598" alt="image" src="https://github.com/user-attachments/assets/c930eeed-5b66-4613-b24a-286857a87393" />

## Preview of products
<img width="879" height="594" alt="image" src="https://github.com/user-attachments/assets/ab7da60e-c9e9-45bb-aed7-b4301afdb2fe" />

## Preview of registering a user
<img width="957" height="589" alt="image" src="https://github.com/user-attachments/assets/4ec12862-9e32-4742-8fd2-ccbeae14257e" />

## How to contact me
* **Email**: claudiaagyeere@gmail.com

##    --------------------------------------------------------------THANK YOU FOR YOUR TIME----------------------------------------------------------------------

