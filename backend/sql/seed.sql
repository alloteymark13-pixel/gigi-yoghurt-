-- sample products
INSERT INTO products(name, sku, unit, unit_size, shelf_life_days)
VALUES
('Plain 250g', 'PL-250', 'g', 250, 10),
('Strawberry 250g','ST-250','g',250,10)
ON CONFLICT DO NOTHING;

-- sample ingredients
INSERT INTO ingredients(name, uom, cost_per_uom, reorder_point)
VALUES
('Milk','kg',0.80,20),
('Sugar','kg',0.60,5),
('Starter Culture','kg',10.00,1),
('Glass Jar','each',0.12,100)
ON CONFLICT DO NOTHING;

-- sample recipes (qty per unit in ingredient UOM)
INSERT INTO recipes(product_id, ingredient_id, qty_per_unit)
SELECT p.product_id, i.ingredient_id, v.qty FROM
(SELECT product_id FROM products WHERE sku='PL-250') p,
(SELECT ingredient_id FROM ingredients WHERE name='Milk') i,
(VALUES (0.25)) v(qty)
ON CONFLICT DO NOTHING;

INSERT INTO recipes(product_id, ingredient_id, qty_per_unit)
SELECT p.product_id, i.ingredient_id, v.qty FROM
(SELECT product_id FROM products WHERE sku='PL-250') p,
(SELECT ingredient_id FROM ingredients WHERE name='Sugar') i,
(VALUES (0.02)) v(qty)
ON CONFLICT DO NOTHING;

-- initial inventory (IN)
INSERT INTO inventory_tx(ingredient_id, quantity, tx_type, ref)
VALUES
((SELECT ingredient_id FROM ingredients WHERE name='Milk'), 200, 'IN', 'initial_stock'),
((SELECT ingredient_id FROM ingredients WHERE name='Sugar'), 50, 'IN', 'initial_stock'),
((SELECT ingredient_id FROM ingredients WHERE name='Starter Culture'), 5, 'IN', 'initial_stock'),
((SELECT ingredient_id FROM ingredients WHERE name='Glass Jar'), 500, 'IN', 'initial_stock');
