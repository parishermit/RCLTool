from datetime import datetime, timedelta
import re
import pytz
import pandas as pd
import time
import json
import sys
import pathlib
trace_app_path = pathlib.Path(__file__).parent
sys.path.append(trace_app_path)

def get_span_list(trace_id):
    span_list = []
    with open(trace_app_path.joinpath('span_list.json'), 'r') as json_file:
        span_list = json.load(json_file)
    return span_list
