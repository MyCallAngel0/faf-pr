import json, os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_json(request):
    if request.method == 'POST' and request.FILES['file']:
        json_file = request.FILES['file']

        try:
            json_data = json_file.read()
            data = json.loads(json_data)
            file_path = os.path.join(os.getcwd(), "log.json")
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            return JsonResponse({'message': 'File uploaded successfully!', 'data': data})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON file.'}, status=400)
    else:
        return JsonResponse({'error': 'File not present'}, status=400)