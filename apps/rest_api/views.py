
# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.renderers import (
    TemplateHTMLRenderer, 
    BrowsableAPIRenderer, 
    JSONRenderer, 
    # StaticHTMLRenderer
)
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExcelSerializer
from scraping.utils import (
    get_excel_data, search_in_column,
    file_is_exist, 
    # get_current_sheet, get_current_file
)

import openpyxl
import os



file_path = os.path.join(settings.BASE_DIR, "data.xlsx")
file = openpyxl.load_workbook(file_path)
current_sheet = file.active


class ExcelListCreateAPIView(APIView):

    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer)

    def get(self, request, pk=None):

        if file_is_exist(file_path):
            excel_data = get_excel_data(file_path)

            return Response(
                {"data": excel_data}, status=status.HTTP_200_OK,
            )

        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):

        if file_is_exist(file_path):
            requested_data = request.data
            serializer = ExcelSerializer(data=requested_data)
            if serializer.is_valid():

                last_row = current_sheet.max_row + 1
                current_sheet["A" + str(last_row)].value = requested_data["ranking"]
                current_sheet["B" + str(last_row)].value = requested_data["novel"]
                current_sheet["C" + str(last_row)].value = requested_data["author"]
                current_sheet["D" + str(last_row)].value = requested_data["country"]
                current_sheet["E" + str(last_row)].value = requested_data["novel_link"]
                current_sheet["F" + str(last_row)].value = requested_data["author_link"]
                current_sheet["G" + str(last_row)].value = requested_data["country_link"]

                file.save(file_path)
                file.close()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )


class ExcelDetailAPIView(APIView):

    def get(self, request, index):

        if file_is_exist(file_path):
            excel_data = get_excel_data(file_path)

            try:
                data = excel_data[index]

                return Response(
                    {"data": data},
                    status=status.HTTP_200_OK
                )

            except KeyError:
                return Response("Record Not Found !", status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, index):

        requested_data = request.data

        if file_is_exist(file_path):

            serializer = ExcelSerializer(data=requested_data)

            if serializer.is_valid():

                excel_data = get_excel_data(file_path)
                ranking = str(int(excel_data[index]["الترتيب"]))
                row_number = search_in_column(current_sheet, ranking, column="A")

                if row_number:

                    current_sheet["A" + str(row_number)] = requested_data["ranking"]
                    current_sheet["B" + str(row_number)] = requested_data["novel"]
                    current_sheet["C" + str(row_number)] = requested_data["author"]
                    current_sheet["D" + str(row_number)] = requested_data["country"]
                    current_sheet["E" + str(row_number)] = requested_data["novel_link"]
                    current_sheet["F" + str(row_number)] = requested_data["author_link"]
                    current_sheet["G" + str(row_number)] = requested_data["country_link"]

                    file.save(file_path)
                    file.close()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response("Row Not Found !", status=status.HTTP_404_NOT_FOUND)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, index):

        if file_is_exist(file_path):

            excel_data = get_excel_data(file_path)
            ranking = str(int(excel_data[index]["الترتيب"]))

            row_number = search_in_column(current_sheet, ranking, column="A")

            if row_number:
                current_sheet.delete_rows(row_number)

                file.save(file_path)
                file.close()

                return Response("Deleted", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Row Not Found !", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                "File Not Found !",
                status=status.HTTP_404_NOT_FOUND
            )