eval $(cat .env)

cd alembic
alembic "$@"