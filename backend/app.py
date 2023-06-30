from create_app import create_app, db
from flask_security import hash_password
from application.models import Roles

app = create_app()
app.app_context().push()
db.create_all()

if not app.security.datastore.find_role("admin"):
    app.security.datastore.create_role(
        name="admin", description="admin_role, can create shows and venues"
    )


if not app.security.datastore.find_user(email="admin@pixelshows.com"):
    app.security.datastore.create_user(
        username="admin",
        email="admin@pixelshows.com",
        password=hash_password("pixel123"),
        user_image="admin_image.jpg",
        Roles=["admin"],
    )

if __name__ == "__main__":
    app.run(port=8000)
