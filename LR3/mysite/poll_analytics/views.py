from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Poll, Choice
from django.http import HttpResponse
import csv
import json
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import matplotlib.pyplot as plt
import io
import base64

class PollAnalyticsView(APIView):
    @swagger_auto_schema(
        operation_description="Получить аналитику по опросу, включая процентное распределение голосов по вариантам ответа и дату",
        manual_parameters=[
            openapi.Parameter('poll_id', openapi.IN_QUERY, description="ID опроса для получения аналитики", type=openapi.TYPE_INTEGER, required=True)
        ],
        responses={
            200: openapi.Response(
                description="Успешный ответ с аналитикой опроса",
                examples={
                    "application/json": {
                        "question": "Ваш любимый цвет?",
                        "choices": [
                            {"choice_text": "Синий", "votes": 50, "percentage": 50.0},
                            {"choice_text": "Красный", "votes": 30, "percentage": 30.0},
                            {"choice_text": "Зеленый", "votes": 20, "percentage": 20.0}
                        ],
                        "date_conducted": "2023-10-01T12:00:00"
                    }
                }
            ),
            400: openapi.Response(description="Некорректный запрос, отсутствует параметр poll_id"),
            404: openapi.Response(description="Опрос с указанным poll_id не найден")
        }
    )
    def get(self, request, *args, **kwargs):
        poll_id = request.query_params.get('poll_id')
        if poll_id:
            try:
                poll_id = int(poll_id)
            except ValueError:
                return Response({"error": "poll_id must be an integer"}, status=400)
        if not poll_id:
            return Response({"error": "poll_id is required"}, status=400)
        
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=404)
        
        choices = Choice.objects.filter(poll=poll)
        total_votes = sum(choice.votes for choice in choices)
        choices_data = [
            {
                "choice_text": choice.text,
                "votes": choice.votes,
                "percentage": (choice.votes / total_votes * 100) if total_votes > 0 else 0
            }
        for choice in choices]

        data = {
            "question": poll.question,
            "choices": choices_data,
            "date_conducted": poll.created_date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        return Response(data)

class PollListView(APIView):
    @swagger_auto_schema(
        operation_description="Получить список опросов, отсортированных по количеству голосов (от возрастания/убывания) или дате создания (от старых к новым/от новых к старым)",
        manual_parameters=[
            openapi.Parameter('sort_by', openapi.IN_QUERY, description="Сортировать по (votes или date)", type=openapi.TYPE_STRING),
            openapi.Parameter('order', openapi.IN_QUERY, description="Порядок сортировки (asc или desc)", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response(
                description="Успешный ответ с списком опросов",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "question": "Ваш любимый цвет?",
                            "created_date": "2023-10-01T12:00:00",
                            "total_votes": 100
                        },
                        {
                            "id": 2,
                            "question": "Ваш любимый фрукт?",
                            "created_date": "2023-09-25T12:00:00",
                            "total_votes": 80
                        }
                    ]
                }
            ),
            400: openapi.Response(description="Некорректный запрос, неверное значение параметра sort_by или order")
        }
    )
    def get(self, request):
        sort_by = request.query_params.get('sort_by')
        order = request.query_params.get('order', 'desc')
        
        if order not in ['asc', 'desc']:
            return Response({"error": "order must be 'asc' or 'desc'"}, status=400)
        
        order_prefix = '' if order == 'asc' else '-'
        
        if sort_by == 'votes':
            polls = Poll.objects.annotate(total_votes=Sum('choices__votes')).order_by(f'{order_prefix}total_votes')
        elif sort_by == 'date':
            polls = Poll.objects.all().order_by(f'{order_prefix}created_date')
        else:
            polls = Poll.objects.all().order_by(f'{order_prefix}created_date')
        
        polls_data = []
        for poll in polls:
            choices = Choice.objects.filter(poll=poll)
            total_votes = sum(choice.votes for choice in choices)
            poll_data = {
                "id": poll.id,
                "question": poll.question,
                "created_date": poll.created_date.strftime('%Y-%m-%dT%H:%M:%S'),
                "total_votes": total_votes
            }
            polls_data.append(poll_data)
        
        return Response(polls_data)

class PollExportJSONView(APIView):
    def get(self, request):
        polls = Poll.objects.all()
        polls_data = []
        for poll in polls:
            choices = Choice.objects.filter(poll=poll)
            total_votes = sum(choice.votes for choice in choices)
            poll_data = {
                "id": poll.id,
                "question": poll.question,
                "created_date": poll.created_date.strftime('%Y-%m-%dT%H:%M:%S'),
                "total_votes": total_votes,
                "choices": [{"choice_text": choice.text, "votes": choice.votes} for choice in choices]
            }
            polls_data.append(poll_data)
        return Response(polls_data, content_type="application/json")

class PollExportCSVView(APIView):
    def get(self, request):
        polls = Poll.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="polls.csv"'
        
        response.write('\ufeff'.encode('utf8'))  # Add BOM to handle UTF-8 in Excel
        writer = csv.writer(response)
        writer.writerow(['ID', 'Question', 'Created Date', 'Total Votes', 'Choices'])
        
        for poll in polls:
            choices = Choice.objects.filter(poll=poll)
            total_votes = sum(choice.votes for choice in choices)
            choices_text = "; ".join([f"{choice.text} ({choice.votes})" for choice in choices])
            created_date = poll.created_date.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([poll.id, poll.question, created_date, total_votes, choices_text])
        
        return response

class PollChartView(APIView):
    @swagger_auto_schema(
        operation_description="Получить график опроса в виде столбчатой диаграммы, закодированной в base64",
        manual_parameters=[
            openapi.Parameter('poll_id', openapi.IN_QUERY, description="ID опроса для получения графика", type=openapi.TYPE_INTEGER, required=True)
        ],
        responses={
            200: openapi.Response(
                description="Успешный ответ с графиком опроса",
                examples={
                    "application/json": {
                        "chart": "data:image/png;base64,..."
                    }
                }
            ),
            400: openapi.Response(description="Некорректный запрос, отсутствует параметр poll_id"),
            404: openapi.Response(description="Опрос с указанным poll_id не найден")
        }
    )
    def get(self, request, *args, **kwargs):
        poll_id = request.query_params.get('poll_id')
        if poll_id:
            try:
                poll_id = int(poll_id)
            except ValueError:
                return Response({"error": "poll_id must be an integer"}, status=400)
        if not poll_id:
            return Response({"error": "poll_id is required"}, status=400)
        
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=404)
        
        choices = Choice.objects.filter(poll=poll)
        choice_texts = [choice.text for choice in choices]
        votes = [choice.votes for choice in choices]
        
        plt.figure(figsize=(10, 6))
        plt.bar(choice_texts, votes, color='blue')
        plt.xlabel('Choices')
        plt.ylabel('Votes')
        plt.title(poll.question)
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        image_base64 = base64.b64encode(image_png).decode('utf-8')
        image_data = f"data:image/png;base64,{image_base64}"
        
        return Response({"chart": image_data})

