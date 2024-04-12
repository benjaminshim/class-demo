"""
This module provides the glossary query form
"""

import forms.restaurant_form_filler as ff

from forms.restaurant_form_filler import FLD_NM  # for tests

STATE = 'state'

RESTAURANT_FORM_FLDS = [
    { 
        FLD_NM: 'state',
        ff.QSTN: 'state',
    },
]


def get_form() -> list:
    return RESTAURANT_FORM_FLDS


def get_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(RESTAURANT_FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(RESTAURANT_FORM_FLDS)


def main():
    # print(f'Form: {get_form()=}\n\n')
    print(f'Form: {get_form_descr()=}\n\n')
    # print(f'Field names: {get_fld_names()=}\n\n')


if __name__ == "__main__":
    main()
