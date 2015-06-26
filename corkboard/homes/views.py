from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseGone, HttpResponseNotFound
from django.http import HttpResponseRedirect, HttpResponseForbidden 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Category, Pin, Board, PinToBoard
from django.core.urlresolvers import reverse


def index(request):
    return render(request, 'homes/index.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        # POST
        username = request.POST['username']
        password = request.POST['password']
        try:
            next_href = request.GET['next']
        except KeyError:
            next_href = "/home/%s" % username
        u = authenticate(username=username, password=password)
        if u is not None:
            if u.is_active:
                # success
                auth_login(request, u)
                return redirect(next_href)
            else:
                # disabled account
                return HttpResponseGone('Inactive user.')
        else:
            # invalid login
            return HttpResponseForbidden('Access Denied.')
    elif request.method == 'GET':
        # GET
        try:
            next_href = request.GET['next']
        except KeyError:
            next_href = None
        return render(request, 'homes/login.html', {'next_href': next_href})

def user(request, user_name):
    if request.user.is_authenticated():
        # a user is logged in
        if request.user.username == user_name:
            # correct user
            user = get_object_or_404(User, username=user_name)
            boards = Board.objects.filter(owner=user)
            board_dict = {}
            for b in boards:
                pin_to_boards = PinToBoard.objects.filter(board=b)
                board_dict[b] = pin_to_boards
            loose_pins = Pin.objects.exclude(pintoboard__board=boards)
            return render(request, 
                    'homes/user.html',
                    {
                        'user': user,
                        'board_dict': board_dict,
                        'boards': boards,
                        'loose_pins' : loose_pins
                    }
                )
        else:
            # incorrect user
            return HttpResponseForbidden('Unauthorized User')
    else:
        # a user is not logged in
        return redirect('/login/?next=%s' % request.path)

def pin(request, pin_id):
    if request.user.is_authenticated():
        p = get_object_or_404(Pin, id=pin_id)
        # Determine if already pinned for this user
        pin_to_boards = PinToBoard.objects.\
                filter(pin_id=pin_id).\
                filter(board__owner=request.user)
        if len(pin_to_boards) == 0:
            # not pinned to anything for this user
            current_board = None
            available_boards = Board.objects.filter(owner=request.user)
        else:
            # already pinned to a board for this user
            current_board = pin_to_boards[0].board
            available_boards = None
        return render(request, 'homes/pin.html', 
                {
                    'pin': p,
                    'current_board' : current_board,
                    'available_boards' : available_boards
                })
    else:
        # redirect to login
        return redirect('/login/?next=%s' % request.path)

def board(request, board_name):
    if request.user.is_authenticated():
        # a user is logged in
        board = get_object_or_404(Board, name=board_name)
        if board.owner.username == request.user.username:
            # correct user
            pin_to_boards = PinToBoard.objects.filter(board__name=board_name)
            return render(request, 
                    'homes/board.html',
                    {
                        'board': board,
                        'pin_to_boards': pin_to_boards
                    }
                )
        else:
            # incorrect user
            return HttpResponseForbidden('Unauthorized User')
    else:
        # a user is not logged in
        return redirect('/login/?next=%s' % request.path)

def pintoboard(request, pin_id):
    # check authentication first
    if request.user.is_authenticated():
        # a user is logged in
        # see if pin exists
        pin = get_object_or_404(Pin, id=pin_id)
        # see if board is owned by user
        try:
            board_id = request.POST['board_id']
            board = get_object_or_404(Board, id=board_id)
        except KeyError:
            # does not exist
            return HttpResponseNotFound('Board Not Found')
        if board.owner.username != request.user.username:
            # user does not own the board
            return HttpResponseForbidden('User Does Not Own Board')
        else:
            # user does own the board
            pintoboard = PinToBoard(pin=pin,
                            board=board)
            pintoboard.save()
            return redirect('/home/%s' % request.user.username)
    else:
        # a user is not logged in
        return redirect('/login/?next=%s' % request.path)

def unpin(request, pin_id):
    # check authentication first
    if request.user.is_authenticated():
        # a user is logged in
        # see if pin exists
        pin = get_object_or_404(Pin, id=pin_id)
        # see if pintoboard(s) owned by user
        pintoboards = PinToBoard.objects.\
                filter(pin=pin,
                        board__owner=request.user)
        if len(pintoboards) == 0:
            # does not exist
            return HttpResponseNotFound('Pin By User Not Found')
        elif len(pintoboards) > 1:
            # too many matches
            return HttpResponseForbidden('Too Many Pins By User Found')
        else:
            # just one match
            pintoboards[0].delete()
            return redirect('/home/%s' % request.user.username)
    else:
        # a user is not logged in
        return redirect('/login/?next=%s' % request.path)

