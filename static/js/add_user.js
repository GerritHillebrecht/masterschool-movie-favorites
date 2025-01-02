const add_user_form = document.forms.add_user_form

add_user_form.addEventListener("submit", (event) => {
    event.preventDefault()

    const user = {
        firstname: add_user_form.firstname.value,
        lastname: add_user_form.lastname.value
    }

    add_user(user)
})

async function add_user(user) {
    const res = await fetch("http://localhost:5002/api/v1/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    })

    if (!res.ok) {
        throw new Error("Everything broke, take your most important belongings and run!")
    }

    try {
        return await res.json()
    } catch (error) {
        console.error("Everything is fucked", error)
    }
}