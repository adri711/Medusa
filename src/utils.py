from flask import Flask, render_template, url_for, flash, redirect, request, jsonify, g, session
from src.models import User
from src import constants

def is_user_logged():
    if 'user_id' in session:
        if User.query.filter_by(id=session['user_id']).first():
            return True

def get_user_id():
    if 'user_id' in session:
        return session['user_id']

def get_user_level(xp):
    curr_level = 0
    for key in constants.USER_LEVELS:
        if constants.USER_LEVELS[key] > xp:
            break
        curr_level = key
    return curr_level