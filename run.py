from api import create_app
import os
import config

if __name__ == '__main__':
    app = create_app(config.DevConfig)
    app.run()