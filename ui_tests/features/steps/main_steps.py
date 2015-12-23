from behave import given, when, then
from ui_tests.pages.base import PageObjectFactory
from ui_tests.pages.examplePages import GooglePage
from hamcrest import assert_that


@given('I am on the google page')
def step(context):
    context.page = PageObjectFactory().create(GooglePage)
    context.page.open()


@when('I search the word "{search_word}"')
def step(context, search_word):
    context.word = search_word
    context.page.search(search_word)


@then('I should see that the search is performed correctly')
def step(context):
    assert_that(context.page.is_search_correct(context.word))
