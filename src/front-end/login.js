'use-strict';

const mainMenuElmnt = document.getElementById('mainMenu');
const loginPageElmnt = document.getElementById('loginScreen');
const buttons = document.getElementsByClassName('buttons');
const loginBtn = document.createElement('button');
const backBtn = document.createElement('button');
const input = document.createElement('input');
const form = document.getElementById('loginForm');
const playGameBtn = document.createElement('button');
const quitGameBtn = document.createElement('button');

// Funktio piilottaa muut divit ja asettaa funktiolle annetun argumentin näkyväksi
function setView(view) {
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
    });
    form.reset();
    view.classList.add('active');
    loginBtn.textContent = 'Login';
}

// Funktio animoituun siirtymään näkymien välillä
function startViewWithTransition(view) {
    document.startViewTransition(() => {
        setView(view);
    });
}

// Main menu div sisältö ja kuuntelijat quit game, play game buttoneille
async function MainMenu() {

    playGameBtn.className = 'btn';
    playGameBtn.type = 'button';
    playGameBtn.value = 'play';
    playGameBtn.textContent = 'Play Game';
    quitGameBtn.className = 'btn';
    quitGameBtn.type = 'button';
    quitGameBtn.value = 'quit';
    quitGameBtn.textContent = 'Quit Game';
    buttons[0].append(playGameBtn, quitGameBtn);

}

// Login page div sisältö
async function LoginPage() {
    const header = document.createElement('header');
    const h1 = document.createElement('h1');
    const buttonsClass = document.querySelectorAll('.buttons');

    h1.className = 'loginPageH1';
    h1.textContent = 'Login';
    input.type = 'text';
    input.placeholder = 'Type your username';
    input.name = 'username';
    input.id = 'unameInput';

    loginBtn.textContent = 'Login';
    loginBtn.type = 'submit';
    loginBtn.className = 'btn';
    backBtn.textContent = 'Back';
    backBtn.className = 'btn';

    header.appendChild(h1);
    loginPageElmnt.insertAdjacentElement('afterbegin', header);
    form.append(input, loginBtn);
    loginPageElmnt.appendChild(buttonsClass[1]);
    buttons[1].appendChild(backBtn);

}

// Palauttaa true jos käyttäjänimi sisältää kiellettyjä sanoja, muuten false
function containsBadWords(username) {
    const kirosanat = ['vittu', 'perkele', 'saatana', 'paska', 'helvetti'];
    return (kirosanat.some(
        kirosana => username.trim().toLowerCase().includes(kirosana)));
}

// Näytetään "Logging in.." käyttäjälle ja kutsutaan login funktiota joka ottaa yhteyden backendiin
async function handleLogin(username) {
    const api = "http://api.flight_game.com:8080/"
    loginBtn.textContent = 'Logging in..';
    loginBtn.disabled = true;

    response_text = NaN

    await fetch(api + "login/" + username, { method: "POST" })
    .then((response) => {
        if (!response.ok) {
            alert("Login failed");
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json();  // Tää on ihan VITUN tyhmää. FUCK javascript. 
    })
    .then((id) => {
        document.cookie = "id=" + id[0][0]
        window.location = "./play/index.html"
    });

}

// Haetaan endpointilta gameState eli suoritetaan varsinainen 'login' ja kommunikointi backendin kanssa
async function login(username) {
    let gameState;
    let response = null;
    const endpointUrl = 'http://127.0.0.1:5000/login/';
    try {
        response = await fetch(endpointUrl + username, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Sijoitetaan backendista tuleva gamestate muuttujaan myöhempää käyttöä varten
        gameState = await response.json();
        return gameState

    } catch (error) {
        return {"Error": error};
    }
}

// Määritellään kuuntelijat buttoneille ja inputille
function addListeners() {
    quitGameBtn.addEventListener('click', () => window.close());
    playGameBtn.addEventListener('click',
        () => startViewWithTransition(loginPageElmnt));
    backBtn.addEventListener('click',
        () => startViewWithTransition(mainMenuElmnt));
    input.addEventListener('input', () => {
        input.setCustomValidity('');
    });
    loginBtn.addEventListener('click', function(evt) {
        evt.preventDefault();
        input.setCustomValidity('');
        const isBadWords = containsBadWords(input.value);

        // Jos käyttäjänimi tyhjä, asetetaan huomautusviesti
        if (input.value === '') {
            input.setCustomValidity('Tarkista käyttäjänimi!');
        }

        // Jos käyttäjä syöttää kirosanan, huomautetaan myös siitä
        else if (isBadWords) {
            input.setCustomValidity('Ei kirosanoja!');
        }

        // Jos checkValidity on false, näytetään käyttäjälle jompi kumpi ylläolevista viesteistä
        if (!input.checkValidity()) {
            form.reportValidity();
        }

        // Kutstutaan handleLogin funktiota jos username validi
        else {
            handleLogin(input.value);
        }
    });
}

function playGameMain() {
    MainMenu();
    LoginPage();
    addListeners();
}

playGameMain();