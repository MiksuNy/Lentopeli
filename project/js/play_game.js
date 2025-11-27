"use-strict";
const mainMenuElmnt = document.getElementById("mainMenu")
const loginPageElmnt = document.getElementById("loginScreen")
const buttons = document.getElementsByClassName("buttons")
const loginBtn = document.createElement("button")
const backBtn = document.createElement("button")
const input = document.createElement("input");
const form = document.getElementById("loginForm")



// Funktio piilottaa muut divit ja asettaa parametrina annetun näkyväksi
function setView(view){
    document.querySelectorAll(".view").forEach(v => {
        v.classList.remove("active")
    })
    view.classList.add("active")
}

// Funktio animoituun siirtymään näkymien välillä
function startViewWithTransition (view){
    document.startViewTransition(() => {
        setView(view)
    })
}

// Main menu div sisältö ja kuuntelijat quit game, play game buttoneille
async function MainMenu() {
    const playGameBtn = document.createElement("button")
    const quitGameBtn = document.createElement("button")

    playGameBtn.className = "btn";
    playGameBtn.type = "button";
    playGameBtn.value = "play";
    playGameBtn.textContent = "Play Game";
    quitGameBtn.className = "btn";
    quitGameBtn.type = "button";
    quitGameBtn.value = "quit";
    quitGameBtn.textContent = "Quit Game"

    buttons[0].append(playGameBtn, quitGameBtn)
    quitGameBtn.addEventListener("click", () => window.close());
    playGameBtn.addEventListener("click", () => startViewWithTransition(loginPageElmnt));
}

// Login page div sisältö ja kuuntelijat login sekä back buttonille
async function LoginPage() {
    const header = document.createElement("header");
    const h1 = document.createElement("h1");
    const buttonsClass = document.querySelectorAll(".buttons")

    h1.className = "loginPageH1";
    h1.textContent = "Login";
    input.type = "text";
    input.placeholder = "Type your username";
    input.name = "username";
    input.id = "unameInput"
    //input.required = true;

    loginBtn.textContent = "Login";
    loginBtn.type = "submit";
    loginBtn.className = "btn";
    backBtn.textContent = "Back";
    backBtn.className = "btn";

    header.appendChild(h1);
    loginPageElmnt.insertAdjacentElement("afterbegin", header);
    form.append(input, loginBtn)
    loginPageElmnt.appendChild(buttonsClass[1])
    buttons[1].appendChild(backBtn)

    backBtn.addEventListener("click", () => startViewWithTransition(mainMenuElmnt))
    form.addEventListener("submit",  function(evt) {
        const isBadWords = containsBadWords(input.value);

        // Jos käyttäjänimi tyhjä, huomautetaan siitä käyttäjälle
        if(input.value === ""){
            input.setCustomValidity("Tarkista käyttäjänimi!")
        }
        // Jos käyttäjä syöttää kirosanan, huomautetaan myös siitä
        else if (isBadWords) {
            input.setCustomValidity("Ei kirosanoja!")
        }
        // Jos checkValidity on false, näytetään käyttäjälle jompi kumpi ylläolevista viesteistä
        if (!input.checkValidity()){
            evt.preventDefault()
            form.reportValidity()
        }
        // Jos ei annettu kiellettyjä sanoja tai tyhjää, suoritetaan handleLogin
        else {
            evt.preventDefault()
            login(input.value);
        }
    });
}
// Palauttaa true jos käyttäjänimi sisältää kiellettyjä sanoja, muuten false
function containsBadWords(username) {
    const kirosanat = ["vittu", "perkele", "saatana", "paska", "helvetti"]
    return (kirosanat.some(kirosana => username.trim().toLowerCase().includes(kirosana)))
}

// Muutetaan loginBtn text contentiksi "Logging in.." ja otetaan pois käytöstä kirjautumisen ajaksi
function handleLogin() {
    loginBtn.textContent = "Logging in.."
    loginBtn.disabled = true;
}

// Haetaan endpointilta gameState eli suoritetaan varsinainen 'login' ja kommunikointi backendin kanssa
async function login (username) {
    handleLogin()
    username = username.trim();
    const endpointUrl = "http://127.0.0.1:5000/login/"
    const response = await fetch(endpointUrl+username, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }
    })
    const gameState = await response.json()
    console.log(gameState)
}
function main(){
    MainMenu()
    LoginPage()
}

main()