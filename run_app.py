# -*- coding: utf-8 -*-

import time
from app import App


if __name__ == '__main__':

    main_app = App()

    try:
        main_app.start()

        while True:
            main_app.loop()
            time.sleep(1)

    except Exception as ex:
        print(ex)