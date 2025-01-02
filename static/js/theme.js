const darkModeButton = document.getElementById("dark-mode")
const lightModeButton = document.getElementById("light-mode")

darkModeButton.addEventListener("click", (e) => {
    document.documentElement.classList.add("dark")
})

lightModeButton.addEventListener("click", (e) => {
    document.documentElement.classList.remove("dark")
})