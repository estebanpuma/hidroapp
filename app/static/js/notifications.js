document.addEventListener('DOMContentLoaded', function() {
    
    console.log("inicia addevent listener de notification")

    

    const bellContainer = document.getElementById('bell-container');

    const notificationSpan = document.getElementById("notifications_container");

    function get_notifications () {
        fetch("/get_notifications")
        .then(response => response.json())
        .then(data =>{
            console.log(data)

        if (data.total_notifications>0){

            
            notificationSpan.className = "position-absolute top-2 start-90 mt-2 translate-middle badge rounded-pill bg-danger";
            notificationSpan.textContent = data.total_notifications; 
            
        }else{
            notificationSpan.innerHTML = ""
            notificationSpan.className="visually-hidden";
        }

        const notificationList = document.getElementById("notificationList");
        notificationList.innerHTML = '';
        data.notifications.forEach((notification, index) => {

            const li = document.createElement('li');
            li.setAttribute('id', `notification-${index}`);
            li.className = "list-group-item"
            if(notification.is_read !== true){
                li.setAttribute("class", "list-group-item list-group-item-secondary");
            }
            const a = document.createElement("a");
            
            a.className = "text-decoration-none text-black d-flex justify-content-between align-items-start";
            a.href = `/read_notification/${notification.id}`
            const divNotificationContent = document.createElement("div");
            divNotificationContent.className = "ms-2 me-auto";
            const divNotificationButton = document.createElement("div");
            divNotificationButton.className = "";
            divNotificationButton.textContent="...";

            const divMessage = document.createElement("div");
            divMessage.className = "fw-medium fs-6";
            divMessage.textContent = notification.message;
            const divActivity = document.createElement("div");
            divActivity.className = "fw-normal fs-6 row ";
            const divActivityText = document.createElement("div");
            divActivityText.className = "d-inline-block text-truncate"
            divActivity.style ="max-width: 250px";
            divActivityText.textContent = notification.activity;
            const divDate = document.createElement("div");
            divDate.textContent =  notification.created_at;
            divDate.className = "fs-6 fst-italic text-muted";
            const i = document.createElement("i")
            i.className = "bi bi-person-circle fs-1"

            divActivity.appendChild(divActivityText);
            divNotificationContent.appendChild(divMessage);
            divNotificationContent.appendChild(divActivity);
            divNotificationContent.appendChild(divDate);

            a.appendChild(i);
            a.appendChild(divNotificationContent);
            a.appendChild(divNotificationButton);

            li.appendChild(a);

            notificationList.appendChild(li);   
        }
        );

    })
    .catch(error => console.error('Error:', error));
    }
    
    get_notifications();

    setInterval(get_notifications, 1000000);

    bellContainer.addEventListener("click", function() {
        get_notifications()
        fetch("/check_notifications")
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        get_notifications()
    })

})