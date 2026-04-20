import contextlib
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from assignment.db import init_db, close_db
from ariadne.asgi import GraphQL
from assignment.graphql_schema import schema
from assignment.core import LoggerSetup
from assignment.core.config import REDIS_HOST, REDIS_PORT, REDIS_DB
from arq.connections import create_pool, RedisSettings
from assignment.routes.google_oauth_routes import (
    google_callback,
    google_login,
    me,
    logout,
)

logger = LoggerSetup().setup_logger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app):
    await init_db()
    app.state.redis = await create_pool(
        RedisSettings(host=REDIS_HOST, port=REDIS_PORT, database=REDIS_DB)
    )
    yield
    await close_db()


def get_context_value(request, data):
    return {
        "request": request,
        "redis": request.app.state.redis,
    }


graphql_app = GraphQL(schema=schema, debug=True, context_value=get_context_value)

routes = [
    Route("/health", lambda r: JSONResponse({"status": "healthy"})),
    Route("/auth/google/login", google_login),
    Route("/auth/google/callback", google_callback),
    Route("/logout", logout),
    Route("/me", me),
    Mount("/graphql", graphql_app),
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="change-me-in-production")
