"""Basic mapping in order to manage application terms
with multi language support

Before using other language you must set
"""
import os

LANGUAGE = os.environ.get("SELENIUM-ODOO-PAGE-LANGUAGE", "en")
TERMS = {"Create and Edit...": "Créer et modifier..."}


def get_term(label):
    if LANGUAGE == "en":
        return label
    return TERMS[LANGUAGE][label]
