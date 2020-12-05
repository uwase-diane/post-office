from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .models import Office, Address, User, Parcel
from django.contrib.auth import authenticate, login, logout
from .utils import generate_code


def login_view(request):
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login")


def sign_in(request):
    if not request.user.is_anonymous:
        logout(request)
        return redirect("/login")
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if not user:
        return redirect("/login")
    login(request, user)

    if user.is_staff:
        return redirect("/users")

    group = user.groups.first()

    customer = Group.objects.filter(name="Customer").first()
    worker = Group.objects.filter(name="Worker").first()

    if not customer:
        customer = Group(name="Customer")
        customer.save()

    if not worker:
        worker = Group(name="Worker")
        worker.save()

    if group == customer:
        return redirect("/profile")

    if group == worker:
        return redirect("/parcels")

    logout(request)
    return redirect("/login")


def register_view(request):
    return render(request, "register.html")


def sign_up(request):
    if not request.user.is_anonymous:
        logout(request)
        return redirect("/login")

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken")

    password = data.pop("password")
    username = data.get("username")

    usr = User(**data)
    usr.set_password(password)
    usr.save()

    customer_group = Group.objects.filter(name="Customer").first()

    if not customer_group:
        customer_group = Group(name="Customer")
        customer_group.save()
        usr.groups.add(customer_group)

    user = authenticate(request, username=username, password=password)

    if not user:
        return redirect("/login")
    login(request, user)
    return redirect("/profile")


@login_required(login_url='/login')
def add_user(request):
    dt = request.POST
    data = dt.dict()
    data.pop("csrfmiddlewaretoken")
    print(data)
    gr = data.pop("group")
    group = Group.objects.filter(name=gr).first()

    if not group:
        group = Group(name=gr)
        group.save()

    password = data.pop("password")

    user = User(**data)
    user.set_password(password)
    user.save()
    user.groups.add(group)
    return redirect("/users?group=Worker")


@login_required(login_url='/login')
def get_reports(request):
    if not request.user.is_staff:
        logout(request)
        return redirect("/login")
    data = {
        "waiting": Parcel.objects.filter(status="Waiting"),
        "accepted": Parcel.objects.filter(status="Accepted"),
        "rejected": Parcel.objects.filter(status="Rejected"),
        "waiting_pickup": Parcel.objects.filter(status="Waiting pickup"),
        "checking": Parcel.objects.filter(status="Checking"),
        "on_way": Parcel.objects.filter(status="On way"),
        "delivered": Parcel.objects.filter(status="Delivered"),
    }
    return render(request, "reports.html", data)


@login_required(login_url='/login')
def get_users(request):
    data = {}
    group_name = request.GET.get('group')
    group = Group.objects.filter(name=group_name).first()
    if not group:
        return redirect("/users?group=Worker")
    users = User.objects.filter(groups=group)
    data["users"] = users
    data["group"] = group
    data["user"] = request.user
    data["groups"] = Group.objects.all()
    return render(request, "users.html", data)


@login_required(login_url='/login')
def view_profile(request):
    data = {
        "user": request.user
    }
    return render(request, "profile.html", data)


@login_required(login_url='/login')
def update_profile(request):
    data = request.POST
    user = request.user
    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.email = data.get("email")
    user.username = data.get("username")
    user.save()
    return redirect("/profile")


@login_required(login_url='/login')
def add_mail_page(request):
    data = {
        "user": request.user,
        "tracking_number": generate_code(),
        "addresses": Address.objects.filter(user=request.user).order_by("-is_default")
    }
    return render(request, "send-mail.html", data)


@login_required(login_url='/login')
def index(request):
    return redirect("/tracking")


@login_required(login_url='/login')
def tracking(request):
    data = {
        "user": request.user,
        "parcels": Parcel.objects.filter(sender=request.user) | Parcel.objects.filter(receiver=request.user)
    }
    return render(request, "tracking.html", data)


@login_required(login_url='/login')
def addresses_page(request):
    data = {
        "user": request.user,
        "addresses": Address.objects.filter(user=request.user).order_by("-is_default")
    }
    return render(request, "addresses.html", data)


@login_required(login_url='/login')
def add_address(request):
    fd = request.POST.dict()
    fd.pop("csrfmiddlewaretoken")

    try:
        if fd["is_default"] == "on":
            fd["is_default"] = True
        else:
            fd["is_default"] = False

    except:
        fd["is_default"] = False

    ad = Address(**fd)
    ad.user = request.user
    # ad.on = True
    ad.save()

    if ad.is_default:
        Address.objects.filter(user=request.user).exclude(id=ad.id).update(is_default=False)
    data = {
        "user": request.user,
        # "addresses": Address.objects.filter(user=request.user)
    }
    return redirect("/addresses")


@login_required(login_url='/login')
def address_delete(request, address_id):
    Address.objects.filter(id=address_id, user=request.user).delete()
    return redirect("/addresses")


@login_required(login_url='/login')
def address_default(request, address_id):
    ad = Address.objects.filter(id=address_id, user=request.user).first()
    if ad:
        ad.is_default = True
        ad.save()
        Address.objects.filter(user=request.user).exclude(id=ad.id).update(is_default=False)

    return redirect("/addresses")


@login_required(login_url='/login')
def add_parcel(request):
    dt = request.POST
    img = request.FILES.get("image")
    data = dt.dict()
    data.pop("csrfmiddlewaretoken")

    quantity = data.get("quantity")

    total = int(quantity) * 5000

    try:
        data.pop("image")
    except:
        pass

    data["sender_address"] = Address.objects.filter(user=request.user, id=data["sender_address"]).first()
    receiver = User.objects.filter(username=data["receiver"]).exclude(id=request.user.id).first()

    if not receiver:
        redirect("/send-mail")

    data["receiver"] = receiver
    rad = Address.objects.filter(user=receiver, is_default=True).first()
    data["receiver_address"] = rad
    data["quantity"] = float(data["quantity"])

    parc = Parcel(**data)
    parc.sender = request.user
    parc.image = img
    parc.total_price = int(total)
    print(data)
    parc.save()
    return redirect("/tracking")


@login_required(login_url='/login')
def parcel_detail(request, parcel_id):
    parcel = Parcel.objects.filter(tracking_number=parcel_id).first()
    user = request.user

    data = {
        "parcel": parcel,
        "user": user
    }

    return render(request, "parcel-detail.html", data)


@login_required(login_url='/login')
def parcel_payment(request, parcel_id):
    parcel = Parcel.objects.filter(tracking_number=parcel_id).first()
    if not parcel:
        return redirect("tracking")
    parcel.is_paid = True
    parcel.status = "Waiting pickup"
    parcel.save()
    return redirect("/parcels/{}".format(parcel_id))
