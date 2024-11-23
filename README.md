# MASTERSCHOOL-MOVIE-FAVORITES

<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">MASTERSCHOOL-MOVIE-FAVORITES</h1></p>
<p align="center">
    <em><code>A web application for managing and sharing your favorite movies with other users</code></em>
</p>
<p align="center">
    <img src="https://img.shields.io/github/license/GerritHillebrecht/masterschool-movie-favorites?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
    <img src="https://img.shields.io/github/last-commit/GerritHillebrecht/masterschool-movie-favorites?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
    <img src="https://img.shields.io/github/languages/top/GerritHillebrecht/masterschool-movie-favorites?style=default&color=0080ff" alt="repo-top-language">
    <img src="https://img.shields.io/github/languages/count/GerritHillebrecht/masterschool-movie-favorites?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
    <!-- default option, no dependency badges. -->
</p>
<br>

## 🔗 Table of Contents

- [📍 Overview](#-overview)
- [👾 Features](#-features)
- [📁 Project Structure](#-project-structure)
  - [📂 Project Index](#-project-index)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#-prerequisites)
  - [⚙️ Installation](#-installation)
  - [🤖 Usage](#🤖-usage)
  - [🧪 Testing](#🧪-testing)
- [📌 Project Roadmap](#-project-roadmap)
- [🔰 Contributing](#-contributing)
- [🎗 License](#-license)
- [🙌 Acknowledgments](#-acknowledgments)

---

## 📍 Overview

The Masterschool Movie Favorites is a Flask-based web application that allows users to create and manage their personal movie collections. Users can search for movies, add them to their favorites, view other users' collections, and discover new films through the community. The application features a modern, responsive interface and integrates with a SQLite database for data persistence.

---

## 👾 Features

- User account creation and management
- Movie search functionality with detailed movie information
- Personal movie collection management
- Social features to view other users' collections
- Responsive design for desktop and mobile devices
- RESTful API for programmatic access
- Movie director information and filtering
- Custom movie recommendations based on user preferences

---

## 📁 Project Structure

```sh
└── masterschool-movie-favorites/
    ├── api
    │   ├── __init__.py
    │   ├── api_routes.py
    │   └── static_routes.py
    ├── config.py
    ├── database
    │   └── extensions.py
    ├── datamanager
    │   ├── __init__.py
    │   ├── data_manager_interface.py
    │   └── sqlite_data_manager.py
    ├── main.py
    ├── requirements.txt
    ├── schemas
    │   ├── __init__.py
    │   ├── base_schema.py
    │   ├── director_schema.py
    │   ├── movie_schema.py
    │   └── user_schema.py
    ├── static
    │   ├── css
    │   ├── js
    │   └── src
    ├── templates
    │   ├── 404.html
    │   ├── _base.html
    │   ├── components
    │   ├── home.html
    │   ├── search.html
    │   ├── user_movies.html
    │   └── users.html
    └── utils
        ├── decorators.py
        ├── filter.py
        └── to_dict_mixin_schema.py
```

### 📂 Project Index
<details open>
    <summary><b><code>MASTERSCHOOL-MOVIE-FAVORITES/</code></b></summary>
    <details>
        <summary><b>__root__</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b>config.py</b></td>
                <td>Application configuration file containing environment variables and settings</td>
            </tr>
            <tr>
                <td><b>main.py</b></td>
                <td>Main application entry point and Flask server initialization</td>
            </tr>
            <tr>
                <td><b>requirements.txt</b></td>
                <td>List of Python dependencies required for the project</td>
            </tr>
            </table>
        </blockquote>
    </details>
    <details>
        <summary><b>schemas</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b>user_schema.py</b></td>
                <td>Database schema and model for user data</td>
            </tr>
            <tr>
                <td><b>director_schema.py</b></td>
                <td>Database schema and model for movie director information</td>
            </tr>
            <tr>
                <td><b>movie_schema.py</b></td>
                <td>Database schema and model for movie information</td>
            </tr>
            <tr>
                <td><b>base_schema.py</b></td>
                <td>Base schema class with common functionality for all models</td>
            </tr>
            </table>
        </blockquote>
    </details>
    <details>
        <summary><b>templates</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b>home.html</b></td>
                <td>Homepage template with featured movies and user recommendations</td>
            </tr>
            <tr>
                <td><b>_base.html</b></td>
                <td>Base template containing common layout elements</td>
            </tr>
            <tr>
                <td><b>user_movies.html</b></td>
                <td>Template for displaying a user's movie collection</td>
            </tr>
            <tr>
                <td><b>users.html</b></td>
                <td>Template for displaying user list and profiles</td>
            </tr>
            <tr>
                <td><b>404.html</b></td>
                <td>Custom 404 error page template</td>
            </tr>
            <tr>
                <td><b>search.html</b></td>
                <td>Movie search results page template</td>
            </tr>
            </table>
            <details>
                <summary><b>components</b></summary>
                <blockquote>
                    <table>
                    <tr>
                        <td><b>footer.html</b></td>
                        <td>Reusable footer component template</td>
                    </tr>
                    <tr>
                        <td><b>navbar_menu.html</b></td>
                        <td>Navigation menu component template</td>
                    </tr>
                    <tr>
                        <td><b>user-card.html</b></td>
                        <td>User profile card component template</td>
                    </tr>
                    <tr>
                        <td><b>movie_card.html</b></td>
                        <td>Movie information card component template</td>
                    </tr>
                    <tr>
                        <td><b>search_bar.html</b></td>
                        <td>Search input component template</td>
                    </tr>
                    <tr>
                        <td><b>navbar.html</b></td>
                        <td>Main navigation bar component template</td>
                    </tr>
                    </table>
                </blockquote>
            </details>
        </blockquote>
    </details>
    <details>
        <summary><b>datamanager</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b>sqlite_data_manager.py</b></td>
                <td>SQLite database manager implementation for data persistence</td>
            </tr>
            <tr>
                <td><b>data_manager_interface.py</b></td>
                <td>Abstract interface for data management implementations</td>
            </tr>
            </table>
        </blockquote>
    </details>
    <details>
        <summary><b>utils</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b>filter.py</b></td>
                <td>Utility functions for filtering and sorting data</td>
            </tr>
            <tr>
                <td><b>decorators.py</b></td>
                <td>Custom decorators for route handling and authentication</td>
            </tr>
            <tr>
                <td><b>to_dict_mixin_schema.py</b></td>
                <td>Mixin class for converting database models to dictionaries</td>
            </tr>
            </table>
        </blockquote>
    </details>
    <details>
        <summary><b>api</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b>api_routes.py</b></td>
                <td>RESTful API route definitions and handlers</td>
            </tr>
            <tr>
                <td><b>static_routes.py</b></td>
                <td>Static page route definitions and handlers</td>
            </tr>
            </table>
        </blockquote>
    </details>
    <details>
        <summary><b>database</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b>extensions.py</b></td>
                <td>Database extension and configuration utilities</td>
            </tr>
            </table>
        </blockquote>
    </details>
</details>

---
## 🚀 Getting Started

### ☑️ Prerequisites

Before getting started with masterschool-movie-favorites, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip


### ⚙️ Installation

Install masterschool-movie-favorites using one of the following methods:

**Build from source:**

1. Clone the masterschool-movie-favorites repository:
```sh
❯ git clone https://github.com/GerritHillebrecht/masterschool-movie-favorites
```

2. Navigate to the project directory:
```sh
❯ cd masterschool-movie-favorites
```

3. Install the project dependencies:

**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```

### 🤖 Usage
Run masterschool-movie-favorites using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python main.py
```

### 🧪 Testing
Run the test suite using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pytest
```

---
## 📌 Project Roadmap

- [X] **`Core Features`**: <strike>Implement basic movie management and user authentication</strike>
- [ ] **`Social Features`**: Add user following, comments, and movie recommendations
- [ ] **`API Enhancement`**: Expand API functionality and add documentation

---

## 🔰 Contributing

- **💬 [Join the Discussions](https://github.com/GerritHillebrecht/masterschool-movie-favorites/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/GerritHillebrecht/masterschool-movie-favorites/issues)**: Submit bugs found or log feature requests for the `masterschool-movie-favorites` project.
- **💡 [Submit Pull Requests](https://github.com/GerritHillebrecht/masterschool-movie-favorites/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/GerritHillebrecht/masterschool-movie-favorites
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/GerritHillebrecht/masterschool-movie-favorites/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=GerritHillebrecht/masterschool-movie-favorites">
   </a>
</p>
</details>

---

## 🎗 License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## 🙌 Acknowledgments

- Flask framework and its community
- SQLAlchemy ORM for database management
- The movie database community for inspiration
- Contributors and testers who helped improve the application

---