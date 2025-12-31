from starlette.routing import Route

from .views import signup_page, signin_page, signout_page


routes = (
    Route("/signup", signup_page, methods=("GET", "POST"), name='signup_page'),
    Route("/signin", signin_page, methods=("GET", "POST"), name='signin_page'),
    Route("/signout", signout_page, methods=("POST", ), name="signout_page"),
)
