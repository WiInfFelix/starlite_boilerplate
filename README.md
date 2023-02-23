# Starlite Minimal Boilerplate

This project implements a small boilerplate for setting up a starlite project for small projects

It does the follwing:
- Create and connect to a SQLite3 DB using the Starlite SQLAlchemy plugin
- Creates a very basic User model and corresponding handlers for creation, listing and deletion
- Demonstrates basic authorization using the built-in JWT CookieAuth for some routes

## To start:
- Clone the project with `git clone` and step into directory
- Install dependencies via poetry: `poetry install`
- Run the __main.py__ script