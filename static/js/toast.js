const toastParentContainer = document.getElementById("toast-parent-container");

export function showToast({title, imageSrc, messageText}) {
  const toastContainer = document.createElement("div");
  toastContainer.id = "toast-message-cta";
  toastContainer.className =
    "w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow dark:bg-gray-800 dark:text-gray-400";
  toastContainer.role = "alert";

  const toastContent = `
        <div class="flex" id="toast-message-cta">
            <img class="w-8 h-8 rounded-full" src="${imageSrc}" alt="Profile image"/>
            <div class="ms-3 text-sm font-normal">
                <span class="mb-1 text-sm font-semibold text-gray-900 dark:text-white">${title}</span>
                <div class="mb-2 text-sm font-normal">${messageText}</div>
                <a href="#"
                   class="inline-flex px-2.5 py-1.5 text-xs font-medium text-center text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-800">Reply</a>
            </div>
            <button type="button"
                    class="ms-auto -mx-1.5 -my-1.5 bg-white justify-center items-center flex-shrink-0 text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
                    data-dismiss-target="#toast-message-cta" aria-label="Close">
                <span class="sr-only">Close</span>
                <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                </svg>
            </button>
        </div>
    `;

  toastContainer.innerHTML = toastContent;

  // Füge den Toast zum Body hinzu
  toastParentContainer.appendChild(toastContainer);

  // Schließe den Toast nach einer bestimmten Zeit (z.B. 5 Sekunden)
  setTimeout(() => {
    dismissToast();
  }, 5000);
}

function dismissToast(toastContainer) {
  if (toastContainer) {
    toastContainer.remove();
  }
}

// Funktion aufrufen, um den Toast anzuzeigen
showToast(
  "https://flowbite.com/docs/images/people/profile-picture-1.jpg",
  "Hi Neil, thanks for sharing your thoughts regarding Flowbite."
);
