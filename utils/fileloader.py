# -*- coding: utf-8 -*-
import logging


def load_file_to_editor(filename, editor):
    try:
        text = open(filename).read()
        editor.clear()
        editor.insertPlainText(text)
    except Exception as e:
        logging.exception(e)
    finally:
        pass
