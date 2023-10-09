from django.shortcuts import render
from sqlalchemy import create_engine, exc
import hashlib
import pandas as pd
from app.doc_intel_quickstart import analyze_invoice


# Create your views here.
def login(request):
    return render(request, 'login.html')

def connection():
    try:
        conn = create_engine('mysql+pymysql://root:root@localhost/stock')
    except exc.SQLAlchemyError as e:
        print(e)

    return conn


conn = connection()

def validation(request):
    file = 'invoice_sample.jpg'
    extracted = analyze_invoice(file)
    data_df = pd.DataFrame.from_dict(extracted)
    print(data_df.head(5))
    return render(request, 'index.html')


def registration(request):
    conn = connection()
    try:
        uname = request.POST.dict().get('username')
        fname = request.POST.dict().get('fname')
        lname = request.POST.dict().get('lname')
        pword = request.POST.dict().get('pword')
        email = request.POST.dict().get('email')
        modules = request.POST.getlist('modules')
        modules = ", ".join(modules)
        encpw = hashlib.sha256(pword.encode()).hexdigest()
        conn.execute(
            f"INSERT into users (username,firstname,lastname,password,email,modules) VALUES ('{uname}','{fname}','{lname}','{encpw}','{email}','{modules}')")
        conn.dispose()
    except Exception as e:
        print(e)
    return render(request, 'login.html')


def intelliextract(request):
    return render(request, 'intelliextract.html')


def search_history(request):
    return render(request, 'search-history.html')

