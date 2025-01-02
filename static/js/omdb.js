import {API_URI, MIN_CHAR_SEARCH, DEBOUNCE_DELAY} from "./settings.js"

const search_main = document.getElementById("search_main");
const search_container = document.getElementById("search_results");
const search_content_container = search_container.querySelector(".search-content-container")

const searchInput = document.getElementById("default-search");
searchInput.addEventListener("keyup", handleSearchbarInput);


let debounceTimeout;
let currentAbortController;


async function handleSearchbarInput ({ target: { value } }) {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(async () => {
    if (value.length >= MIN_CHAR_SEARCH) {
      if (currentAbortController) {
        currentAbortController.abort();
      }

      currentAbortController = new AbortController();
      const { signal } = currentAbortController;

      try {
        search_content_container.innerText = "";
        search_content_container.appendChild(create_loader());

        const movie = await fetch_movies(value, signal);

        search_content_container.innerText = "";

        if (movie.name) {
          search_content_container.appendChild(create_search_result(movie));
        } else {
          const not_found_message = document.createElement("p");
          not_found_message.className = "uppercase text-xs font-bold tracking-widest text-center"
          not_found_message.textContent = `No movie found with title "${value}"`;

          search_content_container.appendChild(not_found_message);
        }
      } catch (error) {
        if (error.name === "AbortError") {
          console.log("Fetch aborted");
        } else {
          console.error("Fetch error:", error);
        }
      }
    }
  }, DEBOUNCE_DELAY);
}

search_main.addEventListener("focusin", () => {
  search_container.classList.add("show-searchbar");
});

search_main.addEventListener("focusout", () => {
    setTimeout(() => {
        search_container.classList.remove("show-searchbar")
    }, 100)
})

// This code was written before i looked deeper into jinja and it felt wrong to delete it.
function create_search_result(movie) {
  const movie_container = document.createElement("div");
  movie_container.className =
    "grid grid-cols-[1fr,2fr] gap-4";

  const movie_poster = document.createElement("img");
  movie_poster.className = "rounded block w-full";
  movie_poster.src = movie["poster"];
  movie_poster.alt = movie["name"];

  const content_container = document.createElement("div");
  content_container.className = "content";

  const title = document.createElement("h5");
  title.className = "font-bold text-xl";
  title.textContent = movie["name"];

  const description = document.createElement("p");
  description.className = "line-clamp-4 text-sm";
  description.textContent = movie["plot"];

  const add_movie_button = document.createElement("button");
  add_movie_button.className =
    "pointer-events-auto mt-2 px-3 py-2 text-xs font-medium text-center text-white bg-primary-700/80 rounded-full hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800";
  add_movie_button.type = "button";
  add_movie_button.textContent = "Add Movie";
  add_movie_button.onclick = () =>
    (window.location.href = `/add-movie?title=${movie["name"]}`);

  content_container.appendChild(title);
  content_container.appendChild(description);
  content_container.appendChild(add_movie_button);

  movie_container.appendChild(movie_poster);
  movie_container.appendChild(content_container);

  return movie_container;
}

function create_loader() {
  const loader_container = document.createElement("div");
  loader_container.className = "flex items-center justify-center"
  loader_container.role = "status";

  const svg_item = document.createElement("svg");
  svg_item["aria-hidden"] = "true";
  svg_item.className =
    "w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-primary-600";
  svg_item.viewBox = "0 0 100 101";
  svg_item.fill = "none";
  svg_item.xmlns = "http://www.w3.org/2000/svg";

  const path_1 = document.createElement("path");
  path_1.d =
    "M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z";
  path_1.fill = "currentColor";

  const path_2 = document.createElement("path");
  path_2.d =
    "M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z";
  path_2.fill = "currentColor";

  svg_item.appendChild(path_1);
  svg_item.appendChild(path_2);

  const sr_span = document.createElement("span");
  sr_span.className = "sr-only";
  sr_span.textContent = "Loading...";

  loader_container.appendChild(svg_item);
  loader_container.appendChild(sr_span);

  loader_container.innerHTML = `<svg aria-hidden="true" role="status" class="inline w-4 h-4 me-3 animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
<path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
</svg>`

  return loader_container;
}

async function fetch_movies(search_string, signal) {
  const search_url = `${API_URI}t=${search_string}`;
  const res = await fetch(search_url, { signal });

  if (!res.ok) {
    throw new Error("Network response was not ok");
  }

  const movie = await res.json();

  console.log(movie);

  return {
    name: movie["Title"],
    actors: movie["Actors"],
    writer: movie["Writer"],
    rated: movie["Rated"],
    plot: movie["Plot"],
    poster: movie["Poster"],
    rating: movie["Ratings"]?.filter(
      (rating) => rating["Source"] == "Internet Movie Database"
    )?.[0]?.["Value"],
    release_year: movie["Year"],
    director: 1,
  };
}
