var track_from = document.getElementById("track")
var InputOrderId  = document.getElementById("InputOrderId")
var showTrack  = document.getElementById("showTrack").childNodes



track_from.addEventListener("submit", (event) => {
    event.preventDefault();
    if(InputOrderId.value.length == 0){
        alert("Вкажіть номер замолення")
    }else{
        send_track_to_serve()
    }
});


function send_track_to_serve(){
    fetch("/track_order", {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        id_order: InputOrderId.value
    })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Помилка: '+data.error);
        } else {
            show_result(data.result)
        }
    })
    .catch(error => {
        alert('Помилка при відправленні запиту: '+error);
    });
}

function show_result(order){
    showTrack[1].innerText = order.id_order
    showTrack[3].innerText = order.color
    showTrack[5].innerText = order.weight
    showTrack[7].innerText = order.price
    showTrack[9].innerText = order.address
    showTrack[11].innerText = order.status
}