from api import app, db

# Flask provides a mechanism for an application to install its own error pages, 
# so that your users don't have to see the plain and boring default ones.
# To declare a custom error handler, the @errorhandler decorator is used.

@app.errorhandler(404)
def not_found_error(error):
    # TODO --------
    return 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    # TODO --------
    return 500

# Error handling placeholder.
def bad_request():
    pass
