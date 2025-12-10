const api = "http://api.flight_game.com"


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
var airplane_markers = L.layerGroup();
var airport_markers = L.layerGroup();



function initial_draw() {
    document.getElementById("store-button").addEventListener("click", function (event) {
        document.getElementsByClassName("store")[0].style.display = "block"
    })
    
    document.getElementById("close-store-button").addEventListener("click", function(event) {
        document.getElementsByClassName("store")[0].style.display = "none"
    })
    
    document.getElementById("next-turn-button").addEventListener("click", function(event) {
        nextTurn()
    })
    
    var OpenTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 17,
        attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    })
    
    OpenTopoMap.addTo(map)
    map.addLayer(airplane_markers);
    map.addLayer(airport_markers);
    
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
    await fetch(api + "/balance/get/" + getCookie("id"))
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json()
    })
    .then((res) => {
        console.log(res)
        document.getElementById("money_amount").innerText = res
    })
    await fetch(api + "/game/getCompletedTurns/" + getCookie("id"))
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json()
    })
    .then((res) => {
        console.log(res)
        document.getElementById("days_amount").innerText = res
    })
}

async function drawOwnedAirplanes() {
    try {
        const airplaneResponse = await fetch(api + "/airplanes/getOwned/" + getCookie("id"));

        if (!airplaneResponse.ok) {
            throw new Error(`HTTP Error: ${airplaneResponse.status}`);
        }

        airplane_markers.clearLayers();

        const airplaneJson = await airplaneResponse.json();
        console.log(airplaneJson);

        for (let i = 0; i < airplaneJson.length; i++){
            const airportResponse = await fetch(api + "/airports/get/" + airplaneJson[i][2]);
            if (!airportResponse.ok) {
                throw new Error(`HTTP Error: ${airportResponse.status}`);
            }
            const airportJson = await airportResponse.json();
            console.log(airportJson)
            
            var marker = L.marker([airportJson[0][4], airportJson[0][5]], {icon: airplane_icon, rotationAngle: Math.random() * 360.0}).bindPopup(airplaneJson[i][3] + " " + airplaneJson[i][0]).addTo(airplane_markers)
        }

    } catch (error) {
        console.error("Fetch error:", error);
    }
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
            var marker = L.marker([json[i][0][4], json[i][0][5]], {icon: airport_icon}).bindPopup(json[i][0][3]).addTo(airport_markers)
        }

    } catch (error) {
        console.error("Fetch error:", error);
    }
}

async function nextTurn() {
    try {
        const response = await fetch(api + "/game/nextTurn/" + getCookie("id"), {method: "POST"});

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        } else {
            map.eachLayer((layer) => {
            if (layer instanceof L.Marker) {
                layer.remove();
            }});
            drawOwnedAirplanes()
            drawOwnedAirports()
            updateCounters()
        }

    } catch (error) {
        console.error("Fetch error:", error);
    }
}

async function buyAirplane(airplane_id) {
    try {
        const response = await fetch(api + "/airplanes/buy/" + airplane_id + "/" + getCookie("id"), {method: "POST"});

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

    } catch (error) {
        console.error("Fetch error:", error);
    }
}

async function populateStoreLists() {
    try {
        // Jos rahat loppuu lol
        //await fetch(api + "/balance/add/100000/" + getCookie("id"), {method: "POST"});
        await wait(10)
        const ownedPlanesResponse = await fetch(api + "/airplanes/getOwned/" + getCookie("id"));
        const availablePlanesResponse = await fetch(api + "/airplanes/getAvailable/" + getCookie("id"));

        if (!availablePlanesResponse.ok) {
            throw new Error(`HTTP Error: ${availablePlanesResponse.status}`);
        }
        if (!ownedPlanesResponse.ok) {
            throw new Error(`HTTP Error: ${ownedPlanesResponse.status}`);
        }
        const ownedPlanesJson = await ownedPlanesResponse.json();
        const availablePlanesJson = await availablePlanesResponse.json();
        console.log(availablePlanesJson);
        console.log(ownedPlanesJson);

        var forSaleList = document.getElementById("airplanes-for-sale");
        var ownedList = document.getElementById("airplanes-owned");
        
        // Clearataan listat ennen kun luodaan uudet itemit
        while (forSaleList.firstChild) {
            forSaleList.removeChild(forSaleList.lastChild)
        }
        while (ownedList.firstChild) {
            ownedList.removeChild(ownedList.lastChild)
        }

        for (let i = 0; i < availablePlanesJson.length; i++){
            let item = document.createElement("li");
            item.classList.add("airplane-for-sale");
            let content = document.createTextNode(availablePlanesJson[i][0]);
            item.appendChild(content);
            forSaleList.appendChild(item);
        }

        for (let i = 0; i < ownedPlanesJson.length; i++) {
            let item = document.createElement("li");
            let content = document.createTextNode(ownedPlanesJson[i][0]);
            item.appendChild(content);
            ownedList.appendChild(item);
        }

        var airplanesForSale = document.getElementsByClassName("airplane-for-sale");
        for (var i = 0; i < airplanesForSale.length; i++) {
            airplanesForSale[i].addEventListener("click", function (event) {
                // FIXME: ei pitäis innerTextin perusteella ostaa koneita, mut tarpeeks hyvä nyt
                buyAirplane(event.target.innerText)
                
                populateStoreLists()
            })
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

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

initial_draw()
updateCounters()
drawOwnedAirports()
drawOwnedAirplanes()
populateStoreLists()