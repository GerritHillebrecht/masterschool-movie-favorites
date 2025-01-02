import {deleteMovie} from "./api.js"

const deleteButton = document.querySelector("#deleteButton")

deleteButton.addEventListener("click", (event) => handleDeleteClick(event.target.dataset.movieId))

async function handleDeleteClick(movieId) {
    if (!confirm(`Do you really want to delete movie with id ${movieId}`)) {
        return
    }

    await deleteMovie(movieId)

    return window.location.assign("/")
}

