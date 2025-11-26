"use-strict";
const mainMenuElmnt = document.getElementById("mainMenu")
const loginPageElmnt = document.getElementById("loginScreen")
const buttons = document.getElementsByClassName("buttons")

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

// Main menu div sisältö ja kuuntelija quit game ja play game buttoneille
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

// Login page div sisältö ja kuuntelija back buttonille
async function LoginPage(){
    const header = document.createElement("header");
    const h1 = document.createElement("h1");
    const input = document.createElement("input");
    const buttonsClass = document.querySelectorAll(".buttons")
    const loginBtn = document.createElement("button")
    const backBtn = document.createElement("button")

    h1.className = "loginPageH1";
    h1.textContent = "Login";
    input.type = "text";
    input.placeholder = "Type your username";
    input.name = "username";
    input.id = "unameInput"
    loginBtn.textContent = "LOGIN";
    loginBtn.type = "submit";
    loginBtn.className = "btn";
    backBtn.textContent = "BACK";
    backBtn.className = "btn";

    header.appendChild(h1);
    loginPageElmnt.insertAdjacentElement("afterbegin", header);
    loginPageElmnt.insertBefore(input, buttonsClass[1])
    buttons[1].append(loginBtn, backBtn)
    backBtn.addEventListener("click", () => startViewWithTransition(mainMenuElmnt))
}

function main(){
    MainMenu()
    LoginPage()
}

main()