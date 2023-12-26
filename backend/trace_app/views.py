# Create your views here.
import os.path

from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Span, RCLLabel
from trace_app.trace_api import get_span_list, get_trace_list
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
            nodes = []
            edges = []
            for span in data:
                node = {"shape": 'circle'}
                edge = {}
                node['id'] = span['span_id']
                node['duration'] = span['duration']
                node['label'] = span['operation_name'].split('/')[-1]
                if span['label']==1:
                    node['color']='orange'
                    edge['color']='red'
                elif span['label']==2:
                    node['color']='red'
                    edge['color']='red'
                edge['from'] = span['parent_span']
                edge['to'] = span['span_id']
                nodes.append(node)
                edges.append(edge)

            return JsonResponse([nodes, edges], safe=False, status=200)
        else:
            return JsonResponse({'error': 'Invalid API request method.'}, status=400)


@csrf_exempt
class DataProcess(View):
    @require_http_methods(['POST'])
    def get_data(request):
        try:
            csv_file = request.FILES["trace.csv"]
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")[1:]
            data_list = []
            for line in lines:
                try:
                    fields = line.split(",")
                    data_dict = {"timestamp": fields[0], "cmdb_id": fields[1], "span_id": fields[2],
                                "trace_id": fields[3], "duration": fields[4], "type": fields[5],
                                "status_code": fields[6], "operation_name": fields[7], "parent_span": fields[8],
                                "label": 0}
                    data_list.append(Span(**data_dict))
                except:
                    print('line', line)
                    return JsonResponse({'isSuccess': 'error', 'info': '文件数据导入失败!'}, status=500)
            Span.objects.bulk_create(data_list)
            return JsonResponse({'isSuccess': 'ok', 'info': '文件数据导入成功！'}, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'isSuccess': 'error', 'info': '文件数据导入失败!'}, status=500)

    @require_http_methods(['GET'])
    def output_trace_csv(request):
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="trace.csv"'
            writer = csv.writer(response)
            writer.writerow(['timestamp', 'cmdb_id', 'span_id', 'trace_id', 'duration', 'type',
                             'status_code', 'operation_name', 'parent_span', 'label'])
            data = Span.objects.all().values_list('timestamp', 'cmdb_id', 'span_id', 'trace_id', 'duration', 'type',
                                                  'status_code', 'operation_name', 'parent_span', 'label')
            
            for item in list(data):
                print(item)
                writer.writerow(item)
            return response
        except Exception as e:
            print(e)
            return JsonResponse({'isSuccess': 'error', 'info': '请检查程序!'}, status=500)

    @require_http_methods(['GET'])
    def output_rcl_csv(request):
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="groundtruth.csv"'
            writer = csv.writer(response)
            writer.writerow(['trace_id', 'operation_name', 'cmdb_id'])
            data = RCLLabel.objects.all().values_list('trace_id', 'operation_name', 'cmdb_id')
            for item in list(data):
                writer.writerow(item)
            return response
        except Exception as e:
            print(e)
            return JsonResponse({'isSuccess': 'error', 'info': '请检查程序!'}, status=500)


@csrf_exempt
class ModifyDB(View):
    @require_http_methods(['GET'])
    def get_root_cause(request):
        try:
            # data = json.loads(request.body)
            trace_id = request.GET.get("trace_id")
            span_id = request.GET.get("span_id")
            if Span.objects.get(span_id=span_id, trace_id=trace_id).label == 2:
                return JsonResponse({'isSuccess': 'false', 'info': '此调用链已标注，请检查!'}, safe=False, status=500)
            else:
                root_cause_span = Span.objects.get(span_id=span_id, trace_id=trace_id)
                parent_span_id = root_cause_span.parent_span
                root_cause_span.label = 2
                root_cause_span.save()
                span_list = get_span_list(trace_id)
                span_list = set(map(lambda x: x['span_id'], span_list))
                while parent_span_id in span_list and parent_span_id != "":
                    anomaly_span = Span.objects.get(span_id=parent_span_id, trace_id=trace_id)
                    parent_span_id = anomaly_span.parent_span
                    anomaly_span.label = 1
                    anomaly_span.save()
                return JsonResponse({'isSuccess': 'ok', 'info': '调用链标注成功!'}, safe=False, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'isSuccess': 'error', 'info': '调用链标注失败!'}, status=400)
