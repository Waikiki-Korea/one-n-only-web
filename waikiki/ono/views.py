import json
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from ono.models import Collection, OnoUser, Token, TempImage, Abi
from django.contrib.auth import get_user_model
from ono.modules.ono_engine.test import testComparison
from ono.modules.ono_web3.nft_contract import testSearch, create_nft_contract, mint_item
from ono.modules.ono_utils.ono_utils import removeFile
import os
import ipfsApi


def index(request):
    collections = Collection.objects.all()
    tokens = Token.objects.all()

    return render(request, 'ono/index.html', {'collections': collections, 'tokens': tokens})


def dashboard(request, user_id):
    onoUser = get_object_or_404(OnoUser, pk=user_id)
    print("[dashboard] onoUser = ", onoUser)

    # Organisation.objects.filter(name__iexact = 'Fjuk inc')
    collections = Collection.objects.filter(user_id=onoUser)
    if len(collections) != 0:
        tokens = Token.objects.filter(collection_id=collections[0])
        return render(request, 'ono/dashboard.html', {'collections': collections, 'tokens': tokens})

    return render(request, 'ono/dashboard.html')

def search(request):
    print("[", request.method, "], /search")

    if request.method == 'POST':
        print("search requested = ", request.POST['search'])

        response = {
            "search_text": request.POST['search'],
            "result": testSearch(request.POST['search'])
        }

    else:
        return redirect('../')

    return render(request, 'ono/search_result.html', response)


def collection(request, user_id):
    print("[", request.method, "], /", user_id, "/collection")

    response = {
        "result": "failed",
        "reason": "<TBD>"
    }
    if request.method == 'POST':
        print('[ Request ] ', request)

        # id, user_id, title, symbol, blockchain, token_size, media_type, contract_address, description, create_date, updated_date
        onoUser = get_object_or_404(OnoUser, pk=user_id)

        collection = Collection()
        collection.user_id = onoUser
        collection.title = request.POST['title']
        for img in request.FILES.getlist('symbol'):
            collection.symbol = img
            break
        collection.blockchain = request.POST['blockchain']
        collection.token_size = request.POST['token_size']
        collection.media_type = request.POST['media_type']
        collection.description = request.POST['description']
        r = create_nft_contract(
            onoUser.eth_address,
            request.POST['private_key'],
            collection.title,
            "symbol"
        )
        collection.contract_address = r['contract_address']
        collection.save()

        abi = Abi()
        abi.id = collection
        abi.abi = json.dumps(r['abi'])
        abi.save()

        response = {
            "result": "successful",
            "reason": "OK"
        }

    else:
        print('..')
        return render(request, 'ono/collection.html')

    return render(request, 'ono/result.html', response)


def mint(request, _user_id):
    print("[", request.method, "], /", _user_id, "/mint")

    response = {
        "result": "failed",
        "reason": "<TBD>"
    }
    if request.method == 'POST':
        print('[ Request ] ', request)

        # id, collection_id, title, media_type, ipfs_path, token_path, sha256_hash, description, owner, created_date, updated_date
        # collections = get_list_or_404(Collection, user_id=_user_id)
        collection = get_object_or_404(
            Collection, pk=int(request.POST['collection_id']))

        token = Token()
        # token.collection_id = collections[int(request.POST['collection_id'])]
        token.collection_id = collection

        onoUser = get_object_or_404(OnoUser, pk=_user_id)
        # onoUser = get_object_or_404(OnoUser, pk=token.collection_id.user_id)

        token.title = request.POST['title']
        token.media_type = request.POST['media_type']
        # token.ipfs_path = request.POST['ipfs_path']
        # token.token_path = request.POST['token_path']
        # token.sha256_hash = request.POST['sha256_hash']
        token.description = request.POST['description']
        # token.owner = request.POST['owner']
        token.owner_address = onoUser.eth_address
        for img in request.FILES.getlist('token_image'):
            token.token_image = img
            break

        # 이미지 판단 시작 [
        tempImage = TempImage()
        tempImage.image = token.token_image
        tempImage.save()

        image_response = testComparison(os.path.join(
            os.getcwd() + "/media/" + str(tempImage.image)))
        print("[image_response] ", image_response)

        # 유사도 판단
        if image_response['similarity'] < 99:
            print("[similarity] This is not a scam. Store item into DB.")
            api = ipfsApi.Client('127.0.0.1', 5001)
            res = api.add(os.path.join(
                os.getcwd() + "/media/" + str(tempImage.image)))
            print("[IPFS RES] ", res[0]['Hash'])
            token.ipfs_path = "http://localhost:8080/ipfs/" + \
                str(res[0]['Hash'])
            token.save()

            abi = get_object_or_404(Abi, pk=token.collection_id)
            r = mint_item(onoUser.eth_address,
                          request.POST['private_key'],
                          token.collection_id.contract_address,
                          abi.abi,
                          onoUser.eth_address,
                          token.id,
                          token.ipfs_path)

            

            response = {
                "result": "successful",
                "reason": "OK",
                "similarity": image_response['similarity'],
                "duration": image_response['duration']
            }
        else:
            print("[similarity] This is a scam!!!")
            response = {
                "result": "failed",
                "reason": "Similarity is so high.",
                "similarity": image_response['similarity'],
                "duration": image_response['duration']
            }
        # 이미지 판단 끝 ]

    else:
        print('..')
        # collections = list(Collection.objects.filter(user_id=_user_id))
        # get_object_or_404(Collection, user_id=_user_id)
        # print("[ collections ] ", collections)
        return render(request, 'ono/mint.html')

    return render(request, 'ono/result.html', response)


def test_image(request):
    print("[", request.method, "], test/image")

    response = {
        "result": "failed",
        "reason": "<TBD>"
    }
    if request.method == 'POST':
        print('[ Request ] ', request)

        tempImage = TempImage()

        for img in request.FILES.getlist('test_image'):
            tempImage.image = img
            break
        tempImage.save()

        # 이미지 판단 시작 [
        image_response = testComparison(os.path.join(
            os.getcwd() + "/media/" + str(tempImage.image)))
        print("[image_response] ", image_response)

        '''
        <TBD>
        response 판단 후, 유사도 판단에 따라 등록 여부를 결정.
        '''
        # 이미지 판단 끝 ]
        removeFile("/media/", str(tempImage.image))
        tempImage.delete()  # delete column from table

        response = {
            "result": "successful",
            "reason": "OK",
            "similarity": image_response['similarity'],
            "duration": image_response['duration']
        }

    else:
        print('..')
        return render(request, 'ono/test_image.html')

    return render(request, 'ono/result.html', response)


def test_minting(request):
    print("[", request.method, "], /test/minting")

    if request.method == 'POST':
        # store DB - tested (20220428)
        # ti = TestInfo() #user_id=user_id_, user_name=user_name_, file_path="", ipfs_path="")
        # ti.user_id = request.POST['user_id']
        # ti.user_name = request.POST['user_name']

        # for img in request.FILES.getlist('images'):
        #     ti.image = img
        #     break;

        # print("user_id = ", ti.user_id, ", image = ", ti.image)

        # ti.save()

        response = {
            "result": "successful",
            "reason": "OK"
        }

        # return HttpResponse(json.dumps(response), content_type = "application/json")
    else:
        response = {
            "result": "failed",
            "reason": "Request method is GET"
        }

        # return HttpResponse(json.dumps(response), content_type = "application/json")

    return render(request, 'ono/result.html', response)
    # raise Http404("Oops!...")
    # return HttpResponse(response)


def make_contract(request):
    print("[", request.method, "], /test/makecontract")

    # if request.method == 'POST':
    response = {
        "search_text": "",
        "result": create_nft_contract()
    }

    # else:
    #     return redirect('../')

    return render(request, 'ono/search_result.html', response)


def make_token(request):
    print("[", request.method, "], /test/maketoken")

    response = {
        "search_text": "",
        "result": mint_item()
    }

    return render(request, 'ono/search_result.html', response)
