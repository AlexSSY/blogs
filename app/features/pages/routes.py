from starlette.routing import Route, Router

from .views import home_page


routes = (
    Route("/", home_page, methods=("GET", ), name='home_page'),
)

router = Router(routes)
