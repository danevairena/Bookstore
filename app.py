# Main application module

from api import create_app, db
from api.models import User, Post

app = create_app()

# With a regular interpreter session, the app symbol is not known unless it is explicitly imported, 
# but when using flask shell, the command pre-imports the application instance.
# You can also configure a "shell context", which is a list of other symbols to pre-import
# make_shell_context() function creates a shell context that adds the database instance and models to the shell session
# After you add the shell context processor function you can work with database entities without having to import them
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}