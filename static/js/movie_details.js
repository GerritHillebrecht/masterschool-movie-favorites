import {deleteMovie} from "./api.js"

const deleteButton = document.querySelector("#deleteButton")

deleteButton.addEventListener("click", (event) => handleDeleteClick(event.target.dataset.movieId))

async function handleDeleteClick(movieId) {
    if (!confirm(`Do you really want to delete movie with id ${movieId}`)) {
        return
    }

    console.log("deleting")
    const deleted_movie = await deleteMovie(movieId)
    console.log("deletion complete")
    console.log(deleted_movie)

    return window.location.assign("/")
}

