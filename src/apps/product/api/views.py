from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from apps.product.forms import FactorCakeImageCreateForm


@method_decorator(csrf_exempt, name='dispatch')
class FactorCakeImageCreate(View):

    def post(self, request):
        data = request.POST.copy()
        data['request'] = request
        f = FactorCakeImageCreateForm(data=data, files=request.FILES)
        if not f.is_valid():
            return JsonResponse({
                'msg': str(f.errors),
                'data': str(data)
            })
        obj = f.save()
        return JsonResponse({
            'status': 200,
            'detail': {
                'factor_code': obj.factor_code
            }
        })
