import {add_user} from "./api.js"

const add_user_form = document.forms.add_user_form

add_user_form.addEventListener("submit", (event) => {
    event.preventDefault()

    const user = {
        firstname: add_user_form.firstname.value,
        lastname: add_user_form.lastname.value
    }

    add_user(user)
})

