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
        user_id_ = request.POST['user_id']
        user_name_ = request.POST['user_name']

        print("user_id = ", user_id_)
        print("user_name = ", user_name_)

        # store DB - tested (20220428)
        ti = TestInfo(user_id=user_id_, user_name=user_name_, file_path="", ipfs_path="")
        ti.save()

        response = {
            "result":"success",
            "reason":"OK"
        }

        return HttpResponse(json.dumps(response), content_type = "application/json")
    else:
        response = {
            "result":"fail",
            "reason":"method is GET"
        }
        return HttpResponse(json.dumps(response), content_type = "application/json")

    # raise Http404("Oops!...")
    # return HttpResponse(response)