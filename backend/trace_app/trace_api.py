from datetime import datetime, timedelta
import re
import pytz
import pandas as pd
import time
import json
import sys
import pathlib
import os
import csv
import pymysql
from trace_app.models import Span


trace_app_path = pathlib.Path(__file__).parent
sys.path.append(trace_app_path)


def get_span_list(trace_id):
    span_list = Span.objects.filter(trace_id=trace_id).values()
    print(list(span_list))
    return list(span_list)
