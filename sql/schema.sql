-- =============================================================================
-- ShopPulse — Schéma relationnel PostgreSQL (dataset Olist, 9 fichiers CSV)
-- Exécuté automatiquement à l'initialisation du conteneur PostgreSQL.
-- Ordre de création conforme aux dépendances de clés étrangères.
-- =============================================================================

-- Nettoyage (idempotent)
DROP TABLE IF EXISTS order_reviews       CASCADE;
DROP TABLE IF EXISTS order_payments      CASCADE;
DROP TABLE IF EXISTS order_items         CASCADE;
DROP TABLE IF EXISTS orders              CASCADE;
DROP TABLE IF EXISTS products            CASCADE;
DROP TABLE IF EXISTS sellers             CASCADE;
DROP TABLE IF EXISTS customers           CASCADE;
DROP TABLE IF EXISTS geolocation         CASCADE;
DROP TABLE IF EXISTS category_translation CASCADE;

-- -----------------------------------------------------------------------------
-- Tables de référence
-- -----------------------------------------------------------------------------
CREATE TABLE category_translation (
    product_category_name         TEXT PRIMARY KEY,
    product_category_name_english TEXT
);

-- La géolocalisation comporte plusieurs lignes par préfixe de code postal
-- (clé non naturelle) → identifiant de substitution.
CREATE TABLE geolocation (
    geolocation_id          BIGSERIAL PRIMARY KEY,
    geolocation_zip_code_prefix INTEGER NOT NULL,
    geolocation_lat         DOUBLE PRECISION,
    geolocation_lng         DOUBLE PRECISION,
    geolocation_city        TEXT,
    geolocation_state       CHAR(2)
);
CREATE INDEX idx_geolocation_zip ON geolocation (geolocation_zip_code_prefix);

CREATE TABLE customers (
    customer_id               TEXT PRIMARY KEY,
    customer_unique_id        TEXT NOT NULL,
    customer_zip_code_prefix  INTEGER,
    customer_city             TEXT,
    customer_state            CHAR(2)
);
CREATE INDEX idx_customers_unique ON customers (customer_unique_id);

CREATE TABLE sellers (
    seller_id                 TEXT PRIMARY KEY,
    seller_zip_code_prefix    INTEGER,
    seller_city               TEXT,
    seller_state              CHAR(2)
);

CREATE TABLE products (
    product_id                 TEXT PRIMARY KEY,
    product_category_name      TEXT,
    product_name_length        INTEGER,
    product_description_length  INTEGER,
    product_photos_qty         INTEGER,
    product_weight_g           INTEGER,
    product_length_cm          INTEGER,
    product_height_cm          INTEGER,
    product_width_cm           INTEGER,
    CONSTRAINT fk_products_category
        FOREIGN KEY (product_category_name)
        REFERENCES category_translation (product_category_name)
);

-- -----------------------------------------------------------------------------
-- Tables transactionnelles
-- -----------------------------------------------------------------------------
CREATE TABLE orders (
    order_id                      TEXT PRIMARY KEY,
    customer_id                   TEXT NOT NULL,
    order_status                  TEXT NOT NULL,
    order_purchase_timestamp      TIMESTAMP,
    order_approved_at             TIMESTAMP,
    order_delivered_carrier_date  TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);
CREATE INDEX idx_orders_customer ON orders (customer_id);
CREATE INDEX idx_orders_status   ON orders (order_status);
CREATE INDEX idx_orders_purchase ON orders (order_purchase_timestamp);

CREATE TABLE order_items (
    order_id          TEXT NOT NULL,
    order_item_id     INTEGER NOT NULL,
    product_id        TEXT NOT NULL,
    seller_id         TEXT NOT NULL,
    shipping_limit_date TIMESTAMP,
    price             NUMERIC(12, 2),
    freight_value     NUMERIC(12, 2),
    PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT fk_items_order   FOREIGN KEY (order_id)   REFERENCES orders (order_id),
    CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products (product_id),
    CONSTRAINT fk_items_seller  FOREIGN KEY (seller_id)  REFERENCES sellers (seller_id)
);
CREATE INDEX idx_items_product ON order_items (product_id);
CREATE INDEX idx_items_seller  ON order_items (seller_id);

CREATE TABLE order_payments (
    order_id             TEXT NOT NULL,
    payment_sequential   INTEGER NOT NULL,
    payment_type         TEXT,
    payment_installments INTEGER,
    payment_value        NUMERIC(12, 2),
    PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT fk_payments_order FOREIGN KEY (order_id) REFERENCES orders (order_id)
);

-- Un même review_id peut apparaître sur plusieurs commandes → identifiant de substitution.
CREATE TABLE order_reviews (
    review_pk              BIGSERIAL PRIMARY KEY,
    review_id              TEXT NOT NULL,
    order_id               TEXT NOT NULL,
    review_score           SMALLINT CHECK (review_score BETWEEN 1 AND 5),
    review_comment_title   TEXT,
    review_comment_message TEXT,
    review_creation_date   TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    CONSTRAINT fk_reviews_order FOREIGN KEY (order_id) REFERENCES orders (order_id)
);
CREATE INDEX idx_reviews_order ON order_reviews (order_id);
CREATE INDEX idx_reviews_score ON order_reviews (review_score);
