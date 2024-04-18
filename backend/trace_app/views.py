# Create your views here.
import os.path

from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Span, RCLLabel,Task
from trace_app.trace_api import get_span_list, get_trace_list
import csv
import json
from collections import defaultdict
import re


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
                # if span['label']==1:
                #     node['color']='orange'
                #     edge['color']='red'
                # elif span['label']==2:
                #     node['color']='red'
                #     edge['color']='red'
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
                    fields = line.strip().split(",")
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


def process_data(data):
    nodes = []
    edges = []
    node_id_map = {}  # 用于记录每个节点名称对应的 ID
    current_id = 1

    for cmdb_id, data_row in data:
        # 处理节点
        node_label = cmdb_id
        if node_label not in node_id_map:
            node_id_map[node_label] = current_id
            node_id = current_id
            current_id += 1
        else:
            node_id = node_id_map[node_label]

        node = {'id': str(node_id), 'label': node_label, 'shape': 'circle'}
        nodes.append(node)

        # 处理边
        parents = data_row['parent_span'].split() if data_row['parent_span'] else []
        for parent in parents:
            parent_label = parent.strip()
            if parent_label in node_id_map:
                parent_id = node_id_map[parent_label]
                edge = {'from': str(parent_id), 'to': str(node_id)}
                edges.append(edge)

    return {'nodes': nodes, 'edges': edges}

# 忽略 CSRF 保护
@csrf_exempt
class TaskDB(View):
    def save_task(request):
        data =json.loads( request.GET['form'])
        new_task = Task.objects.create(
            task_name=data['Taskname'],
            learning_rate = data['LearningRate'],
            batch_size = data['Batchsize'],
            epoch = data['Epoch'],
            number_of_labels = data['NumberOfLabels'],
            # 其他项
        )
        return JsonResponse({'message': 'Task saved successfully'}, status=200)

    
    def get_task(request): 
        tasks = Task.objects.all()       
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.task_id,
                'name': task.task_name,
                'status': task.task_status,
                'progress': task.task_progress
                # 其他字段
            })
        
        return JsonResponse({'taskList': task_list})   
    
    def upload(request): 
        file_name = request.GET.get('file_name')
        print(file_name)
        if request.method == 'POST' and request.FILES.get('file'):
            file = request.FILES['file']
            # 获取当前文件所在目录（即 settings.py 文件所在目录）
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # 获取项目根目录（假设 settings.py 文件位于根目录下的 myproject 文件夹中）
            project_root = os.path.dirname(current_directory)

            # 构建文件保存路径
            file_path = os.path.join(project_root, file_name, file.name)

            # 确保目标目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # print(file_path)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return JsonResponse({'message': 'File uploaded successfully'}, status=200) 
    
# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 GET
@require_http_methods(['GET'])
class Test(View):   
    def get_res(request):
        querydata = Span.objects.all().values()

        data = {'data': list(querydata)}
        import csv
        from collections import defaultdict
        import re

        # 表A，用于存储 span_id 对应的 cmdb_id
        table_A = {}
        # 用于存储聚合后的数据
        aggregated_data = defaultdict(dict)
        # 用于统计每种cmdb_id出现的次数
        cmdb_id_counts = defaultdict(int)

        for row in list(querydata):
            if 'cmdb_id' in row:  # 检查是否存在'cmdb_id'字段
                cmdb_id = row['cmdb_id']
                # 提取字母部分
                cmdb_id_alpha = re.match(r'[a-zA-Z]+', cmdb_id).group()
                table_A[row['span_id']] = cmdb_id_alpha
                # 统计每种cmdb_id出现的次数
                cmdb_id_counts[cmdb_id_alpha] += 1


        for row in list(querydata):
            if 'cmdb_id' in row:  # 检查是否存在'cmdb_id'字段
                cmdb_id = row['cmdb_id']
                span_id = row['span_id']
                duration = int(row['duration'])
                parent_span = row['parent_span']

                # 替换 parent_span 为相应的 cmdb_id
                if parent_span in table_A:
                    parent_span = table_A[parent_span]

                # 提取字母部分
                cmdb_id_alpha = re.match(r'[a-zA-Z]+', cmdb_id).group()

                # 如果当前 cmdb_id 在 aggregated_data 中不存在，则创建一个新的条目
                if cmdb_id_alpha not in aggregated_data:
                    aggregated_data[cmdb_id_alpha] = {
                        'duration': duration,
                        'parent_span': [parent_span]
                    }
                else:
                    # 如果当前 cmdb_id 在 aggregated_data 中已经存在，则将持续时间累加
                    aggregated_data[cmdb_id_alpha]['duration'] += duration
                    # 添加 parent_span，并用空格分隔
                    aggregated_data[cmdb_id_alpha]['parent_span'].append(parent_span)
        # 对 parent_span 进行去重，并去除多余的空格
        for cmdb_id, data in aggregated_data.items():
            data['parent_span'] = " ".join(set(data['parent_span']))

        # 使用列表储存处理后的数据
        output_data = []
        # 将处理后的数据存储到列表中
        for cmdb_id, data in aggregated_data.items():
            # 计算平均持续时间
            average_duration = data['duration'] / cmdb_id_counts[cmdb_id]
            # 将每个 cmdb_id 的统计信息存储到列表中
            output_data.append({
                'Node': cmdb_id,
                'Parent': ' '.join(data['parent_span'].split()),
                'duration': data['duration'],
                'Occurrences': cmdb_id_counts[cmdb_id],
                'Average Duration': average_duration
            })


        data_processed = process_data(aggregated_data.items())

        return JsonResponse(data_processed, safe=False, status=200)
    
# 忽略 CSRF 保护
@csrf_exempt
# 限制 HTTP 方法为 GET
@require_http_methods(['GET'])
class List(View):   
    def get_tree(request):
        querydata = Span.objects.all().values()
        trace_id = request.GET.get('trace_id')
        nodes = {}
        data_temp = []
        duration_list = []
        duration_all_list = []
        lines = []
        all_lines = []

        for item in querydata:
             one_line = (item['span_id'], item['parent_span'], item['cmdb_id'], item['duration'], item['operation_name'])
             all_lines.append(one_line)  

        for item in querydata:
            if item['trace_id'] == trace_id:

                line = (item['span_id'], item['parent_span'], item['cmdb_id'], item['duration'], item['operation_name'])
                lines.append(line) 

        for _,_,_,duration,_ in lines:
            duration_list.append(duration)
        
        for _,_,_,duration,_ in all_lines:
            duration_all_list.append(duration)

        min_duration = min(duration_all_list)
        max_duration = max(duration_all_list)
        print("=====================")
        print(min_duration)
        print(max_duration)

        for line in lines:
            id, parentId, cmdb_id, duration, operation_name = line
            # parentId为空，等于span_id，代表是根节点
            if parentId == "":
                parentId = id
            # nodes[]保存需要的字典格式
            nodes[id] = {'id': id, "parentId": parentId, "cmdb_id": cmdb_id, "duration": duration,
                        "operation_name": operation_name, 'children': []}
            # data_temp 保存id,parentId
            data_temp.append({'id': id, "parentId": parentId})
        data = []
        for i in data_temp:
            id = i['id']
            parent_id = i['parentId']
            node = nodes[id]
            node['length'] = (node['duration']-min_duration)/(max_duration-min_duration)
            if id == parent_id:
                data.append(node)
            else:
                parent = nodes.get(parent_id)
                if parent:
                    parent['children'].append(node)
                else:
                    data.append(node)
            
        return JsonResponse(data, safe=False, status=200)