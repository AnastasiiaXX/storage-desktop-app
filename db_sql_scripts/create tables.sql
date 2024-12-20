CREATE TABLE if not exists supplier_type (
	id SERIAL PRIMARY KEY NOT NULL,
	title VARCHAR(4) NOT NULL
);

CREATE TABLE IF NOT EXISTS material_type (
	id SERIAL PRIMARY KEY NOT NULL,
	title VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS materials (
	id SERIAL PRIMARY KEY NOT NULL,
	title VARCHAR(50) UNIQUE,
	material_type_id INT NOT NULL REFERENCES material_type(id) ON DELETE CASCADE,
	image VARCHAR(250) NULL,
	price MONEY,
	stock_quantity INT CHECK(stock_quantity >= 0),
    	min_quantity INT CHECK(min_quantity >= 0) ,
    	package_quantity INT CHECK(package_quantity >= 0),
    	unit VARCHAR(5) CHECK (unit IN ('л', 'м', 'г', 'кг'))
);

CREATE TABLE IF NOT EXISTS suppliers (
	id SERIAL PRIMARY KEY NOT NULL,
	title VARCHAR(100) UNIQUE,
	supplier_type_id INT NOT NULL REFERENCES supplier_type(id) ON DELETE CASCADE,
	INN BIGINT UNIQUE,
	quality_rating INT,
	start_date DATE
);

CREATE TABLE IF NOT EXISTS materials_suppliers (
	material_id INT NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
	supplier_id INT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
	UNIQUE (material_id, supplier_id)
);
