# app/socket_events.py
from flask import flash

from flask_socketio import emit, join_room

from flask_login import current_user

from app import socketio



@socketio.on('connect', namespace="/notifications")
def handle_connect():
    flash("conectadop")
    user_id = str(current_user.id)  # Convertimos el ID del usuario a string para usarlo como nombre de room
    join_room(user_id)  # El usuario se une a su propio room basado en su ID
    print(f'Cliente {user_id} conectado a las notificaciones.')
    emit('message', {'data': 'Conectado a las notificaciones en el servior'})


@socketio.on('disconnect', namespace="/notifications")
def handle_disconnect():
    print('Cliente desconectado de las notificaciones.')


@socketio.on('notify', namespace="/notifications")
def handle_notification(data):
    message = data['message']
    user_ids = data['user_ids']  # Lista de IDs de usuarios a los que se enviará la notificación
    for user_id in user_ids:
        emit('notification', {'data': message}, room=user_id, namespace='/notifications')

@socketio.on('my_event', namespace='/notifications')
def handle_my_custom_event(json):
    print('Recibido evento personalizado: ' + str(json))
    emit('my_response', {'data': 'Evento recibido'})

# Función para enviar notificaciones a un usuario específico
def send_notification(users_id, message):
    for user_id in users_id:
        emit('message', {'data': message}, room=str(user_id), namespace='/notifications')