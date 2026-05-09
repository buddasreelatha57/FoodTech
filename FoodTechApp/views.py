import os
import base64
import pickle
from datetime import date

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import pyqrcode

from Blockchain import *
from Block import *


# ---------------- SAFE GLOBAL VARIABLES ----------------
uname, address, phone = "", "", ""
deliver_address, deliver_time = "", ""

# ---------------- BLOCKCHAIN SAFE INIT ----------------
blockchain = Blockchain()

BLOCKCHAIN_FILE = "blockchain_contract.txt"

try:
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "rb") as f:
            blockchain = pickle.load(f)
except:
    blockchain = Blockchain()


# ---------------- HOME ----------------
def index(request):
    return render(request, "index.html")


# ---------------- STATIC PAGES ----------------
def AddFood(request):
    return render(request, "AddFood.html")

def Login(request):
    return render(request, "Login.html")

def Admin(request):
    return render(request, "Admin.html")

def Register(request):
    return render(request, "Register.html")


# ---------------- ADD FOOD ----------------
def AddFoodAction(request):
    if request.method == "POST":
        fname = request.POST["t1"]
        batch = request.POST["t2"]
        farm = request.POST["t3"]
        expiry = request.POST["t4"]
        storage = request.POST["t5"]
        shipping = request.POST["t6"]
        price = request.POST["t7"]
        image = request.FILES["t8"]

        imagename = image.name

        data = (
            "addproduct#" + fname + "#" + batch + "#" + farm + "#" +
            expiry + "#" + storage + "#" + shipping + "#" +
            price + "#" + imagename + "#qr_" + batch + ".png"
        )

        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), "utf-8")

        blockchain.add_new_transaction(enc)
        blockchain.mine()

        blockchain.save_object(blockchain, BLOCKCHAIN_FILE)

        fs = FileSystemStorage()
        fs.save("FoodTechApp/static/products/" + imagename, image)

        qr = pyqrcode.create(fname + "," + batch + "," + farm)
        qr.png("FoodTechApp/static/products/qr_" + batch + ".png", scale=6)

        return render(request, "AddFood.html", {"data": "Food added successfully"})



# ---------------- LOGIN FIXED ----------------
def UserLogin(request):
    global uname, address, phone

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        status = "failed"

        for i in range(len(blockchain.chain)):
            if i > 0:
                b = blockchain.chain[i]
                data = base64.b64decode(b.transactions[0])
                decrypt = blockchain.decrypt(data).decode()

                arr = decrypt.split("#")

                if arr[0] == "signup":
                    if arr[1] == username and arr[2] == password:
                        status = "success"
                        uname = username
                        address = arr[5]
                        phone = arr[3]
                        break

        if status == "success":
            with open("session.txt", "w") as f:
                f.write(username)

            return render(request, "UserScreen.html", {"data": "Welcome " + username})
        else:
            return render(request, "Login.html", {"data": "Invalid login"})


# ---------------- SIGNUP ----------------
def Signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        contact = request.POST["contact"]
        email = request.POST["email"]
        address = request.POST["address"]

        data = "signup#" + username + "#" + password + "#" + contact + "#" + email + "#" + address

        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), "utf-8")

        blockchain.add_new_transaction(enc)
        blockchain.mine()
        blockchain.save_object(blockchain, BLOCKCHAIN_FILE)

        return render(request, "Register.html", {"data": "Signup successful"})


# ---------------- BOOK ORDER ----------------
def BookOrder(request):
    if request.method == "GET":
        pid = request.GET["crop"]

        user = open("session.txt").read().strip()

        today = date.today()

        data = "bookorder#" + pid + "#" + user + "#" + str(today)

        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), "utf-8")

        blockchain.add_new_transaction(enc)
        blockchain.mine()
        blockchain.save_object(blockchain, BLOCKCHAIN_FILE)

        return render(request, "UserScreen.html", {"data": "Order placed"})

        
        



        
            
