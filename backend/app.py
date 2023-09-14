from create_app import create_app, db
from flask_security import hash_password

app = create_app()
app.app_context().push()
db.create_all()


admin_role = app.security.datastore.find_or_create_role(
    name="admin", description="can create, delete, update shows and venues"
)

user_role = app.security.datastore.find_or_create_role(
    name="patron", description="can book tickets for shows"
)


if not app.security.datastore.find_user(email="admin@pixelshows.com"):
    app.security.datastore.create_user(
        username="admin",
        email="admin@pixelshows.com",
        password=hash_password("pixel123"),
        roles=[admin_role],
    )

db.session.commit()
if __name__ == "__main__":
    app.run(port=8000)
