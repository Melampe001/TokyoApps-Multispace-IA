-- Tabla de facturas (Invoices)
CREATE EXTERNAL TABLE IF NOT EXISTS invoices (
    invoice_id STRING,
    user_id STRING,
    amount DECIMAL(10,2),
    currency STRING,
    status STRING,
    product_id STRING,
    product_name STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata STRING
)
PARTITIONED BY (
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake/billing-data/invoices/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'projection.enabled'='true',
    'projection.year.type'='integer',
    'projection.year.range'='2020,2030',
    'projection.month.type'='integer',
    'projection.month.range'='1,12',
    'projection.day.type'='integer',
    'projection.day.range'='1,31',
    'storage.location.template'='s3://tokyo-ia-data-lake/billing-data/invoices/year=${year}/month=${month}/day=${day}'
);

-- Tabla de transacciones (Transactions)
CREATE EXTERNAL TABLE IF NOT EXISTS transactions (
    transaction_id STRING,
    invoice_id STRING,
    user_id STRING,
    amount DECIMAL(10,2),
    currency STRING,
    payment_method STRING,
    status STRING,
    created_at TIMESTAMP,
    metadata STRING
)
PARTITIONED BY (
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake/billing-data/transactions/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'projection.enabled'='true',
    'projection.year.type'='integer',
    'projection.year.range'='2020,2030',
    'projection.month.type'='integer',
    'projection.month.range'='1,12',
    'projection.day.type'='integer',
    'projection.day.range'='1,31',
    'storage.location.template'='s3://tokyo-ia-data-lake/billing-data/transactions/year=${year}/month=${month}/day=${day}'
);

-- Tabla de usuarios (Users)
CREATE EXTERNAL TABLE IF NOT EXISTS users (
    user_id STRING,
    email STRING,
    name STRING,
    status STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata STRING
)
PARTITIONED BY (
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake/billing-data/users/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'projection.enabled'='true',
    'projection.year.type'='integer',
    'projection.year.range'='2020,2030',
    'projection.month.type'='integer',
    'projection.month.range'='1,12',
    'projection.day.type'='integer',
    'projection.day.range'='1,31',
    'storage.location.template'='s3://tokyo-ia-data-lake/billing-data/users/year=${year}/month=${month}/day=${day}'
);

-- Tabla de suscripciones (Subscriptions)
CREATE EXTERNAL TABLE IF NOT EXISTS subscriptions (
    subscription_id STRING,
    user_id STRING,
    plan_id STRING,
    plan_name STRING,
    status STRING,
    price DECIMAL(10,2),
    currency STRING,
    billing_cycle STRING,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata STRING
)
PARTITIONED BY (
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake/billing-data/subscriptions/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'projection.enabled'='true',
    'projection.year.type'='integer',
    'projection.year.range'='2020,2030',
    'projection.month.type'='integer',
    'projection.month.range'='1,12',
    'projection.day.type'='integer',
    'projection.day.range'='1,31',
    'storage.location.template'='s3://tokyo-ia-data-lake/billing-data/subscriptions/year=${year}/month=${month}/day=${day}'
);
