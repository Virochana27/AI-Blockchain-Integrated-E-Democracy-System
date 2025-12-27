from flask import Flask         
from .config import Config
from .extensions import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)                      

    jwt.init_app(app)

    from app.auth.routes import auth_bp
    from app.users.routes import users_bp
    from app.elections.routes import elections_bp
    from app.posts.routes import posts_bp
    from app.issues.routes import issues_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(elections_bp, url_prefix="/elections")
    app.register_blueprint(posts_bp, url_prefix="/posts")
    app.register_blueprint(issues_bp, url_prefix="/issues")

    return app
