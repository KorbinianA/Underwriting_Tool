import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from scoring import load_data, underwriting_scoring

load_dotenv()

url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "my_db"),
)

engine = create_engine(url)

df = load_data(engine)

scored_df = underwriting_scoring(df)

print(scored_df.head())