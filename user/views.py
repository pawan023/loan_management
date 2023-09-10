from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from user.models import User


# Create your views here.

class CreateUser(APIView):
    def post(self, request):
        from user.tasks import compute_credit_score_task
        data = request.data

        aadhar_id = data.get("aadhar_id")
        name = data.get("name")
        email = data.get("email")
        annual_income = data.get("annual_income")
        username = str(name) + "." + str(aadhar_id)

        user = User.objects.create(aadhar_id=aadhar_id, first_name=name, username=username, email=email,
                                   annual_income=annual_income)
        uuid, aadhar_id = user.id, user.aadhar_id
        compute_credit_score_task.delay(aadhar_id, uuid)
        return Response(data={"status": "success", "uuid": user.id}, status=HTTP_200_OK)
