function clickedAirport(e) {
    console.log(e)
}


// IKONIT

var airplane_icon = L.icon({
    iconUrl: '../res/airplane.png',
    popupAnchor:  [12, 12]
});

var airport_icon = L.icon({
    iconUrl: '../res/airport.png',
    iconSize:     [32, 32],
    popupAnchor:  [-10, -10]
})


document.getElementById("store-button").addEventListener("click", function (event) {
    document.getElementsByClassName("store")[0].style.display = "block"
})

document.getElementById("close-store-button").addEventListener("click", function(event) {
    document.getElementsByClassName("store")[0].style.display = "none"
})


var map = L.map('map').setView([51.505, -0.09], 3);

var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
	maxZoom: 17,
	attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
})

OpenTopoMap.addTo(map)

var marker = L.marker([51.515, -0.09], {icon: airplane_icon}).addTo(map)
    .bindPopup("Lentokone")
    .on('click', clickedAirport)

marker.setRotationAngle(45)

var marker2 = L.marker([51.515, -0.19], {icon: airport_icon}).addTo(map)
    .bindPopup("Lentokenttä")
    .on('click', clickedAirport)

var audio = new Audio("../res/bg.wav");

document.getElementById("mutebtn").addEventListener("click", function(event) {
    if (audio.paused || audio.volume == 0.0) {
        document.getElementById("mute-icon").setAttribute("src", "../res/unmute.png")
        audio.play()
        audio.volume = 1
    }
    else {
        audio.volume = 0.0
        document.getElementById("mute-icon").setAttribute("src", "../res/mute.png")
    }
})









