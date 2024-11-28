from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Point
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Доступ запрещен. Требуются права администратора.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    points = Point.query.filter_by(confirmed=False).all()
    return render_template('admin/dashboard.html', points=points)

@admin_bp.route('/confirm/<int:point_id>')
@login_required
@admin_required
def confirm_point(point_id):
    point = Point.query.get_or_404(point_id)
    point.confirmed = True
    db.session.commit()
    flash('Точка подтверждена.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete/<int:point_id>', methods=['POST'])
@login_required
@admin_required
def delete_point(point_id):
    point = Point.query.get_or_404(point_id)
    db.session.delete(point)
    db.session.commit()
    flash('Точка удалена.', 'info')
    return redirect(url_for('admin.dashboard'))
