"use-strict";
const mainMenu = document.getElementById("mainMenu")
const loginPage = document.getElementById("loginScreen")


function showView(view){
    document.querySelectorAll(".view").forEach(v => {
        v.classList.remove("active")
    })
    view.classList.add(".active")
}

async function showMainMenu() {
    const playGameBtn = document.createElement("button")
    const quitGameBtn = document.createElement("button")
    const buttons = document.getElementsByClassName("buttons")

    playGameBtn.className = "btn";
    playGameBtn.type = "button";
    playGameBtn.value = "play";
    playGameBtn.textContent = "Play Game";
    playGameBtn.style.width = "130px";
    playGameBtn.style.height = "40px";


    quitGameBtn.className = "btn";
    quitGameBtn.type = "button";
    quitGameBtn.value = "quit";
    quitGameBtn.textContent = "Quit Game"
    quitGameBtn.style.width = "130px";
    quitGameBtn.style.height = "40px";

    buttons[0].append(playGameBtn, quitGameBtn)

    quitGameBtn.addEventListener("click", () => window.close())
    playGameBtn.addEventListener("click", () => showView(loginPage))

}

async function showLoginPage(){




}

function main(){
    showMainMenu()
}

main()