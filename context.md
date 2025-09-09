# Project Context

## Project Goal
To build an on-device, multi-modal, adaptive learning app for a Socratic Math Tutor, a text-based emotional check-in, and a concept weaving explore feed. The MVP will run fully on-device using lightweight, open-source models.

## Architecture


## Current Status
**Story 1.1: Core Framework Setup**
* **Status:** Done ✅
* **Notes:** All core folders and initial documentation have been successfully created.

---

**Story 1.2: Socratic Tutor**
* **Status:** Done ✅
* **Notes:** The backend API (`/tutor/ask`) has been successfully implemented using Mistral 7B. The Flutter frontend has a functional chat interface that communicates with the backend, completing the full user story.

---

**Sprint 2: Inner World & Launchpad Integration**
* **Status:** In Progress
* **Notes:** We have completed the backend and database setup for the Emotional GPS check-in and the corresponding frontend UI to finish this user story. End-to-end testing confirms that both the Socratic Tutor and Emotional GPS backend endpoints are fully functional.

---

## Detailed Development Log

### **User Story 1.1: Project Core Framework & Version Control**
* **Goal:** Establish a stable foundation for the project with proper version control and documentation.
* **Steps Taken:**
    * Initialized a new Git repository.
    * Created a `.gitignore` file to manage unwanted files.
    * Established a core folder structure (`frontend`, `backend`, `models`, `docs`, `data`).
    * Created and committed initial `README.md` and `context.md` files.
* **Rationale:** This provided the necessary structure for the project and ensures we have a versioned, single source of truth for all code and documentation.

### **User Story 1.2: Socratic Math Tutor**
* **Goal:** Implement the core Socratic tutoring chat functionality, connecting a powerful LLM to a user-facing chat interface.
* **Backend Setup:**
    * Used a Python virtual environment to manage dependencies (`fastapi`, `uvicorn`, `llama-cpp-python`).
    * Downloaded the `Mistral 7B Instruct` GGUF model.
    * Created a `main.py` file to handle model loading and expose the `/tutor/ask` endpoint.
* **Frontend Setup:**
    * Added the `http` package to `pubspec.yaml`.
    * Created a `ChatScreen` widget to serve as the chat interface.
    * Wrote the logic to send `POST` requests to the backend endpoint and display the responses.
* **Rationale:** FastAPI and Flutter were chosen for their respective strengths in backend performance and cross-platform UI development. The `llama-cpp-python` library provides efficient, on-device model inference.

### **User Story 2.1: Emotional GPS**
* **Goal:** Enable users to record and track their emotional state via a daily text check-in.
* **Backend Setup:**
    * Installed `SQLAlchemy` for database management.
    * Updated `main.py` with database setup for a `UserEmotion` table and a placeholder `POST /checkin/emotional` endpoint.
* **Frontend Setup:**
    * Created a new Dart file (`emotional_checkin_screen.dart`) with a UI for the check-in.
    * Modified `main.dart` to include a new `HomeScreen` widget for navigation with buttons for both the Socratic Tutor and Emotional GPS screens.
* **Rationale:** SQLite offers a lightweight, file-based database ideal for on-device use. The modular frontend setup in Flutter adheres to best practices for building scalable applications.

### **User Story 2.2: Explore Feed & Concept Weaving**
* **Goal:** Implement the "magic glue" that connects learned concepts to relevant content in an Explore Feed.
* **Backend Setup:**
    * Created a static `data/explore_feed.json` file to act as the curated content database.
    * Implemented `FuzzyWuzzy` for robust keyword matching in the `weave_concepts` function.
    * Updated `main.py` with new logic to load the JSON file at startup.
    * Created a new `GET /feed/explore/{tags}` endpoint to retrieve content based on tags.
    * Modified the `ask_tutor` endpoint to call `weave_concepts` and return the relevant tags in the response.
* **Frontend Setup:**
    * Created a new Dart file (`explore_feed_screen.dart`) with a UI to display content items.
    * Added the `url_launcher` package to open links.
    * Modified `main.dart` to include a button on the `HomeScreen` that navigates to the `ExploreFeedScreen` with some predefined tags.
* **Rationale:** This feature is the core differentiator of our app. Using a static JSON file and simple keyword matching is the perfect MVP approach. It proves the concept without the complexity of a real-time CMS or a full-scale recommender system. The modular frontend setup ensures the app remains organized as we add more features.

### **Parallel Teaching Summary**

* **Flutter `Navigator`:** A fundamental concept in Flutter for managing app navigation. It operates like a stack, where new screens are `pushed` onto the stack and old screens are `popped` off. We use `MaterialPageRoute` to define the transition to a new screen.

***

Please proceed with the frontend implementation. Once you have tested the new `ExploreFeedScreen` and it successfully loads content from your backend, let me know.