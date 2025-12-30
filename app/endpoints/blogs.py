# from starlette_wtf import csrf_protect
# from starlette import status
# from starlette.requests import Request
# from starlette.responses import RedirectResponse

# from app.core.templating import templating
# from app.forms.signup import SignUpForm
# from app.forms.signin import SignInForm
# from app.forms.posts import AddPostForm
# from app.core.database import get_session
# from app.services import auth_service
# from app.features.shared.security import login_required


# def home_page(request: Request):
#     return templating.TemplateResponse(
#         request, "pages/home.html", {"hello_world": "Hello World from Jinja2."}
#     )


# @csrf_protect
# async def signup_page(request: Request):
#     signup_form = await SignUpForm.from_formdata(request)

#     if await signup_form.validate_on_submit():
#         async with get_session() as session:
#             hashed_password = await users.hash_password(signup_form.password.data)
#             await users.create_new_user(
#                 session, signup_form.email.data, hashed_password
#             )
#         return RedirectResponse(request.url_for("signin_page"), status.HTTP_303_SEE_OTHER)

#     status_code = (
#         status.HTTP_422_UNPROCESSABLE_CONTENT
#         if signup_form.errors
#         else status.HTTP_200_OK
#     )
#     return templating.TemplateResponse(
#         request, "pages/signup.html", {"form": signup_form}, status_code
#     )


# @csrf_protect
# async def signin_page(request: Request):
#     signin_form = await SignInForm.from_formdata(request)

#     if await signin_form.validate_on_submit():
#         async with get_session() as session:
#             user = await auth_service.authenticate(
#                 session, 
#                 signin_form.email.data,
#                 signin_form.password.data
#             )
#         if not user:
#             signin_form.invalidate()
#         else:
#             request.session['user_id'] = user.id
#             return RedirectResponse(
#                 request.url_for("home_page"), status.HTTP_303_SEE_OTHER
#             )

#     status_code = (
#         status.HTTP_422_UNPROCESSABLE_CONTENT
#         if signin_form.errors
#         else status.HTTP_200_OK
#     )
#     return templating.TemplateResponse(
#         request, "pages/signin.html", {"form": signin_form}, status_code
#     )


# async def signout_page(request: Request):
#     request.session.clear()
#     return RedirectResponse(
#         request.url_for("home_page"), status.HTTP_303_SEE_OTHER
#     )


# @login_required
# async def profile_page(request: Request):
#     return templating.TemplateResponse(
#         request, "pages/profile.html"
#     )


# @login_required
# async def add_post_page(request: Request):
#     add_post_form = await AddPostForm.from_formdata(request)
#     return templating.TemplateResponse(
#         request,
#         "pages/add_post.html",
#         {"form": add_post_form}
#     )
