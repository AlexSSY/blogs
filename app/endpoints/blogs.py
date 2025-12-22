from starlette_wtf import csrf_protect
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse

from app.core.templating import templating
from app.forms.signup import SignUpForm


def home_page(request: Request):
    return templating.TemplateResponse(request, 'blogs/home.html', {'hello_world': 'Hello World from Jinja2.'})


@csrf_protect
async def signup_page(request: Request):
    form_template = templating.get_template('forms/signup.html')
    signup_form = await SignUpForm.from_formdata(request)
    if await signup_form.validate_on_submit():
        return PlainTextResponse('SUCCESS')
    html = form_template.render(request=request, form=signup_form)
    return HTMLResponse(html)
