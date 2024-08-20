document.addEventListener('DOMContentLoaded', (event) => {
   
    var socket = io('http://192.168.0.157:5000', {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000
    });
  

    socket.on('connect', function() {
        
    });

    socket.emit('my_event', {data: 'test'});
    
    socket.on('my_response', function(data) {
        console.log('Respuesta recibida:', data);
    });

   

    socket.on('message', function(data) {
        console.log('Respuesta recibida:', data);
    });

    socket.on('notify', function(data) {
        alert('Nueva notificación: ' + data.data);
        console.log("nooorrrr")
    });

   
    socket.on('disconnect', function() {
        console.log('Desconectado de las notificaciones');
    });
   
    socket.on('connect_error', (error) => {
        console.log('Error de conexión:', error);
    });
});