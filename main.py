from flask import Flask, jsonify
from flasgger import Swagger
from app.extensions import db, jwt
from app.users.auth import auth_bp
from app.users.users import user_bp
from app.users.models import User, TokenBlocklist


def create_app(config_class=None):

    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_prefixed_env()

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')

    swagger = Swagger(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        indentity = jwt_data['sub']
        return User.query.filter_by(username = indentity).one_or_none()

    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity ==  "Joa":
            return {"is_staff": True}
        return {"is_staff": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error":"token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"Signature verification failed", "error":"invalid_token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message":"Request doesnt contain valid token", "error":"authorization_header"}), 401

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
        jti = jwt_data['jti']

        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None
  
    return app 

