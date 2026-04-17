import contextlib
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from db import init_db, close_db
from ariadne.asgi import GraphQL
from graphql_schema import schema


@contextlib.asynccontextmanager
async def lifespan(app):
    await init_db()
    yield
    await close_db()


graphql_app = GraphQL(schema=schema, debug=True)

routes = [
    Route("/health", lambda r: JSONResponse({"status": "healthy"})),
    Mount("/graphql", graphql_app),
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
