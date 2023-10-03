## FastAPI E-Commerce Dashboard

A back-end API that can power a web admin dashboard for e-commerce managers.

### Table of Contents

- Dependencies
- Setup Guid
- Code Explanation
- API Explanation


### Dependencies

The dependencies are listed in the requirements.txt file. 

### Setup Guide

You need following to run this project:

- Python 3.9
- MySQL
- venv

Once you have installed the above and have cloned the repository, you can 
follow the following steps to get the project up and running:

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
 ```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Start the database instance.

4. Copy the `.env.example` file to `.env` and update the values.

5. To populate the database with demp data, run the demo_data.py file. 
```bash
python demo_data.py
```
The demo_data.py file will first create the database if it does not exist. It
will then create all the tables, and then create some demo data. 

6. Run the server:

```bash
python main.py
```

The server should now be running on `http://localhost:8000` and the API 
documentation should be available at `http://localhost:8000/docs`.

### Code Explanation

There are 2 main directories in the project:

1. `core`: This directory contains the central code of this project. It 
  contains code like database connections, database creation, configuration, middlewares and server initialization.

2. `app`: This directory contains the actual application code. It contains the models, repositories, api, and schemas for the application. 
The directory has the following subdirectories:
   - `api` This directory contains the API layer of the application. It contains the API router, all the endpoints are defined here.
   - `models` this contains all the models.
   - `repository` For each model, we have a repository. This is 
    where the CRUD operations for the model are defined.
   - `schemas` This is where the request and response schemas for the 
   application are defined.


### API Explanation

- **Get Inventory Status Endpoint**
The "Get Inventory Status" endpoint allows you to retrieve the current inventory status for products, including low stock alerts. 

        HTTP Method: GET

        Path: /v1/inventory

        Query Parameters: low_stock_threshold (optional): An integer value that represents the minimum quantity at which a product is considered to be in low stock. Products with a current quantity less than or equal to this threshold will be flagged as low stock.

        Response: The endpoint returns a list of InventoryStatus objects, each providing product_id, product_name, current_quantity, low_stock


- **Update Inventory Endpoint**
The "Update Inventory" endpoint allows you to modify the inventory levels for 
products and track changes over time. 

        HTTP Method: POST

        Path: /v1/inventory/update

        Request Body: Provide the following data in the request body to update the inventory for a product:

            product_id: The unique identifier of the product.
            quantity_change: The quantity change value, which can be positive (to increase stock) or negative (to decrease stock).

        Response: The endpoint returns an InventoryChange object, which provides details about the inventory update, including the product's ID, name, the quantity change, and the new quantity after the update.


- **Get Products Endpoint**
The "Get Products" endpoint retrieves a list of products from the database. 

        HTTP Method: GET

        Path: /api/products

        Query Parameters:

            limit (Optional): maximum number of products to retrieve in a single request.  Default is 10.
            offset (Optional): number of products to skip before starting to retrieve products. Default is 0.

        Response: The endpoint returns a list of product objects, each containing details such as product ID, name, description, price, and the associated category.


- **Register Product Endpoint**
The "Register Product" endpoint used to register a new product

        HTTP Method: POST

        Path: /v1/products/register

        Request Body: The request body should contain the details of the product to be  registered, including the product name, description, price, and the associated category.

        Response: returns the newly created product object.


- **Revenue Across Time Period Endpoint**
The "Revenue Across Time Period" endpoint calculates the total 
revenue for a specified time period.

        HTTP Method: GET

        Path: /v1/revenue/timeperiod

        Query Parameters: You need to provide two query parameters:

            start_date: The start date of the time period for revenue calculation.
            end_date: The end date of the time period for revenue calculation.

        Response: returns the total revenue generated during the specified time period.


- **Daily Revenue Analysis Endpoint**
The "Daily Revenue Analysis" endpoint allows you to calculate the total revenue
on a daily basis for a specified number of days.

        HTTP Method: GET

        Path: /v1/revenue/daily

        Query Parameters: 

            days (default value: 7): The number of days to analyze. This parameter determines the duration for which daily revenue data will be calculated.

        Response: the endpoint returns a list of daily revenue data, including the date and total revenue for each day within the specified time frame.


- **Weekly Revenue Analysis Endpoint**
The "Weekly Revenue Analysis" endpoint allows you to calculate the total revenue
on a weekly basis for a specified number of weeks.

        HTTP Method: GET

        Path: /v1/revenue/weekly

        Query Parameters: 

            weeks (default value: 4): The number of weeks to analyze. This parameter determines the duration for which weekly revenue data will be calculated.

        Response: the endpoint returns a list of weekly revenue data, including the date and total revenue for each week within the specified time frame.


- **Monthly Revenue Analysis Endpoint**
The "Monthly Revenue Analysis" endpoint allows you to calculate the total revenue
on a monthly basis for a specified number of months.

        HTTP Method: GET

        Path: /v1/revenue/monthly

        Query Parameters: 

            months (default value: 6): The number of months to analyze. This parameter  determines the duration for which monthly revenue data will be calculated.

        Response: the endpoint returns a list of monthly revenue data, including the date and total revenue for each month within the specified time frame.


- **Annual Revenue Analysis Endpoint**
The "Annual Revenue Analysis" endpoint allows you to calculate the total revenue
on an annual basis for a specified number of years.

        HTTP Method: GET

        Path: /v1/revenue/annual

        Query Parameters: 
    
            years (default value: 2): The number of yeasr to analyze. This parameter determines the duration for which yeasr revenue data will be calculated.

        Response: the endpoint returns a list of annual revenue data, including the date and total revenue for each year within the specified time frame.


- **Compare Product Revenue Endpoint**
This endpoint compares the total revenue across multiple products.

        HTTP Method: GET
    
        Path: /v1/revenue/products

        Query Parameters:

            product_ids (required): A list of product IDs that you want to compare for revenue analysis. 

        Response: the endpoint returns a list of revenue data for the specified products. Each entry includes the product name and the total revenue generated by that product.


- **Compare Category Revenue Endpoint**
This endpoint compares the total revenue across multiple categories.

        HTTP Method: GET

        Path: /v1/revenue/categories

        Query Parameters:

            category_ids (required): A list of category IDs that you want to compare for revenue analysis. 

        Response: the endpoint returns a list of revenue data for the specified categories. Each entry includes the category name and the total revenue generated for that category.


- **Get Sales Data**
This endpoint allows you to retrieve sales data from the database.

        HTTP Method: GET
        Path: /v1/sales

        Query Parameters:
            limit (optional): The number of sales records to return (default is 10).
            offset (optional): The starting index for pagination (default is 0).


- **Filter Sales by Date**
This endpoint enables you to filter sales data based on a specified date range.

        HTTP Method: GET
        Path: /v1/sales/date

        Query Parameters:

            start_date (required): The start date of the date range for filtering sales data.
            end_date (required): The end date of the date range for filtering sales data.


- **Filter Sales Product**
This endpoint allows you to filter sales data by a specific product using its unique product ID. 

        HTTP Method: GET
        Path: /v1/sales/product

        Query Parameters:
            product_id (required): The unique identifier of the product for which you want to filter sales data.

        Response: the endpoint returns a list of sales data for the specified product.


- **Filter Sales Category**
This endpoint allows you to filter sales data by a specific product using its 
unique product ID. 

        HTTP Method: GET
        Path: /v1/sales/category

        Query Parameters:
            category_id (required): The unique identifier of the category for which you want to filter sales data.

        Response: the endpoint returns a list of sales data for the specified category.


- **Analyze Sales**
This endpoint provides an analysis of sales data.

        HTTP Method: GET
        Path: /v1/sales/analyze

        Response Model: SalesAnalysis
        This endpoint returns an instance of the SalesAnalysis response model, which contains the following information:

        total_sales: The total number of sales quantities recorded in the dataset.
        average_revenue: The average revenue generated per sale.
        sales_per_product: A list of objects containing the names of products and their
        corresponding total sales quantities.
        sales_per_category: A list of objects containing the names of product categories and their total sales quantities.