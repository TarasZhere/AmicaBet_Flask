from flask import Blueprint, redirect, session, url_for, request
from requests import post, get, HTTPError
from amica.server_url import SERVER_URL as URL, headers as h
from amica.auth import login_required

bp = Blueprint('bet', __name__, url_prefix='/bet')


@bp.route('create/<int:invited_Uid>', methods=['POST'])
@bp.route('create/', methods=['POST'])
@login_required
def create(invited_Uid=None):
    bet = dict(
        Uid=session.get('Uid'),
        title=request.form['title'],
        description=request.form['description'],
        ticket=int(request.form['ticket']),
        invited_Uid=invited_Uid
    )

    try:
        response = post(f'{URL}bet/create', headers=h, json=bet)
        response.raise_for_status()
    except HTTPError as e:
        print(e)
        return e, 500

    return redirect(url_for('user.homepage'))


@bp.route('accept')
@bp.route('accept/<int:Bid>')
@login_required
def accept(Bid):
    try:
        response = get(URL+f"bet/accept/{Bid}")
        response.raise_for_status()

    except HTTPError as e:
        print(e)
        return e, 500
    except Exception as e:
        print(e)
        return e, 500

    return 'Ok', 200
