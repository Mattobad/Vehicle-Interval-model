from app.app import create_app
from app.config import config

application = create_app(config_object=config.DevelopmentConfig)

def run_app():
    application.run(host='0.0.0.0')

if __name__ =='__main__':
    run_app()