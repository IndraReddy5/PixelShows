from datetime import datetime as dt
from flask_restful import Resource, request

from application.database import db
from application.models import *
from application.errors import *

from flask_security import (
    auth_required,
    SQLAlchemyUserDatastore,
    hash_password,
    roles_required,
)
from application.utils import *

import os
import json


user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)


### JS Console Login API Fetch Request Test Code
"""
let data = {'username':'admin','password':'pixel123'}
fetch("http://127.0.0.1:8000/login?include_auth_token",
{headers:{'content-type': 'application/json'},
'method':'POST','body':JSON.stringify(data)})
.then(response => response.json())
.then(data => console.log(data))
"""


### Admin APIs
class Admin_Change_Password_API(Resource):
    @roles_required("admin")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        u_obj = Users.query.filter_by(username=form_data.get("username")).first()
        if u_obj:
            u_obj.password = hash_password(form_data.get("password"))
            db.session.commit()
            return "Password Changed", 200
        else:
            raise NotFound(status_code=404, error_message="User not found")


class Admin_Save_Image_API(Resource):
    @roles_required("admin")
    @auth_required("token")
    def post(self, filename):
        image = request.files.get("file")
        location = os.path.join(os.getcwd(), "..", "static", filename)
        image.save(location)
        return "Image Saved", 200


class Admin_Get_Bookings_API(Resource):
    @roles_required("admin")
    @auth_required("token")
    def get(self):
        ub_objs = UserBookings.query.all()
        if ub_objs:
            booking_data = {
                "bookings": [
                    {
                        "username": ub.user_info.username,
                        "email": ub.user_info.email,
                        "role": ub.user_info.roles.name,
                        "last_login_at": ub.user_info.last_login_at,
                        "show_name": ub.show_info_user.show_info.show_name,
                        "venue_name": ub.show_info_user.venue_info.venue_name,
                        "show_timing": ub.show_info_user.show_info.show_timing,
                        "booking_date": ub.booking_date,
                        "ticket_price": ub.booking_price,
                        "no_of_tickets_booked": ub.no_of_tickets,
                        "payment_status": ub.payment_status,
                        "show_status": ub.show_status,
                    }
                    for ub in ub_objs.user_bookings
                ]
            }

        else:
            return json.dumps({"bookings": []}), 200


class Admin_Venue_Type_API(Resource):
    @roles_required("admin")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        v_obj = VenueTypes()
        v_obj.type = form_data.get("type")
        v_obj.venue_charges = form_data.get("venue_charges")
        db.session.add(v_obj)
        db.session.commit()
        return "Venue Type Added", 200

    @roles_required("admin")
    @auth_required("token")
    def delete(self, t_id):
        v_obj = VenueTypes.query.filter_by(id=t_id).first()
        if v_obj:
            db.session.delete(v_obj)
            db.session.commit()
            return "Venue Type Deleted", 200
        else:
            raise NotFound(status_code=404, error_message="Venue Type not found")


class Admin_Venue_API(Resource):
    @roles_required("admin")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        v_obj = Venues()
        v_obj.venue_name = form_data.get("venue_name")
        v_obj.seating_capacity = form_data.get("seating_capacity")
        v_obj.venue_image = form_data.get("venue_image")
        v_obj.venue_address = form_data.get("venue_address")
        v_obj.venue_city = form_data.get("venue_city")
        v_obj.venue_type = form_data.get("venue_type")
        db.session.add(v_obj)
        db.session.commit()
        return "Venue Added", 200

    @roles_required("admin")
    @auth_required("token")
    def put(self, v_id):
        form_data = request.form()
        v_obj = Venues.query.filter_by(id=v_id).first()
        if v_obj:
            v_obj.venue_name = form_data.get("venue_name")
            v_obj.seating_capacity = form_data.get("seating_capacity")
            v_obj.venue_image = form_data.get("venue_image")
            v_obj.venue_address = form_data.get("venue_address")
            v_obj.venue_city = form_data.get("venue_city")
            v_obj.venue_type = form_data.get("venue_type")
            db.session.commit()
            return "Venue Updated", 200
        else:
            raise NotFound(status_code=404, error_message="Venue not found")

    @roles_required("admin")
    @auth_required("token")
    def delete(self, v_id):
        v_obj = Venues.query.filter_by(id=v_id).first()
        if v_obj:
            # handling shows in ShowVenues table (todo: handle tickets sold)
            sv_obj = ShowVenues.query.filter_by(venue_id=v_id).all()
            for sv in sv_obj:
                # handling userbookings
                ub_obj = UserBookings.query.filter_by(show_venue_id=sv.id).all()
                for ub in ub_obj:
                    if (
                        dt.strptime(sv.show_info.show_timing, "%m/%d/%y %H:%M:%S")
                        > dt.now()
                    ):
                        ub.payment_status = "Refunded"
                        ub.show_status = "Cancelled"
                # deleting show and moving to archived shows table
                ar_obj = ArchivedShows()
                ar_obj.show_id = sv.show_info.id
                ar_obj.show_name = sv.show_info.show_name
                s_obj = Shows.query.filter_by(id=sv.show_info.id).first()
                db.session.delete(s_obj)
                db.session.delete(sv)
            # deleting venue
            db.session.delete(v_obj)
            db.session.commit()
            return "Venue Deleted", 200
        else:
            raise NotFound(status_code=404, error_message="Venue not found")


class Admin_Tag_API(Resource):
    @roles_required("admin")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        t_obj = Tags()
        t_obj.tag_name = form_data.get("tag_name")
        db.session.add(t_obj)
        db.session.commit()
        return "Tag Added", 200

    @roles_required("admin")
    @auth_required("token")
    def delete(self, tag_value):
        t_obj = Tags.query.filter_by(tag_name=tag_value).first()
        if t_obj:
            db.session.delete(t_obj)
            db.session.commit()
            return "Tag Deleted", 200
        else:
            raise NotFound(status_code=404, error_message="Tag not found")


class Admin_Shows_API(Resource):
    # add/ modify new/old shows in Shows table, ShowTags table, ShowVenues table and UserBookings table
    @roles_required("admin")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        s_obj = Shows()
        s_obj.show_name = form_data.get("show_name")
        s_obj.ticket_price = form_data.get("ticket_price")
        s_obj.show_description = form_data.get("show_description")
        s_obj.show_poster = form_data.get("show_poster")
        s_obj.show_timing = form_data.get("show_timing")
        db.session.add(s_obj)
        db.session.commit()
        show_venues_list = list(form_data.get("show_venues"))
        show_tags_list = list(form_data.get("show_tags"))
        for venue in show_venues_list:
            sv_obj = ShowVenues()
            sv_obj.show_id = s_obj.id
            sv_obj.venue_id = venue
            db.session.add(sv_obj)
            db.session.commit()
        for tag in show_tags_list:
            st_obj = ShowTags()
            st_obj.show_id = s_obj.id
            st_obj.tag_id = tag
            db.session.add(st_obj)
            db.session.commit()
        return "Show Added", 200

    @roles_required("admin")
    @auth_required("token")
    def delete(self):
        form_data = request.get_json()
        s_obj = Shows.query.filter_by(id=form_data.get("show_id")).first()
        if s_obj:
            # delete show from ShowVenues table and ShowTags table (todo: handle tickets sold)
            sv_obj = ShowVenues.query.filter_by(show_id=form_data.get("show_id")).all()
            for sv in sv_obj:
                # handling userbookings
                ub_obj = UserBookings.query.filter_by(show_venue_id=sv.id).all()
                for ub in ub_obj:
                    if (
                        dt.strptime(sv.show_info.show_timing, "%m/%d/%y %H:%M:%S")
                        > dt.now()
                    ):
                        ub.payment_status = "Refunded"
                        ub.show_status = "Cancelled"
                        db.session.commit()
                db.session.delete(sv)
                db.session.commit()
            st_obj = ShowTags.query.filter_by(show_id=form_data.get("show_id")).all()
            for st in st_obj:
                db.session.delete(st)
                db.session.commit()

            # moving the deleted show to ArchivedShows table
            ds_obj = ArchivedShows()
            ds_obj.show_name = s_obj.show_name

            # finally deleting it from shows table
            db.session.delete(s_obj)
            db.session.commit()
            return "Show Deleted", 200
        else:
            raise NotFound(status_code=404, error_message="Show not found")

    @roles_required("admin")
    @auth_required("token")
    def put(self, s_id):
        form_data = request.get_json()
        s_obj = Shows.query.filter_by(id=s_id).first()
        s_obj.show_name = form_data.get("show_name")
        s_obj.ticket_price = form_data.get("ticket_price")
        s_obj.show_description = form_data.get("show_description")
        s_obj.show_poster = form_data.get("show_poster")
        s_obj.show_timing = form_data.get("show_timing")
        db.session.add(s_obj)
        db.session.commit()

        # adding these loops to make the changes to previous show_venues and show_tags
        show_venues_delete_list = list(form_data.get("show_venues_delete"))
        show_tags_delete_list = list(form_data.get("show_tags_delete"))
        show_venues_add_list = list(form_data.get("show_venues_add"))
        show_tags_add_list = list(form_data.get("show_tags_add"))
        for venue in show_venues_delete_list:
            sv_obj = ShowVenues.query.filter_by(show_id=s_id, venue_id=venue).first()
            db.session.delete(sv_obj)
            db.session.commit()
        for tag in show_tags_delete_list:
            st_obj = ShowTags.query.filter_by(show_id=s_id, tag_id=tag).first()
            db.session.delete(st_obj)
            db.session.commit()
        for venue in show_venues_add_list:
            sv_obj = ShowVenues()
            sv_obj.show_id = s_id
            sv_obj.venue_id = venue
            db.session.add(sv_obj)
            db.session.commit()
        for tag in show_tags_add_list:
            st_obj = ShowTags()
            st_obj.show_id = s_id
            st_obj.tag_id = tag
            db.session.add(st_obj)
            db.session.commit()
        return "Show Modified", 200


### Patron APIs
class User_Profile_API(Resource):
    @roles_required("patron")
    @auth_required("token")
    def get(self, username):
        u_obj = Users.query.filter_by(username=username).first()
        if u_obj:
            user_data = {
                "username": u_obj.username,
                "email": u_obj.email,
                "role": u_obj.roles.name,
                "last_login_at": u_obj.last_login_at,
                "past_bookings": {
                    {
                        "show_name": ub.show_info_user.show_info.show_name,
                        "venue_name": ub.show_info_user.venue_info.venue_name,
                        "show_timing": ub.show_info_user.show_info.show_timing,
                        "booking_date": ub.booking_date,
                        "ticket_price": ub.booking_price,
                        "no_of_tickets_booked": ub.no_of_tickets,
                        "payment_status": ub.payment_status,
                        "show_status": ub.show_status,
                    }
                    for ub in u_obj.user_bookings
                },
            }
            return json.dumps(user_data), 200
        else:
            raise NotFound(status_code=404, error_message="User not found")

    def delete(self, username):
        u_obj = Users.query.filter_by(username=username).first()
        if u_obj:
            db.session.delete(u_obj)
            db.session.commit()
            return f"{username} profile deleted", 200
        else:
            raise NotFound(status_code=404, error_message="User not found")

    @roles_required("patron")
    @auth_required("token")
    def put(self, username):
        u_obj = Users.query.filter_by(username=username).first()
        if u_obj:
            form_data = request.get_json()
            u_obj.username = username
            u_obj.email = form_data.get("email")
            u_obj.password = hash_password(form_data.get("password"))

            return "User Profile Updated", 200
        else:
            raise NotFound(status_code=404, error_message="User not found")

    @roles_required("patron")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        username = form_data.get("username")
        email = form_data.get("email")
        if (
            not Users.query.filter_by(username=username).first()
            and not Users.query.filter_by(email=email).first()
        ):
            user_datastore.create_user(
                username=form_data.get("username"),
                password=hash_password(form_data.get("password")),
                email=form_data.get("email"),
                roles=["patron"],
            )
            db.session.commit()
            return "user created", 200
        else:
            raise ValidationError(
                status_code=400,
                error_code="user_exists",
                error_message="username already exists.",
            )


class User_Bookings_API(Resource):
    @roles_required("patron")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        ub_obj = UserBookings()
        ub_obj.user_id = form_data.get("username")
        ub_obj.show_id = form_data.get("show_id")
        ub_obj.show_venues_id = form_data.get("show_venues_id")
        ub_obj.booking_date = dt.now().strftime("%m/%d/%y %H:%M:%S")
        ub_obj.booking_price = form_data.get("booking_price")
        ub_obj.no_of_tickets = form_data.get("no_of_tickets")
        ub_obj.payment_status = "Payment_Completed"
        ub_obj.show_status = "Active"

        db.session.add(ub_obj)
        db.session.commit()
        return "Ticket Booked", 200

    # when user cancels the booking
    @roles_required("patron")
    @auth_required("token")
    def put(self, ub_id):
        ub_obj = UserBookings.query.filter_by(id=ub_id).first()
        if ub_obj:
            ub_obj.payement_status = "Refunded"
            db.session.commit()
            return "Ticket Cancelled", 200
        else:
            raise NotFound(status_code=404, error_message="Ticket not found")


class User_Venue_Reviews_API(Resource):
    @roles_required("patron")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        vr_obj = VenueReviews()
        vr_obj.venue_id = form_data.get("venue_id")
        vr_obj.user_id = form_data.get("user_id")
        vr_obj.review_text = form_data.get("review_text")
        vr_obj.rating = form_data.get("rating")

        db.session.add(vr_obj)
        db.session.commit()

        return "Venue Review Added", 200


class User_Show_Reviews_API(Resource):
    @roles_required("patron")
    @auth_required("token")
    def post(self):
        form_data = request.get_json()
        sr_obj = ShowReviews()
        sr_obj.show_id = form_data.get("show_id")
        sr_obj.user_id = form_data.get("user_id")
        sr_obj.review_text = form_data.get("review_text")
        sr_obj.rating = form_data.get("rating")

        db.session.add(sr_obj)
        db.session.commit()

        return "Show Review Added", 200


### Public APIs
class Public_Venue_API(Resource):
    @auth_required("token")
    def get(self):
        # list out all venues
        v_obj = Venues.query.all()
        if v_obj:
            return (
                json.dumps(
                    {
                        "venues": [
                            {
                                v.venue_name: {
                                    "seating_capacity": v.seating_capacity,
                                    "venue_image": v.venue_image,
                                    "venue_address": v.venue_address,
                                    "venue_city": v.venue_city,
                                    "venue_rating": average(
                                        [
                                            e.rating
                                            for e in VenueReviews.query.filter_by(
                                                venue_id=v.id
                                            ).all()
                                        ]
                                    ),
                                    "venue_type": VenueTypes.query.filter_by(
                                        id=v.venue_type
                                    )
                                    .first()
                                    .type,
                                    "venue_shows": sort_by_time(
                                        {
                                            s.show_info.show_name: {
                                                "ticket_price": s.show_info.ticket_price
                                                + VenueTypes.query.filter_by(
                                                    venue_id=v.venue_type
                                                )
                                                .first()
                                                .venue_charges,
                                                "show_description": s.show_info.show_description,
                                                "show_poster": s.show_info.show_poster,
                                                "show_timing": s.show_info.show_timing,
                                                "show_tags": [
                                                    (st.tag_id, st.tag_info.tag_name)
                                                    for st in s.show_info.show_tags
                                                ],
                                                "show_rating": average(
                                                    [
                                                        e.rating
                                                        for e in ShowReviews.query.filter_by(
                                                            show_id=s.show_id
                                                        ).all()
                                                    ]
                                                ),
                                                "tickets_sold": s.tickets_sold,
                                            }
                                            for s in v.venue_shows
                                        }
                                    ),
                                }
                            }
                            for v in v_obj
                        ]
                    }
                ),
                200,
            )
        else:
            return json.dumps({"venues": []}), 200

    @roles_required("admin")
    @auth_required("token")
    def get(self, v_id):
        v_obj = Venues.query.filter_by(id=v_id).first()
        if v_obj:
            return (
                json.dumps(
                    {
                        v_obj.venue_name: {
                            "seating_capacity": v_obj.seating_capacity,
                            "venue_image": v_obj.venue_image,
                            "venue_address": v_obj.venue_address,
                            "venue_city": v_obj.venue_city,
                            "venue_rating": average(
                                [
                                    e.rating
                                    for e in VenueReviews.query.filter_by(
                                        venue_id=v_obj.id
                                    ).all()
                                ]
                            ),
                            "venue_type": VenueTypes.query.filter_by(
                                id=v_obj.venue_type
                            )
                            .first()
                            .type,
                            "venue_shows": sort_by_time(
                                {
                                    s.show_info.show_name: {
                                        "ticket_price": s.show_info.ticket_price
                                        + +VenueTypes.query.filter_by(
                                            venue_id=v_obj.venue_type
                                        )
                                        .first()
                                        .venue_charges,
                                        "show_description": s.show_info.show_description,
                                        "show_poster": s.show_info.show_poster,
                                        "show_timing": s.show_info.show_timing,
                                        "show_tags": [
                                            (st.tag_id, st.tag_info.tag_name)
                                            for st in s.show_info.show_tags
                                        ],
                                        "show_rating": average(
                                            [
                                                e.rating
                                                for e in ShowReviews.query.filter_by(
                                                    show_id=s.show_id
                                                ).all()
                                            ]
                                        ),
                                        "tickets_sold": s.tickets_sold,
                                    }
                                    for s in v_obj.venue_shows
                                }
                            ),
                        }
                    }
                ),
                200,
            )
        else:
            raise NotFound(status_code=404, error_message="Venue not found")


class Public_Venue_Type_API(Resource):
    @auth_required("token")
    def get(self):
        # list out all venue types
        v_obj = VenueTypes.query.all()
        if v_obj:
            return (
                json.dumps(
                    {"venue_types": [(v.id, v.type, v.venue_charges) for v in v_obj]}
                ),
                200,
            )
        else:
            return json.dumps({"venue_types": []}), 200


class Public_Show_Tags_API(Resource):
    @auth_required("token")
    def get(self, s_id):
        # list out all tags for a show
        st_obj = ShowTags.query.filter_by(show_id=s_id).all()
        if st_obj:
            return json.dumps({"show_tags": [st.tag_name for st in st_obj]}), 200
        else:
            return json.dumps({"show_tags": []}), 200


class Public_Show_API(Resource):
    @auth_required("token")
    def get(self):
        s_objs = Shows.query.all()
        if s_objs:
            return (
                json.dumps(
                    {
                        "shows": sort_by_time(
                            {
                                s.show_name: {
                                    "ticket_price": s.ticket_price
                                    + VenueTypes.query.filter_by(
                                        venue_id=s.show_venues.venue_info.venue_type
                                    )
                                    .first()
                                    .venue_charges,
                                    "show_description": s.show_description,
                                    "show_poster": s.show_poster,
                                    "show_timing": s.show_timing,
                                    "show_venues": [
                                        (
                                            sv.venue_id,
                                            sv.venue_info.venue_name,
                                            sv.tickets_sold,
                                        )
                                        for sv in s.show_venues
                                    ],
                                    "show_tags": [
                                        (st.tag_id, st.tag_info.tag_name)
                                        for st in s.show_tags
                                    ],
                                    "show_rating": average(
                                        [
                                            e.rating
                                            for e in ShowReviews.query.filter_by(
                                                show_id=s.id
                                            ).all()
                                        ]
                                    ),
                                }
                                for s in s_objs
                            }
                        )
                    }
                ),
                200,
            )
        else:
            return json.dumps({"shows": []}), 200

    @auth_required("token")
    def get(self, s_id):
        s_obj = Shows.query.filter_by(id=s_id).first()
        if s_obj:
            return (
                json.dumps(
                    {
                        s_obj.show_name: {
                            "ticket_price": s_obj.ticket_price
                            + VenueTypes.query.filter_by(
                                venue_id=s_obj.show_venues.venue_info.venue_type
                            )
                            .first()
                            .venue_charges,
                            "show_description": s_obj.show_description,
                            "show_poster": s_obj.show_poster,
                            "show_timing": s_obj.show_timing,
                            "show_venues": [
                                (sv.venue_id, sv.venue_info.venue_name, sv.tickets_sold)
                                for sv in s_obj.show_venues
                            ],
                            "show_tags": [
                                (st.tag_id, st.tag_info.tag_name)
                                for st in s_obj.show_tags
                            ],
                            "show_rating": average(
                                [
                                    e.rating
                                    for e in ShowReviews.query.filter_by(
                                        show_id=s_obj.id
                                    ).all()
                                ]
                            ),
                        }
                    }
                ),
                200,
            )
        else:
            raise NotFound(status_code=404, error_message="Show not found")


class Public_Show_Search_API(Resource):
    @auth_required("token")
    def get(self, location=None, tag=None):
        if location:
            v_objs = Venues.query.filter_by(venue_city=location).all()
            v_ids = [v.id for v in v_objs]
        if location and tag:
            s_objs = Shows.query.filter(
                Shows.show_venues.any(venue_id=v_ids),
                Shows.show_tags.any(tag_name=tag),
            ).all()
        elif not location and tag:
            s_objs = Shows.query.filter(Shows.show_tags.any(tag_name=tag)).all()
        else:
            s_objs = Shows.query.filter(Shows.show_venues.any(venue_id=v_ids)).all()

            if s_objs:
                return (
                    json.dumps(
                        {
                            "shows": sort_by_time(
                                {
                                    s.show_name: {
                                        "ticket_price": s.ticket_price
                                        + VenueTypes.query.filter_by(
                                            venue_id=s.show_venues.venue_info.venue_type
                                        )
                                        .first()
                                        .venue_charges,
                                        "show_description": s.show_description,
                                        "show_poster": s.show_poster,
                                        "show_timing": s.show_timing,
                                        "show_venues": [
                                            (
                                                sv.venue_id,
                                                sv.venue_info.venue_name,
                                                sv.tickets_sold,
                                            )
                                            for sv in s.show_venues
                                        ],
                                        "show_tags": [
                                            (st.tag_id, st.tag_info.tag_name)
                                            for st in s.show_tags
                                        ],
                                        "show_rating": average(
                                            [
                                                e.rating
                                                for e in ShowReviews.query.filter_by(
                                                    show_id=s.id
                                                ).all()
                                            ]
                                        ),
                                    }
                                    for s in s_objs
                                }
                            )
                        }
                    ),
                    200,
                )
            else:
                return json.dumps({"shows": []}), 200
