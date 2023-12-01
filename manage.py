# flask
from app.config.es_config import es_init
from app import create_app


es_init()
app = create_app()


# test app run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
