CREATE TABLE "User" (
	id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	email VARCHAR, 
	created DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
CREATE INDEX "ix_User_id" ON "User" (id);
CREATE TABLE "Customer" (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	created DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE "Contract" (
	id INTEGER NOT NULL, 
	customer_id INTEGER, 
	hourly_rate FLOAT, 
	start_date DATE, 
	created DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES "Customer" (id)
);
CREATE TABLE "Income" (
	id INTEGER NOT NULL, 
	total FLOAT, 
	contract_id INTEGER, 
	invoice_date VARCHAR, 
	excl FLOAT, 
	incl FLOAT, 
	netto FLOAT, 
	yearl_vat FLOAT, 
	created DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(contract_id) REFERENCES "Contract" (id)
);
CREATE INDEX "ix_Income_id" ON "Income" (id);
