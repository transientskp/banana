"""
This app is only here for testing purposes. Since we don't want Django to
manage our TRAP databases, we defined managed = False in the banana model. But
if you want to run the test suite you need to create some model to test! So
this app will dynamically alter the managed variable so the model is created.
"""