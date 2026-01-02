from starlette.routing import Route, Router

from .views import SignUp, signin_page, signout_page


routes = (
    Route("/signup", SignUp, name='signup_page'),
    Route("/signin", signin_page, methods=("GET", "POST"), name='signin_page'),
    Route("/signout", signout_page, methods=("POST", ), name="signout_page"),
)

router = Router(routes)
