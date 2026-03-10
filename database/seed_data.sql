-- ============================================================================
-- Seed Data for Grocery Store Management System
-- Sample data for testing and demonstration
-- ============================================================================

USE grocery_store_db;

-- ============================================================================
-- SAMPLE PRODUCTS
-- ============================================================================

-- Beverages
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888001', 'Coca Cola 1.5L', 1, 45.00, 35.00, 100, 20, 'Refreshing carbonated soft drink'),
('8888888002', 'Pepsi 1.5L', 1, 45.00, 35.00, 80, 20, 'Classic cola beverage'),
('8888888003', 'Mountain Dew 1.5L', 1, 45.00, 35.00, 75, 20, 'Citrus flavored soda'),
('8888888004', 'Orange Juice 1L', 1, 65.00, 50.00, 60, 15, '100% pure orange juice'),
('8888888005', 'Bottled Water 500ml', 1, 15.00, 10.00, 200, 50, 'Purified drinking water');

-- Dairy Products
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888011', 'Fresh Milk 1L', 2, 85.00, 70.00, 50, 15, 'Fresh whole milk'),
('8888888012', 'Skimmed Milk 1L', 2, 90.00, 75.00, 45, 15, 'Low-fat milk'),
('8888888013', 'Yogurt 500ml', 2, 55.00, 45.00, 80, 20, 'Natural yogurt'),
('8888888014', 'Cheddar Cheese 200g', 2, 120.00, 95.00, 30, 10, 'Premium cheddar cheese'),
('8888888015', 'Butter 250g', 2, 95.00, 75.00, 40, 12, 'Salted butter');

-- Bakery
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888021', 'White Bread Loaf', 3, 55.00, 45.00, 60, 20, 'Soft white bread'),
('8888888022', 'Whole Wheat Bread', 3, 65.00, 50.00, 40, 15, 'Healthy whole grain bread'),
('8888888023', 'Croissant Pack of 6', 3, 85.00, 65.00, 35, 10, 'Buttery croissants'),
('8888888024', 'Chocolate Cake', 3, 250.00, 180.00, 15, 5, 'Delicious chocolate cake'),
('8888888025', 'Cookies 400g', 3, 75.00, 55.00, 50, 15, 'Assorted cookies');

-- Snacks
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888031', 'Potato Chips 100g', 4, 35.00, 25.00, 120, 30, 'Crispy potato chips'),
('8888888032', 'Chocolate Bar', 4, 25.00, 18.00, 150, 40, 'Milk chocolate bar'),
('8888888033', 'Peanuts 200g', 4, 45.00, 32.00, 90, 25, 'Roasted peanuts'),
('8888888034', 'Popcorn 150g', 4, 40.00, 28.00, 80, 20, 'Butter flavored popcorn'),
('8888888035', 'Pretzels 200g', 4, 50.00, 35.00, 70, 18, 'Salted pretzels');

-- Household Items
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888041', 'Dish Soap 500ml', 5, 45.00, 35.00, 70, 20, 'Lemon scented dish soap'),
('8888888042', 'Toilet Paper 4-pack', 5, 120.00, 95.00, 50, 15, 'Soft toilet tissue'),
('8888888043', 'Paper Towels 2-roll', 5, 65.00, 50.00, 60, 18, 'Absorbent paper towels'),
('8888888044', 'Laundry Detergent 1L', 5, 150.00, 120.00, 40, 12, 'Powerful cleaning detergent'),
('8888888045', 'Trash Bags 20pcs', 5, 75.00, 55.00, 55, 15, 'Strong garbage bags');

-- Fresh Produce
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888051', 'Fresh Apples 1kg', 6, 120.00, 100.00, 30, 10, 'Crisp red apples'),
('8888888052', 'Bananas 1kg', 6, 65.00, 50.00, 45, 12, 'Sweet ripe bananas'),
('8888888053', 'Oranges 1kg', 6, 95.00, 75.00, 35, 10, 'Juicy oranges'),
('8888888054', 'Tomatoes 1kg', 6, 85.00, 65.00, 40, 12, 'Fresh tomatoes'),
('8888888055', 'Lettuce Head', 6, 45.00, 32.00, 50, 15, 'Crisp lettuce');

-- Meat & Seafood
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888061', 'Chicken Breast 500g', 7, 180.00, 150.00, 25, 8, 'Boneless chicken breast'),
('8888888062', 'Ground Beef 500g', 7, 220.00, 180.00, 20, 7, 'Lean ground beef'),
('8888888063', 'Pork Chops 500g', 7, 195.00, 165.00, 22, 7, 'Fresh pork chops'),
('8888888064', 'Salmon Fillet 300g', 7, 350.00, 290.00, 15, 5, 'Fresh salmon'),
('8888888065', 'Shrimp 250g', 7, 280.00, 230.00, 18, 6, 'Fresh shrimp');

-- Frozen Foods
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888071', 'Ice Cream 1L', 8, 150.00, 120.00, 40, 12, 'Vanilla ice cream'),
('8888888072', 'Frozen Pizza', 8, 185.00, 145.00, 35, 10, 'Deluxe frozen pizza'),
('8888888073', 'Frozen Vegetables Mix 500g', 8, 75.00, 60.00, 50, 15, 'Mixed vegetables'),
('8888888074', 'Chicken Nuggets 400g', 8, 165.00, 130.00, 45, 12, 'Crispy chicken nuggets'),
('8888888075', 'French Fries 750g', 8, 95.00, 75.00, 55, 15, 'Golden french fries');

-- Canned Goods
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888081', 'Canned Tuna 185g', 9, 65.00, 50.00, 80, 20, 'Tuna in oil'),
('8888888082', 'Canned Corn 400g', 9, 45.00, 35.00, 90, 25, 'Sweet corn kernels'),
('8888888083', 'Tomato Sauce 400g', 9, 55.00, 42.00, 75, 20, 'Tomato pasta sauce'),
('8888888084', 'Chicken Soup 400ml', 9, 60.00, 48.00, 70, 18, 'Creamy chicken soup'),
('8888888085', 'Baked Beans 400g', 9, 50.00, 38.00, 85, 22, 'Beans in tomato sauce');

-- Personal Care
INSERT INTO products (barcode, product_name, category_id, unit_price, cost_price, stock_quantity, reorder_level, description) VALUES
('8888888091', 'Shampoo 400ml', 10, 125.00, 95.00, 55, 15, 'Moisturizing shampoo'),
('8888888092', 'Conditioner 400ml', 10, 135.00, 105.00, 50, 14, 'Hair conditioner'),
('8888888093', 'Body Soap 100g', 10, 35.00, 25.00, 100, 25, 'Antibacterial soap'),
('8888888094', 'Toothpaste 100ml', 10, 85.00, 65.00, 75, 20, 'Whitening toothpaste'),
('8888888095', 'Toothbrush', 10, 45.00, 32.00, 90, 22, 'Soft bristle toothbrush');

-- ============================================================================
-- CONFIRMATION
-- ============================================================================

-- Display count of products added
SELECT 
    c.category_name,
    COUNT(p.product_id) as product_count,
    SUM(p.stock_quantity * p.unit_price) as total_value
FROM products p
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY c.category_name;

-- Total summary
SELECT 
    COUNT(*) as total_products,
    SUM(stock_quantity) as total_units,
    SUM(stock_quantity * unit_price) as total_inventory_value
FROM products;
