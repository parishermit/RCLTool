from django.db import models

# Create your models here.
from django.db import models


class Span(models.Model):
    timestamp = models.CharField(max_length=100, default="")
    cmdb_id = models.CharField(max_length=100, default="")
    span_id = models.CharField(max_length=100, default="")
    trace_id = models.CharField(max_length=100, default="")
    duration = models.IntegerField(default=0)
    type = models.CharField(max_length=100, default="")
    status_code = models.CharField(max_length=100, default="0")
    operation_name = models.CharField(max_length=200, default="")
    parent_span = models.CharField(max_length=100, default="")


class RCLLabel(models.Model):
    trace_id = models.CharField(max_length=100, default="")
    operation_name = models.CharField(max_length=200, default="")
    cmdb_id = models.CharField(max_length=100, default="")
