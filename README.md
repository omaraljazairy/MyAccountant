# MyAccountant
--------------
is an API created to help me manage my invoices. I can create, modify and get an overview of my incomes with and without tax. It also reminds my of uploading receipts to my accountant app.
This api is built using Python FastAPI.


## Class Diagram
----------------

```mermaid
classDiagram
    class Customer
    Customer: +id int
    Customer: +name str
    Customer: +created datetime

    class Contract
    Contract: +id int
    Contract: +customer_id int
    Contract: +unit str
    Contract: +rate float
    Contract: +start_date date
    Contract: +created datetime

    Customer "1" --> "many" Contract

    class Income
    Income: +id int
    Income: +contract_id int
    Income: +total float
    Income: +invoice_date str
    Income: +created datetime

    Income: +invoice_month_year() str
    Income: +rate_unit() str
    Income: +customer_name() str
    Income: +customer_id() int
    Income: +total_rate_excl_vat() float
    Income: +total_rate_incl_vat() float
    Income: +total_yearly_vat() float
    Income: +total_netto() float


    Income "1" --> "1" Contract
    Contract "1" --> "many" Income
    
```
