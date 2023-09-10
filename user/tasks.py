import pandas as pd
from celery import shared_task
from pathlib import Path
from django.conf import settings


@shared_task(queue="queue1")
def compute_credit_score_task(aadhar_id, uuid):
    import math
    from django.contrib.auth import get_user_model
    User = get_user_model()
    file_path = Path(settings.BASE_DIR) / 'user' / 'transactions.csv'
    _df = pd.read_csv(file_path, keep_default_na=False)
    total_account_balance = 0
    for _data in _df.iterrows():
        user = _data[1].get('user')
        date = _data[1].get('date')
        transaction_type = _data[1].get('transaction_type')
        amount = _data[1].get('amount')
        if user == aadhar_id:
            total_account_balance += amount if transaction_type == "CREDIT" else -amount
    credit_score = 300
    if (total_account_balance > 100000 and total_account_balance < 1000000):
        credit_score += math.ceil(total_account_balance / 1500)
    elif (total_account_balance >= 1000000):
        credit_score = 900

    try:
        user = User.objects.get(id=uuid)
    except Exception as e:
        user = None

    if user is None:
        return

    user.credit_score = credit_score
    user.save()
