# Habit Tracker

A full stack daily habit tracking app with user authentication. Users can register, log in, and manage their own private categories and habits with daily check-offs, streak tracking, and progress bars.

## Live Demo

[hashtagone.github.io/Habit-Tracker-Rebuild](https://hashtagone.github.io/Habit-Tracker-Rebuild/)

## Features

- User registration and login with bcrypt password hashing
- Session-based authentication with Flask-Login
- Create, edit, and delete color-coded habit categories
- Create, edit, and delete habits within categories
- Daily check-off system per habit
- Streak counter per habit — counts consecutive days completed
- Progress bar per category based on today's completions
- Inline double-click editing for category and habit names
- Confirm modal before any deletion
- Smooth animations — category slide-in from left, page crossfade transitions, modal enter/exit, progress bar fill
- Data persists in PostgreSQL — habits survive across sessions and devices
- Deployed frontend on GitHub Pages, backend and database on Render

## Tech Stack

- **Frontend:** Vue 3 (Composition API, script setup), Vue Router, Vite, CSS custom properties
- **Backend:** Python, Flask, Flask-Login, Flask-SQLAlchemy, Flask-CORS, bcrypt
- **Database:** PostgreSQL (via psycopg2)
- **Deployment:** GitHub Pages (frontend), Render (backend + database)

## What I Learned

- Building session-based authentication end to end — password hashing with bcrypt, session cookies, protected routes on both frontend and backend
- Designing a relational database schema with foreign key chains (users → categories → habits → completions) and cascade deletes
- Why cross-domain cookies require SameSite=None and Secure=True in production
- How Vue's <Transition> and <TransitionGroup> work and why CSS animations on child elements conflict with parent opacity transitions
- Using @before-leave to capture element position before position: absolute snaps it out of flow
- The difference between optimistic UI updates and server-driven state, and why the latter causes noticeable delay
- How authReady prevents the navigation guard from routing before the session check completes on refresh
