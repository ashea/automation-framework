from modules import behave


def before_all(context):
    behave.context_initializer(context, browser_size="large")


def after_feature(context, feature):
    behave.after_feature(context, feature)


def before_scenario(context, scenario):
    behave.before_scenario(context, scenario)


def after_scenario(context, scenario):
    behave.after_scenario(context, scenario)
