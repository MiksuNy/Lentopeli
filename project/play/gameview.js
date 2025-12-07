const api = "http://127.0.0.1:5000"


var airplane_icon = L.icon({
    iconUrl: '../res/airplane.png',
    popupAnchor:  [12, 12]
});

var airport_icon = L.icon({
    iconUrl: '../res/airport.png',
    iconSize:     [32, 32],
    popupAnchor:  [-10, -10]
})
var map = L.map('map').setView([51.505, -0.09], 3);



function initial_draw() {
    
    
    document.getElementById("store-button").addEventListener("click", function (event) {
        document.getElementsByClassName("store")[0].style.display = "block"
    })
    
    document.getElementById("close-store-button").addEventListener("click", function(event) {
        document.getElementsByClassName("store")[0].style.display = "none"
    })
    
    
    
    var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 17,
        attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    })
    
    OpenTopoMap.addTo(map)
    
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

}



function clickedAirport(e) {
    console.log(e)
}

async function updateCounters(){
    var money = NaN
    var days = 0
    
    money = await fetch(api + "/balance/get/" + getCookie("id"))
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json()
    })
    .then((res) => {
        console.log(res)
        document.getElementById("money_amount").innerText = res
    }
)
}

async function drawOwnedAirports() {



    try {
        const response = await fetch(api + "/airports/getOwned/" + getCookie("id"));

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const json = await response.json();
        console.log(json);

        for (i = 0; i < json.length; i++){
            var marker = L.marker([json[i][0][4], json[i][0][5]], {icon: airport_icon}).bindPopup(json[i][0][3]).addTo(map)
        }


    } catch (error) {
        console.error("Fetch error:", error);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
}

initial_draw()
updateCounters()
drawOwnedAirports()









