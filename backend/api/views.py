from rest_framework import serializers
from rest_framework.serializers import Serializer
from django.core.files.storage import default_storage
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
import os

# Importing dependencies of the ML Model

from pathlib import Path
import fastbook
from fastai.vision.all import *
import pathlib

model_path = os.path.relpath(
    'dog-breed-classifier/models/dog_model.pkl', 'api/views.py')

"""
Avoiding "pathing issues" by creating the PosixPath property needed for processing of certain path format
passed in
"""
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

fastbook.setup_book()

path = Path(model_path)

if path.exists():
    LEARN__INF = load_learner(model_path)
else:
    print(path)
    raise Exception("Model path does not exist")


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def result(request):
    """
    Return inference
    """
    img_file = request.FILES["imageFile"]
    img_name = default_storage.save(img_file.name, img_file)
    img_path = default_storage.path(img_name)

    try:
        inference = LEARN__INF.predict(img_path)[0]
        result = {'inference': inference}
        default_storage.delete(img_path)
        print(result)
        return Response(result, status=status.HTTP_200_OK)

    except:
        return Response({'error': 'Something has gone wrong. Please check file type'}, status=status.HTTP_400_BAD_REQUEST)
