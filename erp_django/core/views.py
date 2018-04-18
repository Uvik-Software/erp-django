import json

from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

HEROES = [
        {'id': 11, 'name': 'Mr. Nice'},
        {'id': 12, 'name': 'Narco'},
        {'id': 13, 'name': 'Bombasto'},
        {'id': 14, 'name': 'Celeritas'},
        {'id': 15, 'name': 'Magneta'},
        {'id': 16, 'name': 'RubberMan'},
        {'id': 17, 'name': 'Dynama'},
        {'id': 18, 'name': 'Dr IQ'},
        {'id': 19, 'name': 'Magma'},
        {'id': 20, 'name': 'Tornado'}
    ]


def index(request):
    return render(request=request, template_name='core/index.html', context={})

@csrf_exempt
def heroes(request):
    if request.method == 'POST':
        post = json.loads(request.body)
        post.update({'id': len(HEROES)})
        HEROES.append(post)
        return JsonResponse(post, safe=False)

    if 'name' in request.GET:
        return JsonResponse(list(filter(lambda x: x['name'].startswith(request.GET['name']), HEROES)), safe=False)

    return JsonResponse(HEROES, safe=False)

@csrf_exempt
def hero(request, id):
    heroitem = [x for x in HEROES if x['id']==id]

    if heroitem:
        if request.method == 'PUT':
            put = json.loads(request.body)
            heroitem[0]['name'] = put['name']
            return JsonResponse(heroitem[0], safe=False)

        if request.method == 'DELETE':
            for index, x in enumerate(HEROES):
                if x['id'] == id:
                    del HEROES[index]
            return JsonResponse('', safe=False)

        return JsonResponse(heroitem[0], safe=False)
    return JsonResponse(heroitem,safe=False)



