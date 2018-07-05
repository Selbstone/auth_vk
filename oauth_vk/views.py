from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialToken
import requests

# Create your views here.


def index(request):
    users_list = []
    vk_uid = SocialAccount.objects.filter(user_id=request.user.id, provider='vk')
    if vk_uid.exists():
        vk_uid = vk_uid[0].uid
        token_vk = SocialToken.objects.get(account__user=request.user, account__provider='vk')
        returned_json = requests.get("https://api.vk.com/method/friends.get?count=5&user_ids=" + vk_uid
                                     + "&fields=first_name,last_name,photo&access_token=" + str(token_vk) + "&v=5.80")
        context = returned_json.json()
        for i in range(5):
            first_name = context['response']['items'][i]['first_name']
            last_name = context['response']['items'][i]['last_name']
            users_list.append(' '.join((first_name, last_name)))

    return render(request, "index.html", {'users_list': users_list})

