from setuptools import setup, find_packages

setup(
    name="restaurant_api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "sqlalchemy>=1.4.0",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=0.19.0",
        "python-jose>=3.3.0",
        "passlib>=1.7.4"
    ],
    python_requires=">=3.7",
)