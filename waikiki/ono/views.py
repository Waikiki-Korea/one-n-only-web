import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from ono.models import TestInfo

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the index.")
    return render(request, 'ono/index.html')

def test_minting(request):
    print("[", request.method, "], /test/minting")

    if request.method == 'POST':
        # store DB - tested (20220428)
        ti = TestInfo() #user_id=user_id_, user_name=user_name_, file_path="", ipfs_path="")
        ti.user_id = request.POST['user_id']
        ti.user_name = request.POST['user_name']

        for img in request.FILES.getlist('images'):
            ti.image = img
            break;

        print("user_id = ", ti.user_id, ", image = ", ti.image)

        ti.save()

        response = {
            "result":"successful",
            "reason":"OK"
        }

        # return HttpResponse(json.dumps(response), content_type = "application/json")
    else:
        response = {
            "result":"failed",
            "reason":"Request method is GET"
        }

        # return HttpResponse(json.dumps(response), content_type = "application/json")

    return render(request, 'ono/result.html', response)
    # raise Http404("Oops!...")
    # return HttpResponse(response)