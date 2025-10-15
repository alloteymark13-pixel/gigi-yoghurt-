-- products (final SKUs)
CREATE TABLE IF NOT EXISTS products (
  product_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  sku TEXT UNIQUE,
  unit TEXT,
  unit_size INTEGER,
  shelf_life_days INTEGER DEFAULT 7
);

-- ingredients
CREATE TABLE IF NOT EXISTS ingredients (
  ingredient_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  uom TEXT,
  cost_per_uom NUMERIC(12,4),
  reorder_point NUMERIC(12,4) DEFAULT 0
);

-- recipe lines
CREATE TABLE IF NOT EXISTS recipes (
  recipe_id SERIAL PRIMARY KEY,
  product_id INTEGER REFERENCES products(product_id),
  ingredient_id INTEGER REFERENCES ingredients(ingredient_id),
  qty_per_unit NUMERIC(12,6)
);

-- production batches
CREATE TABLE IF NOT EXISTS batches (
  batch_id SERIAL PRIMARY KEY,
  batch_code TEXT UNIQUE,
  product_id INTEGER REFERENCES products(product_id),
  planned_qty INTEGER,
  actual_qty INTEGER,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  status TEXT DEFAULT 'planned',
  total_cost NUMERIC(12,4)
);

-- inventory transactions (positive for IN, negative for OUT)
CREATE TABLE IF NOT EXISTS inventory_tx (
  tx_id SERIAL PRIMARY KEY,
  ingredient_id INTEGER REFERENCES ingredients(ingredient_id),
  quantity NUMERIC(12,6),
  tx_type TEXT,
  ref TEXT,
  timestamp TIMESTAMP DEFAULT now()
);

-- sales
CREATE TABLE IF NOT EXISTS sales (
  sale_id SERIAL PRIMARY KEY,
  product_id INTEGER REFERENCES products(product_id),
  qty INTEGER,
  sale_price NUMERIC(12,4),
  sale_time TIMESTAMP DEFAULT now()
);

-- orders
CREATE TABLE IF NOT EXISTS orders (
  order_id SERIAL PRIMARY KEY,
  customer_name TEXT NOT NULL,
  phone TEXT NOT NULL,
  product_id INTEGER REFERENCES products(product_id),
  quantity INTEGER NOT NULL,
  price NUMERIC(12,4),
  total_amount NUMERIC(12,4),
  status TEXT DEFAULT 'Pending',
  delivery_date DATE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- users
CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(150) UNIQUE NOT NULL,
  email VARCHAR(254),
  hashed_password VARCHAR(512) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  is_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT now()
);
