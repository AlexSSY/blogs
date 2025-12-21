from starlette.routing import Route

from app.endpoints.blogs import home_page


routes = (
    Route("/", home_page, methods=("GET", )),
)
