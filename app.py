from api import create_app

app = create_app()

if __name__ == '__main__':
    app.config.from_prefixed_env()
    app.config["APP_PORT"]
    app.config["APP_DEBUG"]
    app.run()
