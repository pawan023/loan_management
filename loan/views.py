from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone
from decimal import Decimal
from django.core import serializers

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from loan.models import Loan, LoanType, Transaction
from user.models import User


# Create your views here.


class InitiateLoan(APIView):
    def post(self, request):
        data = request.data
        uuid = data.get("uuid")
        loan_type = data.get("loan_type")
        loan_amount = data.get("loan_amount")
        interest_rate = data.get("interest_rate")
        term_period = data.get("term_period")
        disbursement_date = data.get("disbursement_date")
        LoanType.objects.get_or_create(loan_type="Car", max_approved_amount=750000)
        LoanType.objects.get_or_create(loan_type="Home", max_approved_amount=8500000)
        LoanType.objects.get_or_create(loan_type="Educational", max_approved_amount=5000000)
        LoanType.objects.get_or_create(loan_type="Personal", max_approved_amount=1000000)

        try:
            user = User.objects.get(id=uuid)
        except Exception as e:
            user = None

        if user is None:
            return Response(data={"status": "failed",
                                  "status_message": "The user registration should be done before applying for a loan"},
                            status=HTTP_400_BAD_REQUEST)
        if user.credit_score is None or user.credit_score < 450:
            return Response(
                data={"status": "failed", "status_message": "As per the credit score user is not eligible for a loan"},
                status=HTTP_400_BAD_REQUEST)
        if user.annual_income < 150000:
            return Response(
                data={"status": "failed",
                      "status_message": "Due to less Annual income user is not eligible for a loan"},
                status=HTTP_400_BAD_REQUEST)

        try:
            loan_type_object = LoanType.objects.get(loan_type=loan_type)
        except Exception as e:
            loan_type_object = None
        loan_amount = int(loan_amount)
        if loan_type_object is None or loan_amount < 0:
            return Response(
                data={"status": "failed", "status_message": "Invalid loan type"},
                status=HTTP_400_BAD_REQUEST)
        if loan_type_object.max_approved_amount < loan_amount:
            return Response(
                data={"status": "failed", "status_message": "Loan amount is not permissible"},
                status=HTTP_400_BAD_REQUEST)

        interest_rate = float(interest_rate)
        term_period = int(term_period)
        emi_interest_rate = interest_rate / 12 / 100
        emi = int(loan_amount * (emi_interest_rate * (1 + emi_interest_rate) ** term_period) / (
                (1 + emi_interest_rate) ** term_period - 1))
        payable_amount = (emi * term_period)
        emis = []
        disbursement_date = datetime.strptime(disbursement_date, '%Y-%m-%d')
        due_date = disbursement_date.replace(day=1) + timedelta(days=32)
        for _ in range(term_period):
            due_date = due_date.replace(day=1)
            emis.append({
                "Date": due_date.strftime('%Y-%m-%d'),
                "Amount_due": emi
            })
            due_date += timedelta(days=32)
        loan = Loan.objects.create(uuid=uuid, loan_type_id=loan_type_object.id, loan_amount=loan_amount,
                                   interest_rate=interest_rate,
                                   term_period=term_period, disbursement_date=disbursement_date, is_active=True,
                                   remaining_amount=payable_amount, remaining_period=term_period)

        return Response(data={"Loan_id": loan.id, "Due_dates": emis}, status=HTTP_200_OK)


class EmiPayment(APIView):
    def post(self, request):
        data = request.data
        loan_id = data.get("loan_id")
        amount_paid = data.get("amount_paid")

        try:
            loan = Loan.objects.get(id=loan_id)
        except Exception as e:
            loan = None

        amount_paid = int(amount_paid)

        if loan is None:
            return Response(
                data={"status": "failed", "status_message": "Invalid loan_id"},
                status=HTTP_400_BAD_REQUEST)
        if loan.is_active is False:
            return Response(
                data={"status": "failed", "status_message": "Loan Payment is Completed, no further dues left"},
                status=HTTP_400_BAD_REQUEST)

        if amount_paid > loan.remaining_amount:
            return Response(
                data={"status": "failed", "status_message": "Payment amount is more than total due amount"},
                status=HTTP_400_BAD_REQUEST)
        if Transaction.objects.filter(loan=loan_id, date=datetime.now().date()).exists():
            return Response({"Error": "Payment for today is already made"}, status=HTTP_400_BAD_REQUEST)

        loan.remaining_amount = loan.remaining_amount - amount_paid
        loan.remaining_period = loan.remaining_period - 1
        if loan.remaining_amount == 0:
            loan.is_active = False

        Transaction.objects.create(loan=loan_id, amount_paid=amount_paid, date=datetime.now().date(),
                                   remaining_amount=loan.remaining_amount, remaining_period=loan.remaining_period)
        return Response(data={"status": "success", "status_message": "Payment is successfully made", "Error": None},
                        status=HTTP_200_OK)


class GetStatement(APIView):
    def get(self, request):
        data = request.data
        loan_id = data.get("loan_id")

        try:
            loan = Loan.objects.get(id=loan_id)
        except Exception as e:
            loan = None

        if loan is None:
            return Response(
                data={"status": "failed", "status_message": "Invalid loan_id"},
                status=HTTP_400_BAD_REQUEST)
        if loan.remaining_amount == 0:
            matching_rows = Transaction.objects.filter(loan=loan_id)
            past_transactions = []
            print("1loan.remaining_amount 2: ", loan.remaining_amount)

            for transaction in matching_rows:
                amount = transaction.amount_paid
                date = transaction.date
                principal = transaction.remaining_amount
                past_transactions.append({"amount": amount, "date": date, "principal": principal})
            return Response(
                data={"status": "success", "status_message": "Loan Payment is Completed, no further dues left",
                      "Past_transactions": past_transactions},
                status=HTTP_200_OK)

        current_date = datetime.now().date()
        statements = []
        for _ in range(loan.remaining_period):
            current_date = current_date.replace(day=1)
            statements.append({
                "Date": current_date.strftime('%Y-%m-%d'),
                "Amount_due": round(loan.remaining_amount / loan.remaining_period, 2)
            })
            current_date += timedelta(days=32)

        matching_rows = Transaction.objects.filter(loan=loan_id)
        past_transactions = []
        for transaction in matching_rows:
            amount = transaction.amount_paid
            date = transaction.date
            principal = transaction.remaining_amount
            past_transactions.append({"amount": amount, "date": date, "principal": principal})

        return Response(
            data={"status": "success", "Error": None,
                  "Past_transactions:": past_transactions,
                  "Upcoming_transactions:": statements}, status=HTTP_200_OK)
