# Better-Software-Task-2
Task 2 — README (Frontend: Comment UI)

Task 2: Frontend UI for Comment CRUD

This pull request adds a complete React UI for creating, editing, and deleting comments on tasks. It consumes the backend APIs built in Task 1 and integrates smoothly into the existing frontend structure.


---

📌 Features Implemented

Comment UI

Add new comment under a task

Edit comment inline

Delete comment with confirmation

Display updated list without page refresh

Error and loading states



---

📌 Project Structure

frontend/
 ├── src/
 │   ├── components/
 │   │   └── Comments/
 │   │       ├── CommentList.jsx
 │   │       ├── CommentItem.jsx
 │   │       └── AddCommentForm.jsx
 │   └── api/comments.js
 └── ...


---

📌 Key Decisions

1. Used modularized component structure to keep UI maintainable.


2. Added lightweight state management using React hooks, avoiding unnecessary libraries.


3. Reused existing design patterns and code style already present in the template.


4. Implemented optimistic UI updates for better UX.


5. Ensured reusable API functions for all operations.




---

📌 How It Works

Comments load automatically when a task is opened.

Users can:

Add new comments

Edit an existing comment through inline input

Delete with a single click


UI updates immediately using React state.



---

📌 API Consumption

Used the following endpoints:

Purpose	Method	Endpoint

Fetch comments	GET	/tasks/<id>/comments
Add comment	POST	/tasks/<id>/comments
Edit comment	PUT	/comments/<id>
Delete comment	DELETE	/comments/<id>



---

📌 How to Run Locally

cd frontend
npm install
npm start


---

📌 Assumptions

Task detail page already exists (as per template).

Comments are displayed underneath each task.

Minimal UI styling added to maintain consistency with template.



---

📌 Summary

This PR introduces a clean, intuitive, and responsive UI for managing comments. It fully integrates with the backend APIs, demonstrates clear component structure, and enhances the task management workflow.


---
