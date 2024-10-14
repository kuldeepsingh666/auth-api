from setuptools import setup, find_packages

setup(
    name="auth-api",
    version="0.1.0",
    description="A reusable authentication API with FastAPI",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "uvicorn",
        "pydantic",
        "passlib",
        "python-jose",
        "python-multipart",
        "python-dotenv"
    ],
    include_package_data=True,
)
