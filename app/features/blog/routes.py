from starlette.routing import Route

from .views import home_page


routes = (
    Route("/", home_page, methods=("GET", ), name='home_page'),
)
