import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.api import *
from flask_restful import Api
from flask_security import Security
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
db = db
api = Api()


def create_app():
    app = Flask(__name__)
    if os.getenv("ENV", "development") == "production":
        raise Exception("currently no production config is setup.")
    else:
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    # Adding Api Resources
    api.add_resource(Admin_Change_Password_API, "/api/changepassword/admin")
    api.add_resource(Admin_Save_Image_API, "/api/saveimage")
    api.add_resource(Admin_Get_Bookings_API, "/api/getbookings")
    api.add_resource(
        Admin_Venue_Type_API, "/api/venuetype", "/api/venuetype/<int:t_id>"
    )
    api.add_resource(Admin_Venue_API, "/api/venue", "/api/venue/<int:v_id>")
    api.add_resource(Admin_Tag_API, "/api/tag", "/api/tag/<string:tag_value>")
    api.add_resource(Admin_Shows_API, "/api/shows", "/api/shows/<int:s_id>")
    api.add_resource(
        User_Profile_API, "/api/createuserprofile", "/api/userprofile/<string:username>"
    )
    api.add_resource(User_Bookings_API, "/api/bookings", "/api/bookings/<int:ub_id>")
    api.add_resource(User_Venue_Reviews_API, "/api/venuereviews")
    api.add_resource(User_Show_Reviews_API, "/api/showreviews")
    api.add_resource(
        Public_Venue_API, "/api/publicvenue", "/api/publicvenue/<int:v_id>"
    )
    api.add_resource(Public_Venue_Type_API, "/api/getvenuetypes")
    api.add_resource(Public_Show_Tags_API, "/api/getshowtags")
    api.add_resource(Public_Show_API, "/api/getshows")
    api.add_resource(Public_Single_Show_API, "/api/getshow/<int:s_id>")
    api.add_resource(Public_Show_Search_API, "/api/searchshows")
    api.add_resource(Public_Venue_locations_API, "/api/getvenuelocations")
    app.security = Security(app, user_datastore)
    api.init_app(app)
    CORS(app)

    return app
