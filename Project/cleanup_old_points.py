from app import create_app, db
from app.models import Point
from datetime import datetime, timedelta

def cleanup_old_points():
    app = create_app()
    with app.app_context():
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        old_points = Point.query.filter(Point.created_at < one_month_ago).all()
        if old_points:
            for point in old_points:
                db.session.delete(point)
            db.session.commit()
            print(f"Удалено {len(old_points)} точек, которым больше месяца.")
        else:
            print("Нет точек для удаления.")

if __name__ == "__main__":
    cleanup_old_points()
