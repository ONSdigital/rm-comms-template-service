# Need to call these functions in run.py to set them up


def register_teardowns(app):
    @app.teardown_request
    def close_session(response_or_exception):
        try:
            if not response_or_exception:
                app.db.session.commit()
            else:
                app.db.session.rollback()
        finally:
            app.db.session.remove()
            # the scoped session from flask-sqlalchemy is supposed to be removed but better safe than sorry
        return response_or_exception
