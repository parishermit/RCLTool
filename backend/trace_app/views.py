# Create your views here.
import os.path

from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Span, RCLLabel
from trace_app.trace_api import get_span_list,get_trace_list
import csv
import json


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
    def get_trace_list(request):
        if request.method == 'GET':
            data = get_trace_list()
            return JsonResponse(data, safe=False, status=200)
        else:
            return JsonResponse({'error': 'Invalid API request method.'}, status=400)
    def get_nodes_and_edges(request):
        if request.method == 'GET':
            trace_id = request.GET.get('trace_id')
            # 凭借trace_id去数据库查询数据并返回list
            data = get_span_list(trace_id)
            nodes=[]
            edges=[]
            for span in data:
                node={"shape": 'circle'}
                edge={}
                node['id']=span['span_id']
                node['duration']=span['duration']
                node['label']=span['operation_name'].split('/')[-1]
                edge['from']=span['parent_span']
                edge['to']=span['span_id']
                nodes.append(node)
                edges.append(edge)
                
            return JsonResponse([nodes,edges], safe=False, status=200)
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
        return JsonResponse({'isSuccess': 'error', 'info': '请检查程序!'}, status=500)


@require_http_methods(['POST'])
def get_root_cause(request):
    try:
        data = json.loads(request.body)
        trace_id = data.get("trace_id", "")
        operation_name = data.get("operation_name", "")
        cmdb_id = data.get("cmdb_id", "")
        if RCLLabel.objects.filter(trace_id=trace_id).exists():
            return JsonResponse({'isSuccess': 'false', 'info': '此调用链已标注!'}, safe=False, status=400)
        else:
            rcl_info = RCLLabel(
                trace_id=trace_id,
                operation_name=operation_name,
                cmdb_id=cmdb_id
            )
            rcl_info.save()
            if RCLLabel.objects.filter(trace_id=trace_id).exists():
                return JsonResponse({'isSuccess': 'ok', 'info': '调用链标注成功!'}, safe=False, status=200)
            else:
                return JsonResponse({'isSuccess': 'false', 'info': '标注失败!'}, safe=False, status=401)
    except Exception as e:
        print(e)
        return JsonResponse({'isSuccess': 'error', 'info': '请检查程序!'}, status=500)
