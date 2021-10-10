from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room,Topic,Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RoomForm,UserForm


# Create your views here.
#
# rooms=[
#     {'id':1,'name':"Aviansh Ak47"},
#     {'id':2,'name':"python code"},
#     {'id':3,'name':"Django Project"},
#     {'id':4,'name':"DSA"},
#     {'id':5,'name':"Core"},
# ]

def userlogout(request):
    logout(request)
    return redirect('home')


def Registeruser(request):
    form=UserCreationForm
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Error during the registration")
    return render(request,'base/login_Reg.html',{"form":form})


def userlogin(request):
    page='login'
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User Not Found")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Recheck the credentials")
    context={'page':page}
    return render(request,'base/login_Reg.html',context=context)



def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q)|
                              Q(name__icontains=q) |
                              Q(description__icontains=q)
                              )
    topic=Topic.objects.all()
    rooms_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))

    context={'topic':topic,'rooms':rooms,'rooms_count':rooms_count,'room_messages':room_messages}
    return render(request,'base/home.html',context=context)


def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)



def profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile_old.html',context=context)




@login_required(login_url='/login')
def createRoom(request):
    rform=RoomForm(request.POST or None)
    topics=Topic.objects.all()
    if(request.method=="POST"):
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        #rform=RoomForm(request.POST)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # if rform.is_valid():
        #     room=rform.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
        rform=RoomForm()
    else:
        rform=RoomForm
    context={'rform':rform,'topics':topics}
    return render(request,'base/room_from.html',context)




@login_required(login_url='/login')
def update(request,pk):
    obj=Room.objects.get(id=pk)
    rform=RoomForm(instance=obj)
    topics = Topic.objects.all()
    if request.user !=obj.host:
        return HttpResponse("u are not permit to edit someone else account")

    if request.method=="POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # rform=RoomForm(request.POST,instance=obj)
        # if rform.is_valid():
        #     rform.save()
        obj.name=request.POST.get('name')
        obj.topic=request.POST.get('topic_name')
        obj.description=request.POST.get('description')
        obj.save()
        return redirect('home')
    context={'rform':rform,'topics':topics,'room':obj}
    return render(request,'base/room_from.html',context=context)


def msg_delete(request,pk):
    msg=Message.objects.get(id=pk)

    if request.user !=msg.user:
        return HttpResponse("Not allowed to delete")
    if request.method=="POST":
        msg.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'msg':msg})




@login_required(login_url='/login')
def delete(request,pk):
    obj=Room.objects.get(id=pk)
    if request.user != obj.host:
        return HttpResponse("u are not permit to delete someone else account")

    context={}
    if request.method=="POST":
        obj.delete()
        return redirect('home')
    return render(request,'base/delete.html',context=context)



@login_required(login_url='login')
def updaetUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)


    return render(request,'base/update-user.html',{'form':form})