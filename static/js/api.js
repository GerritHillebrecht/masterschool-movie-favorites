
const API_PATH = "api"
const API_VERSION = "v1"
const API_URL = `${window.location.origin}/${API_PATH}/${API_VERSION}`

export async function add_user(user) {
    const res = await fetch(`${API_URL}/users`, {
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

export async function add_movie_to_database(movie, userId) {
    const res = await fetch(`${API_URL}/users/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(movie)
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

export async function deleteMovie(movieId) {
    const res = await fetch(`${API_URL}/delete_movie/${movieId}`, {
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