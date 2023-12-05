# Create your views here.
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
from datetime import datetime
import json
import time
from trace_app.trace_api import get_span_list


# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 GET
@require_http_methods(['GET'])
class traceView(View):
    def get_span_list(request):
        if request.method == 'GET':
            trace_id = request.GET.get('trace_id')
            # 凭借trace_id去数据库查询数据并返回list
            data = get_span_list(trace_id)
            return JsonResponse(data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Invalid API request method.'}, status=400)