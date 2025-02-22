from behave import given, when, then
from ui_tests.pages.base import PageObjectFactory
from ui_tests.pages.examplePages import LoginPage


@given('I am in the login page')
def step(context):
    context.page = PageObjectFactory().create(LoginPage)
    context.page.open()


@when('I input credentials "{user_email}" and "{user_password}')
def step(context, user_email, user_password):
    context.page.input_credentials(user_email, user_password)


@then('I should see the login error message displayed correctly')
def step(context):
    assert context.page.is_login_error_displayed(), "Login error message was not displayed"


@then('I should see the login success message')
def step(context):
    assert context.page.is_login_success(), "Login error message was not displayed"


@then('I should see that the search is performed wrongly')
def step(context):
    assert not context.page.is_search_correct(context.word)
