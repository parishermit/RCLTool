# Create your views here.
import os.path

from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Span, RCLLabel
import pandas as pd
from datetime import datetime
import json
import time
from trace_app.trace_api import get_span_list
import csv


# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 GET
@require_http_methods(['GET'])
class TraceView(View):
    def get_span_list(request):
        if request.method == 'GET':
            trace_id = request.GET.get('trace_id')
            # 凭借trace_id去数据库查询数据并返回list
            data = get_span_list(trace_id)
            return JsonResponse(data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Invalid API request method.'}, status=400)


@require_http_methods(['POST'])
def get_data(request):
    try:
        span_name_list = Span.objects.values_list()
        filepath = request.POST.get('filepath')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                csv_data = []
                for row in reader:
                    if tuple(row[0]) in span_name_list:
                        csv_data.append(row)
                Span.objects.bulk_create(csv_data)
                return JsonResponse({'isSuccess': 'ok', 'info': '文件数据导入成功！'}, safe=False, status=200)
        else:
            return JsonResponse({'isSuccess': 'false', 'info': '文件路径不存在，导入失败!'}, safe=False, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"isSuccess": "error", 'info': '请检查程序!'}, status=500)
