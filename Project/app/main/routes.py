from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Point
from app.forms import PointForm
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PointForm()
    if form.validate_on_submit():
        # Парсинг координат из одной строки
        try:
            coordinates = form.coordinates.data.split(',')
            if len(coordinates) != 2:
                raise ValueError("Неверный формат координат.")
            longitude = float(coordinates[0].strip())
            latitude = float(coordinates[1].strip())
            # Дополнительная валидация координат
            if not (-180 <= longitude <= 180):
                flash('Долгота должна быть в диапазоне от -180 до 180.', 'danger')
                return redirect(url_for('main.index'))
            if not (-90 <= latitude <= 90):
                flash('Широта должна быть в диапазоне от -90 до 90.', 'danger')
                return redirect(url_for('main.index'))
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('main.index'))

        description = form.description.data.strip() if form.description.data else None

        point = Point(
            longitude=longitude,
            latitude=latitude,
            description=description,
            author=current_user
            # created_at устанавливается автоматически
        )
        db.session.add(point)
        db.session.commit()
        flash('Точка добавлена и ожидает подтверждения администратором.', 'success')
        return redirect(url_for('main.index'))

    # Получение всех подтвержденных точек для отображения на карте
    points = Point.query.filter_by(confirmed=True).all()
    return render_template('main/index.html', form=form, points=points)


@main_bp.route('/api/points')
@login_required
def get_points():
    points = Point.query.filter_by(confirmed=True).all()
    points_data = [
        {
            'longitude': p.longitude,
            'latitude': p.latitude,
            'description': p.description,
            'created_at': p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for p in points
    ]
    return jsonify(points_data)
