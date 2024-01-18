from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Dht11
from .serializers import DHT11serialize


@api_view(["GET", "POST"])
def dhtser(request):
    if request.method == "GET":
        # Retrieve all data
        all_data = Dht11.objects.all()
        # Serialize the data
        data_ser = DHT11serialize(all_data, many=True)
        # Return the serialized data as a response
        return Response(data_ser.data)

    elif request.method == "POST":
        # Deserialize the incoming data
        serial = DHT11serialize(data=request.data)

        # Check if the data is valid
        if serial.is_valid():
            # Save the valid data
            serial.save()
            # Return the serialized data as a response with status 201 Created
            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            # Return the validation errors as a response with status 400 Bad Request
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
