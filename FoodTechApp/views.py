from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import os
import base64
import pickle
from datetime import date

from Blockchain import *
from Block import *

import pyqrcode
import png


# ---------------- GLOBAL VARIABLES ----------------
uname = ""
address = ""
phone = ""
deliver_address = ""
deliver_time = ""

# ---------------- BLOCKCHAIN INIT ----------------
blockchain = Blockchain()

# Safe loading (IMPORTANT for Render)
if os.path.exists('blockchain_contract.txt'):
    try:
        with open('blockchain_contract.txt', 'rb') as fileinput:
            blockchain = pickle.load(fileinput)
    except:
        blockchain = Blockchain()


# ---------------- HOME ----------------
def index(request):
    return render(request, 'index.html')


# ---------------- STATIC PAGES ----------------
def AddFood(request):
    return render(request, 'AddFood.html')


def Login(request):
    return render(request, 'Login.html')


def Admin(request):
    return render(request, 'Admin.html')


def Register(request):
    return render(request, 'Register.html')


# ---------------- USER / ADMIN SCREENS ----------------
def ViewOrders(request):
    output = '<table border=1 align=center>'
    output += '<tr><th>Food Name</th><th>User</th><th>Phone</th><th>Email</th><th>Address</th><th>Date</th></tr>'

    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = base64.b64decode(b.transactions[0])
            decrypt = blockchain.decrypt(data).decode("utf-8")
            arr = decrypt.split("#")

            if arr[0] == 'bookorder':
                details = arr[3].split(",")

                output += f"<tr><td>{arr[1]}</td>"
                output += f"<td>{arr[2]}</td>"
                output += f"<td>{details[0]}</td>"
                output += f"<td>{details[1]}</td>"
                output += f"<td>{details[2]}</td>"
                output += f"<td>{arr[4]}</td></tr>"

    output += "</table>"
    return render(request, 'ViewOrders.html', {'data': output})


# ---------------- ADD FOOD ----------------
def AddFoodAction(request):
    if request.method == 'POST':

        fname = request.POST['t1']
        batch = request.POST['t2']
        farm = request.POST['t3']
        expiry = request.POST['t4']
        storage = request.POST['t5']
        shipping = request.POST['t6']
        price = request.POST['t7']
        image = request.FILES['t8']

        imagename = image.name

        data = f"addproduct#{fname}#{batch}#{farm}#{expiry}#{storage}#{shipping}#{price}#{imagename}#qr_{batch}.png"

        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), 'utf-8')

        blockchain.add_new_transaction(enc)
        blockchain.mine()

        blockchain.save_object(blockchain, 'blockchain_contract.txt')

        fs = FileSystemStorage()
        fs.save(f'FoodTechApp/static/products/{imagename}', image)

        qr = pyqrcode.create(",".join([fname, batch, farm, expiry, storage, shipping, price]))
        qr.png(f'FoodTechApp/static/products/qr_{batch}.png', scale=6)

        return render(request, 'AddFood.html', {'data': 'Food Added Successfully'})


# ---------------- BROWSE ----------------
def BrowseProducts(request):
    output = '<tr><td>Select Food</td><td><select name="t1">'

    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = base64.b64decode(b.transactions[0])
            decrypt = blockchain.decrypt(data).decode("utf-8")
            arr = decrypt.split("#")

            if arr[0] == 'addproduct':
                output += f'<option value="{arr[1]}">{arr[1]}</option>'

    output += "</select></td></tr>"

    return render(request, 'BrowseProducts.html', {'data1': output})


# ---------------- SEARCH ----------------
def SearchProductAction(request):
    if request.method == 'POST':

        ptype = request.POST['t1']

        output = '<table border=1>'
        output += '<tr><th>Food</th><th>Batch</th><th>Farm</th><th>Expiry</th><th>Storage</th><th>Shipping</th><th>Price</th></tr>'

        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = base64.b64decode(b.transactions[0])
                decrypt = blockchain.decrypt(data).decode("utf-8")
                arr = decrypt.split("#")

                if arr[0] == 'addproduct' and arr[1] == ptype:
                    output += f"<tr><td>{arr[1]}</td><td>{arr[2]}</td><td>{arr[3]}</td><td>{arr[4]}</td><td>{arr[5]}</td><td>{arr[6]}</td><td>{arr[7]}</td></tr>"

        output += "</table>"

        return render(request, 'SearchProducts.html', {'data': output})


# ---------------- SIGNUP ----------------
def Signup(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        contact = request.POST['contact']
        email = request.POST['email']
        address = request.POST['address']

        data = f"signup#{username}#{password}#{contact}#{email}#{address}"

        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), 'utf-8')

        blockchain.add_new_transaction(enc)
        blockchain.mine()

        blockchain.save_object(blockchain, 'blockchain_contract.txt')

        return render(request, 'Register.html', {'data': 'Signup Success'})


# ---------------- USER LOGIN ----------------
def UserLogin(request):
    global uname, address, phone

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = base64.b64decode(b.transactions[0])
                decrypt = blockchain.decrypt(data).decode("utf-8")
                arr = decrypt.split("#")

                if arr[0] == "signup":
                    if arr[1] == username and arr[2] == password:
                        uname = username
                        address = arr[5]
                        phone = arr[3]

                        with open("session.txt", "w") as f:
                            f.write(username)

                        return render(request, 'UserScreen.html', {'data': 'Login Success'})

        return render(request, 'Login.html', {'data': 'Invalid login'})


# ---------------- ADMIN LOGIN ----------------
def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == "admin" and password == "admin":
            return render(request, 'AdminScreen.html', {'data': 'Welcome Admin'})

        return render(request, 'Admin.html', {'data': 'Invalid login'})


# ---------------- BOOK ORDER ----------------
def BookOrder(request):
    global deliver_address, deliver_time

    pid = request.GET['crop']

    user = open("session.txt").read().strip()

    today = date.today()

    data = f"bookorder#{pid}#{user}#details#{today}#{deliver_address}#{deliver_time}"

    enc = blockchain.encrypt(str(data))
    enc = str(base64.b64encode(enc), 'utf-8')

    blockchain.add_new_transaction(enc)
    blockchain.mine()

    blockchain.save_object(blockchain, 'blockchain_contract.txt')

    return render(request, 'UserScreen.html', {'data': 'Order Placed'})


# ---------------- DELIVERY ----------------
def Deliver(request):
    global deliver_address, deliver_time

    deliver_address = request.POST['t1']
    deliver_time = request.POST['t2']

    return render(request, 'Login.html', {'data': 'Login to continue'})          


        
        



        
            
