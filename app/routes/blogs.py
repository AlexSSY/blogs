from starlette.routing import Route

from app.endpoints.blogs import (
    home_page,
    signup_page,
    signin_page,
)


routes = (
    Route("/", home_page, methods=("GET", ), name='home_page'),
    Route("/signup", signup_page, methods=("GET", "POST"), name='signup_page'),
    Route("/signin", signin_page, methods=("GET", "POST"), name='signin_page'),
)
