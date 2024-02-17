#!/usr/bin/env python3
"""routes for the web application
"""

from models import storage
from flask_login import login_user, current_user, logout_user
from flask import abort, make_response, render_template, redirect, request, flash
from flask_login import login_required
from models.admin import Admin
from models.guardian import Guardian
from models.student import Student
from models.teacher import Teacher
from web.schedu.forms import GuardianRegForm, LoginForm, StudentRegForm, TeacherRegForm
from sqlalchemy.exc import IntegrityError
from web.schedu import *
import json
from datetime import datetime


# ------------------------------- Login Manager ------------------------------
@login_manager.user_loader
def load_user(user_id):
    """Load user from the database
    """
    return storage.get(None, user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Redirect user to sign in page if not authenticated
    """
    return redirect('/auth/sign_in')

# ---------------------------Login Route -------------------------------------

@app.route('/', strict_slashes=False)
@login_required
def index():
    """Handle the index route
    """
    form = LoginForm()
    return render_template(
        f"/dashboard_{current_user.role}.html",
        user=current_user,
        form=form)


@app.route('/auth/sign_out', methods=['POST'], strict_slashes=False)
@login_required
def sign_out():
    """Handle the sign_out route
    """
    if not current_user.is_authenticated:
        return redirect(f"/auth/sign_in")
    logout_user()
    flash('You have been logged out', 'success')
    return redirect("/auth/sign_in")


@app.route('/auth/sign_in', methods=['GET', 'POST'], strict_slashes=False)
def sign_in():
    """Handle the sign_in route"""
    if current_user.is_authenticated:
        # Redirect user to their dashboard or another page
        flash('You are already signed in')
        return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        user = storage.get(None, form.id.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome {user.first_name}, You have been logged in', 'success')
            response = make_response(redirect("/"))
            response.headers['Cache-Control'] = (
                'no-cache, no-store, must-revalidate')
            return response
        else:
            flash('Invalid ID or password', 'error')
            response = make_response(redirect("/auth/sign_in"))
            response.headers['Cache-Control'] = (
                'no-cache, no-store, must-revalidate')
            return response

    return render_template('login.html', form=form)


# ------------------------------- Register Route ----------------------------

@app.route('/register/student', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def register_student():
    """Handle the student registration route"""
    form = StudentRegForm()
    if form.validate_on_submit():
        data = form.data
        pd = data['password']
        data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        data.pop('confirm_password')
        data.pop('csrf_token')
        data.pop('submit')
        data['name'] = f"{data['first_name']} {data['last_name']}"
        student_count = storage.count("Student") + 1
        data['id'] = f"schedu-student-{data['name'][:3]}-{student_count}".lower()
        data['date_of_birth'] = data['date_of_birth'].strftime('%d-%m-%Y')
        data['role'] = "student"
        student = Student(**data)
        student.save()
        flash(f'{data["name"]} has been registered. id: {data["id"]}, password: {pd}', 'success')
        response = make_response(redirect("/"))
        response.headers['Cache-Control'] = (
            'no-cache, no-store, must-revalidate')
        return response
    else:
        print(form.errors)
    return render_template('reg_student.html', user=current_user, form=form, data=form.data)


@app.route('/register/teacher', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def register_teacher():
    """Handle the teacher registration route"""
    form = TeacherRegForm()
    print("first")
    if form.validate_on_submit():
        print("second")
        data = form.data
        pd = data['password']
        data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        data.pop('confirm_password')
        data.pop('submit')
        data['name'] = f"{data['first_name']} {data['last_name']}"
        data.pop('csrf_token')
        teacher_count = storage.count("Teacher") + 1
        data['id'] = f"schedu-teacher-{data['name'][:3]}-{teacher_count}".lower()
        data["date_of_birth"] = data["date_of_birth"].strftime('%d-%m-%Y')
        data['role'] = "teacher"
        teacher = Teacher(**data)
        teacher.save()
        flash(f'{data["name"]} has been registered. id: {data["id"]}, password: {pd}', 'success')
        response = make_response(redirect("/"))
        response.headers['Cache-Control'] = (
            'no-cache, no-store, must-revalidate')
        return response
    else:
        print(form.errors)
    return render_template('reg_teacher.html', form=form, user=current_user)


@app.route('/register/guardian', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def register_guardian():
    """Handle the guardian registration route"""
    form = GuardianRegForm()
    if form.validate_on_submit():
        data = form.data
        pd = data['password']
        data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        data.pop('confirm_password')
        data.pop('submit')
        data['name'] = f"{data['first_name']} {data['last_name']}"
        data.pop('csrf_token')
        data["date_of_birth"] = data["date_of_birth"].strftime('%d-%m-%Y')
        guardian_count = storage.count("Guardian") + 1
        data['id'] = f"schedu-guardian-{data['name'][:3]}-{guardian_count}".lower()
        data['role'] = "guardian"
        guardian = Guardian(**data)
        guardian.save()
        flash(f'{data["name"]} has been registered. id: {data["id"]}, password: {pd}', 'success')
        response = make_response(redirect("/"))
        response.headers['Cache-Control'] = (
            'no-cache, no-store, must-revalidate')
        return response
    else:
        print(form.errors)
    return render_template('reg_guardian.html', form=form, user=current_user)


# ----------------------------------------------------------------------------
