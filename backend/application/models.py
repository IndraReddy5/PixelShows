from .database import db
from flask_security import UserMixin, RoleMixin


class Roles(db.Model, RoleMixin):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id"))


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    user_image = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String, unique=True, nullable=False)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    active = db.Column(db.String)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    roles = db.relationship(
        "Roles",
        secondary="roles_users",
        backref=db.backref("users_roles", lazy="dynamic"),
        viewonly=True,
    )


class VenueTypes(db.Model):
    __tablename__ = "venue_types"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    type = db.Column(db.String)
    venue_charges = db.Column(db.Float)


class Venues(db.Model):
    __tablename__ = "venues"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    venue_name = db.Column(db.String(160))
    seating_capacity = db.Column(db.Integer)
    venue_image = db.Column(db.String)
    venue_address = db.Column(db.String(500))
    venue_city = db.Column(db.String(120))
    venue_type = db.Column(db.Integer, db.ForeignKey("venue_types.id"))
    venue_shows = db.relationship("ShowVenues", foreign_keys="ShowVenues.venue_id", lazy="dynamic", backref=db.backref("venue_info"))


class Shows(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    show_name = db.Column(db.String(240))
    ticket_price = db.Column(db.Float)
    show_description = db.Column(db.String(500))
    show_poster = db.Column(db.String(500))
    show_timing = db.Column(db.DateTime)
    show_venues = db.relationship("ShowVenues", foreign_keys="ShowVenues.show_id", lazy="dynamic", backref=db.backref("show_info"))
    show_tags = db.relationship("ShowTags", foreign_keys="ShowTags.show_id", lazy="dynamic")


class Tags(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    tag_name = db.Column(db.String(60))
    tag_rel = db.relationship("ShowTags", foreign_keys="ShowTags.tag_id", lazy="dynamic", backref = db.backref("tag_info"))


class ShowTags(db.Model):
    __tablename__ = "show_tags"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    

class ShowVenues(db.Model):
    __tablename__ = "show_venues"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"))
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"))
    tickets_sold = db.Column(db.Integer)
    user_bookings = db.relationship("UserBookings", foreign_keys="UserBookings.show_venues_id", lazy="dynamic", backref=db.backref("show_info_user"))


class ShowReviews(db.Model):
    __tablename__ = "show_reviews"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    review_text = db.Column(db.String(500))
    rating = db.Column(db.Float)


class UserBookings(db.Model):
    __tablename__ = "user_bookings"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    show_venues_id = db.Column(db.Integer, db.ForeignKey("show_venues.id"))
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"))
    booking_date = db.Column(db.DateTime)
    booking_price = db.Column(db.Float)
    no_of_tickets = db.Column(db.Integer)
    payment_status = db.Column(db.String(60))
    show_status = db.Column(db.String(60))


class VenueReviews(db.Model):
    __tablename__ = "venue_reviews"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    review_text = db.Column(db.String(500))
    rating = db.Column(db.Float)

class ArchivedShows(db.Model):
    __tablename__ = "archived_shows"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"))
    show_name = db.Column(db.String(240))