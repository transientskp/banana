"""
This app is only here for testing purposes. Since we don't want Django to
manage our TRAP databases, we defined managed = False in the model. But
if you want to run the test suite you need some data! So this app will
dynamically alter the managed variable so the model is created.
"""