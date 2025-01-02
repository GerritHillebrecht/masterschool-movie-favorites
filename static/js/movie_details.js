const deleteButton = document.querySelector("#deleteButton")

deleteButton.addEventListener("click", (event) => handleDeleteClick(event.target.dataset.movieId))

async function handleDeleteClick(movieId) {
    if (!confirm(`Do you really want to delete movie with id ${movieId}`)) {
        return
    }

    await deleteMovie(movieId)

    return window.location.assign("/")
}

async function deleteMovie(movieId) {
    const res = await fetch(`http://localhost:5002/api/v1/delete_movie/${movieId}`, {
        method: "DELETE",
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