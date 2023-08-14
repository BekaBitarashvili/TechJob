from app import create_app, db

app = create_app()


def create_database():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
