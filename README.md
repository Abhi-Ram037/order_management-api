\# Django Order Management API



\## Project Overview



The Django Order Management API is a REST API developed using Django and Django REST Framework. It allows users to manage customers, products, and customer orders.



The system automatically calculates order totals, checks product stock, reduces stock when an order is created, and restores stock when an order is cancelled.



\## Technologies Used



\- Python

\- Django

\- Django REST Framework

\- SQLite3

\- Django Admin

\- REST API



\## Features



\- Create customers

\- Create products

\- Create orders

\- Calculate order total automatically

\- Check available product stock

\- Reduce stock after order creation

\- View all orders

\- View order details

\- Update order status

\- Cancel orders

\- Restore product stock after cancellation

\- Validate customers and products

\- Prevent orders above available stock

\- Django Admin support



\## Project Structure



```text

order\_management/

│

├── manage.py

├── db.sqlite3

├── requirements.txt

├── README.md

│

├── order\_management/

│   ├── settings.py

│   ├── urls.py

│   ├── asgi.py

│   └── wsgi.py

│

└── orders/

&#x20;   ├── admin.py

&#x20;   ├── models.py

&#x20;   ├── serializers.py

&#x20;   ├── urls.py

&#x20;   ├── views.py

&#x20;   └── migrations/

```



\## Database Models



\### Customer



Stores customer information.



Fields:



\- id

\- name

\- email



\### Product



Stores product information.



Fields:



\- id

\- name

\- price

\- stock



\### Order



Stores order information.



Fields:



\- id

\- customer

\- order\_date

\- total\_amount

\- status



Available statuses:



\- Pending

\- Confirmed

\- Shipped

\- Delivered

\- Cancelled



\### OrderItem



Stores products included in an order.



Fields:



\- id

\- order

\- product

\- quantity

\- price



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| POST | `/customers/` | Create a customer |

| POST | `/products/` | Create a product |

| POST | `/orders/` | Create an order |

| GET | `/orders/` | Get all orders |

| GET | `/orders/<id>/` | Get order details |

| PUT | `/orders/<id>/status/` | Update order status |

| POST | `/orders/<id>/cancel/` | Cancel an order |



\## Create Customer



\### Request



```json

{

&#x20;   "name": "Abhiram",

&#x20;   "email": "abhiram@gmail.com"

}

```



\## Create Product



\### Request



```json

{

&#x20;   "name": "Laptop",

&#x20;   "price": 50000,

&#x20;   "stock": 10

}

```



\## Create Order



\### Request



```json

{

&#x20;   "customer": 1,

&#x20;   "items": \[

&#x20;       {

&#x20;           "product": 1,

&#x20;           "quantity": 2

&#x20;       },

&#x20;       {

&#x20;           "product": 2,

&#x20;           "quantity": 3

&#x20;       }

&#x20;   ]

}

```



The system automatically calculates the total amount.



For example:



```text

Laptop: 50000 × 2 = 100000

Mouse: 1000 × 3 = 3000



Total = 103000

```



The product stock is also reduced automatically.



\## Update Order Status



\### Request



```json

{

&#x20;   "status": "Confirmed"

}

```



Supported status updates:



```text

Pending

Confirmed

Shipped

Delivered

```



\## Cancel Order



Use:



```text

POST /orders/<id>/cancel/

```



When an order is cancelled:



1\. The order status becomes Cancelled.

2\. The ordered quantities are added back to product stock.

3\. A success response is returned.



\## Validation



The API validates:



\- Customer existence

\- Product existence

\- Customer name

\- Customer email

\- Product price

\- Product stock

\- Order quantity

\- Order status

\- Cancelled orders

\- Delivered orders



The system does not allow an order quantity greater than available stock.



\## Running the Project



\### 1. Create and activate virtual environment



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



\### 2. Install dependencies



```powershell

pip install -r requirements.txt

```



\### 3. Apply migrations



```powershell

python manage.py migrate

```



\### 4. Run the server



```powershell

python manage.py runserver

```



The API will be available at:



```text

http://127.0.0.1:8000/

```



\## Admin Panel



Django Admin is available at:



```text

http://127.0.0.1:8000/admin/

```



The admin panel can be used to view:



\- Customers

\- Products

\- Orders

\- Order Items



\## Testing



The project was tested for:



\- Customer creation

\- Product creation

\- Order creation

\- Automatic total calculation

\- Stock reduction

\- Order details

\- Order status update

\- Order cancellation

\- Stock restoration

\- Invalid customer validation

\- Invalid product validation

\- Insufficient stock validation

\- Cancelled order protection



\## Home API



The root URL provides an overview of the available endpoints:



```text

GET /

```



Example response:



```json

{

&#x20;   "message": "Order Management API",

&#x20;   "endpoints": {

&#x20;       "customers": "/customers/",

&#x20;       "products": "/products/",

&#x20;       "orders": "/orders/",

&#x20;       "admin": "/admin/"

&#x20;   }

}

```



\## Conclusion



The Django Order Management API provides a simple and reliable way to manage customers, products, and orders. It uses Django REST Framework to provide RESTful API endpoints and SQLite3 for data storage. Automatic stock management and order validation help maintain accurate order and product information.

