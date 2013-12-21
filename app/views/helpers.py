from jinja2 import Markup
import datetime
from app.controllers import utils


def datetime(date, fmt='%x'):
    return date.strftime(fmt)

def human_time(date):
    return utils.pretty_date(date)

def tz_time(date):
    return utils.iso_date(date)