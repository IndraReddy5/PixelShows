from flask_restful import Resource, request
from flask_restful import fields, marshal_with

from application.database import db
from application.models import Users, Roles
from application.errors import *

from flask_security import auth_required, SQLAlchemyUserDatastore, hash_password

import os
from datetime import datetime as dt


user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)

class User_profile_API(Resource):

    output = {"username": fields.String, "first_name": fields.String,
              "last_name": fields.String, "profile_image": fields.String, "email": fields.String,
              "followers_count": fields.Integer, "following": fields.Integer, "total_posts": fields.Integer}
    
    @auth_required('token')
    @marshal_with(output)
    def get(self, username):
        u_obj = Users.query.filter_by(username=username).first()
        if u_obj:
            u_obj.followers_count = len(u_obj.followed)
            u_obj.following = len(u_obj.follower)
            u_obj.total_posts = len(u_obj.posts_rel)
            return u_obj, 200
        else:
            raise NotFound(status_code=404, error_message="User not found")

    def delete(self, username):
        u_obj = Users.query.filter_by(username=username).first()
        u_p_obj = Users.query.filter_by(username=username).first()
        if u_obj and u_p_obj:
            for post in u_p_obj.posts_rel:
                if post.post_image:
                    file_path = f'static/post_images/{post.author_name}_' + \
                        post.title + '_' + post.post_image
                    print(file_path)
                    cmd = 'rm ' + f"'{file_path}'"
                    os.system(cmd)
            db.session.delete(u_obj)
            db.session.delete(u_p_obj)
            # profile pic to be deleted
            file_path = f'static/profile_images/{username}_' + \
                u_p_obj.profile_image
            cmd = 'rm ' + f'{file_path}'
            os.system(cmd)
            db.session.commit()
            return f"{username} profile deleted", 200
        else:
            raise NotFound(status_code=404, error_message="User not found")

    @marshal_with(output)
    def put(self, username):
        u_obj = Users.query.filter_by(username=username).first()
        u_p_obj = Users.query.filter_by(username=username).first()
        if u_p_obj and u_obj:
            form_data = request.get_json()
            if form_data.get("profile_image"):
                file_path = f'static/profile_images/{username}_' + \
                    u_p_obj.profile_image
                cmd = 'rm ' + f"'{file_path}'"
                os.system(cmd)
                u_obj.profile_image = form_data.get("profile_image")
                u_p_obj.profile_image = form_data.get("profile_image")
            u_p_obj.first_name = form_data.get("first_name")
            u_p_obj.last_name = form_data.get("last_name")
            u_p_obj.email = form_data.get("email")
            u_obj.email = form_data.get("email")
            u_obj.password = hash_password(form_data.get("password"))
            db.session.commit()
            u_p_obj.followers_count = len(u_p_obj.followed)
            u_p_obj.following = len(u_p_obj.follower)
            u_p_obj.total_posts = len(u_p_obj.posts_rel)

            return u_p_obj, 200
        else:
            raise NotFound(status_code=404, error_message="User not found")

    @marshal_with(output)
    def post(self):
        form_data = request.get_json()
        username = form_data.get("username")
        if not Users.query.filter_by(username=username).first():
            if username:
                u_obj = Users()
                u = user_datastore.create_user(username=form_data.get("username"), password=hash_password(form_data.get(
                    "password")), email=form_data.get("email"), profile_image=form_data.get("profile_image"))
                u_obj.username = form_data.get("username")
                u_obj.first_name = form_data.get("first_name")
                u_obj.last_name = form_data.get("last_name")
                u_obj.email = form_data.get("email")
                u_obj.profile_image = form_data.get("profile_image")
                db.session.add(u_obj)
                db.session.commit()
                u_obj.followers_count = 0
                u_obj.following = 0
                u_obj.total_posts = 0
                return u_obj, 200
            else:
                raise ValidationError(
                    status_code=400, error_code="user_2", error_message="username not given.")
        else:
            raise ValidationError(
                status_code=400, error_code="user_1", error_message="username already exists.")