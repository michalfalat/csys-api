# csys-api

uvicorn app.main:app --reload

# create new DB migration

alembic revision --autogenerate

# apply migration

alembic upgrade head
