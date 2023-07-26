from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import ia_instrumaster_app.model.prediction as mm 
import os
# Create your views here.

class PredictsFruit(APIView):
    def get(self, request, format=None):
        # instrumento = mm.HacerPrediccion()
        return Response(status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        archivo = request.FILES['wav']
        archivo_guardado = os.path.join('assets', archivo.name)
        
        with open(archivo_guardado, 'wb+') as destination:
            for chunk in archivo.chunks():
                destination.write(chunk)

        mensaje_respuesta = f'El archivo se guardó en {archivo_guardado}'
        predict = mm.HacerPrediccion(archivo_guardado)
        os.remove(archivo_guardado)
        return Response(predict, status=status.HTTP_200_OK)