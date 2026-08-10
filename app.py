from flask import Flask, redirect, url_for, session
from flask_session import Session
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Flask-Session
    Session(app)
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.exam import exam_bp
    from routes.proctoring import proctoring_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(proctoring_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from flask import send_from_directory
    @app.route('/evidence/<attempt_id>/<filename>')
    def serve_evidence(attempt_id, filename):
        if 'admin_user' not in session:
            return redirect(url_for('admin.login'))
        return send_from_directory(app.config['EVIDENCE_DIR'], f"{attempt_id}/{filename}")
    
    @app.route('/')
    def index():
        session.clear()
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
