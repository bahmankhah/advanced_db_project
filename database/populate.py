import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

df = pd.read_csv('Google-Playstore.csv')

connection = psycopg2.connect(
    host="localhost",
    database="playstore_db",
    user="postgres",
    password="1234"
)
cursor = connection.cursor()

def clean_int(value):
    if pd.isna(value):
        return None
    try:
        clean_value = float(str(value).replace(',', '').replace('+', ''))
        return int(clean_value)
    except ValueError:
        return None  

cursor.execute("""
CREATE TABLE IF NOT EXISTS developers (
    developer_id SERIAL PRIMARY KEY,
    developer_name TEXT UNIQUE NOT NULL,
    developer_website TEXT,
    developer_email TEXT,
    privacy_policy TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS apps (
    app_id SERIAL PRIMARY KEY,
    app_name TEXT NOT NULL,
    app_unique_id TEXT UNIQUE NOT NULL,
    developer_id INTEGER REFERENCES developers(developer_id),
    category_id INTEGER REFERENCES categories(category_id),
    rating FLOAT,
    rating_count BIGINT,
    installs BIGINT,
    min_installs BIGINT,
    max_installs BIGINT,
    free BOOLEAN,
    price FLOAT,
    currency TEXT,
    size TEXT,
    minimum_android_version TEXT,
    released_date TEXT,
    last_updated TEXT,
    content_rating TEXT,
    ad_supported BOOLEAN,
    in_app_purchases BOOLEAN,
    editor_choice BOOLEAN
);
""")

connection.commit()

developers = df[['Developer Id', 'Developer Website', 'Developer Email', 'Privacy Policy']].drop_duplicates()
developer_values = [
    (row['Developer Id'], row['Developer Website'], row['Developer Email'], row['Privacy Policy'])
    for _, row in developers.iterrows()
]
execute_values(cursor, """
INSERT INTO developers (developer_name, developer_website, developer_email, privacy_policy)
VALUES %s ON CONFLICT (developer_name) DO NOTHING;
""", developer_values)

categories = df['Category'].unique()
category_values = [(category,) for category in categories]
execute_values(cursor, "INSERT INTO categories (name) VALUES %s ON CONFLICT (name) DO NOTHING;", category_values)

connection.commit()

cursor.execute("SELECT developer_id, developer_name FROM developers")
developer_dict = {name: dev_id for dev_id, name in cursor.fetchall()}

cursor.execute("SELECT category_id, name FROM categories")
category_dict = {name: cat_id for cat_id, name in cursor.fetchall()}

app_values = []
for _, row in df.iterrows():
    try:
        installs = clean_int(row['Installs'])
        min_installs = clean_int(row['Minimum Installs'])
        max_installs = clean_int(row['Maximum Installs'])
        rating_count = clean_int(row['Rating Count'])
        price = float(row['Price']) if not pd.isna(row['Price']) else 0.0

        app_values.append((
            row['App Name'],
            row['App Id'],
            developer_dict.get(row['Developer Id'], None),
            category_dict.get(row['Category'], None),
            float(row['Rating']) if not pd.isna(row['Rating']) else None,
            rating_count,
            installs,
            min_installs,
            max_installs,
            row['Free'] == 'True',
            price,
            row['Currency'],
            row['Size'],
            row['Minimum Android'],
            row['Released'],
            row['Last Updated'],
            row['Content Rating'],
            row['Ad Supported'] == 'True',
            row['In App Purchases'] == 'True',
            row['Editors Choice'] == 'True'
        ))
    except Exception as e:
        print(f"Error processing row {row['App Name']}: {e}")

execute_values(cursor, """
INSERT INTO apps (
    app_name, app_unique_id, developer_id, category_id, rating, rating_count, installs, min_installs, max_installs,
    free, price, currency, size, minimum_android_version, released_date, last_updated, content_rating,
    ad_supported, in_app_purchases, editor_choice
) VALUES %s;
""", app_values)

connection.commit()

cursor.close()
connection.close()
