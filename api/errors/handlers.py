# Flask provides a mechanism for an application to install its own error pages, 
# so that your users don't have to see the plain and boring default ones.

from api import db

# Import blueprint
from api.errors import bp

# instead of attaching the error handlers to the application with the @app.errorhandler decorator, 
# the blueprint's @bp.app_errorhandler decorator. While both decorators achieve the same end result, 
# the idea is to try to make the blueprint independent of the application so that it is more portable.

@bp.app_errorhandler(404)
def not_found_error(error):
    # TODO --------
    return 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    # TODO --------
    return 500
