from app import app as application
from app.models import Profile, Project

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Profile': Profile, 'Project': Project}