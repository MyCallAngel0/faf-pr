from django.shortcuts import render


def chat_main(request):
    return render(request, 'main.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

