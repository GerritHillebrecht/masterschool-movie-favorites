const add_movie_btn = document.getElementById("add_movie_btn")
const movie_data_ref = document.getElementById("movie_data")
const movie_data = JSON.parse(movie_data_ref.querySelector("code").innerHTML)
const movie_form = document.forms.movie_form

movie_form.addEventListener("submit", async (event) => {
    event.preventDefault()

    const user = localStorage.getItem("selectedUser")
    const userData = JSON.parse(user)

    const movie = {
        user_id: userData.id,
        name: movie_form.title.value,
        poster: movie_form.poster.value,
        rating: movie_form.rating.value,
        plot: movie_form.plot.value,
        release_year: movie_data.Released,
        actors: movie_data.Actors,
        writers: movie_data.Writer,
        boxOffice: movie_data.BoxOffice,
        genre: movie_data.Genre,
        awards: movie_data.Awards
    }


    const added_movie = await add_movie_to_database(movie, userData.id)

    if (added_movie) {
        window.location.assign(`/movie/${added_movie.id}`)
    }
})

async function add_movie_to_database(movie, userId) {
    const res = await fetch(`http://localhost:5002/api/v1/users/${userId}`, {
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