from functools import wraps

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, OperationalError

from database.extensions import db


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Integrity error - Possible duplicate entry"}), 400
        except DataError:
            db.session.rollback()
            return jsonify({"error": "Data error - Invalid data format or value"}), 400
        except OperationalError:
            db.session.rollback()
            return jsonify({"error": "Operational error - Operational issue such as NOT NULL constraint"}), 500
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return wrapper
