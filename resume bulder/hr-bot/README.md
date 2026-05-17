# HR Bot Dashboard

A modern, dynamic, front-end web application that simulates an advanced Human Resources dashboard. It includes features for leave management, automated AI document verification, HR extension requests, and IT service applications.

## 🚀 Features Implemented

### 1. Dynamic User Switching
- The application uses client-side JavaScript to simulate an active database of employees (`data.js`).
- Users can switch between employees (e.g., John Doe, Alice Smith) via a top-right dropdown menu.
- The dashboard, credentials, and leave balances instantly update to reflect the selected profile.

### 2. Advanced Leave Management System
- **Calculated Balances:** Displays Paid Leave (20 days) and Casual Leave (10 days) using circular progress rings.
- **Date Automation:** When applying for a leave, users input the Number of Days and select a Start Date. The system automatically calculates and formats the End Date.
- **Maternity Leave & Gender Gating:** Female employees automatically have access to a "Maternity Leave" option with an allocated 180-day balance. Male employees do not see this option.
- **Persistent Storage:** Leave applications dynamically deduct balances and save the history to the browser's `localStorage`. Refreshing the page does not wipe the data.

### 3. Simulated AI Document Verification
- If a user applies for Maternity Leave, they are required to upload a "Medical Certificate PDF".
- Uploading a file triggers a mock **AI Agent Verification** process.
- A loading state simulates an AI model checking the document for authenticity before returning a success or failure result, preventing submission if the document is deemed "fake".

### 4. HR Extension Request (Exception Handling)
- If an employee attempts to apply for more leaves than their balance allows, they are blocked.
- Instead of just failing, an **HR Request Modal** pops up.
- This modal allows the employee to draft an email request directly to HR, categorized by reason (e.g., Health, Marriage, Accident, Family Function), sending the request to a "Pending HR Review" state.

### 5. IT Services & Performance Tracking
- **IT Requests:** Includes forms to order replacement laptops or apply for new physical ID cards.
- **Performance Tab:** Displays the employee's current project deadline, work progress percentage, and an overall star rating score.

### 6. Emergency Contacts
- A dedicated HR Support Widget is embedded in the bottom left of the sidebar, displaying the HR Manager's name (Ramu), email, and phone number for immediate assistance.

## 📁 File Structure
- `index.html`: The core structural layout of the dashboard, including the sidebar, header, and hidden modals.
- `styles.css`: Contains all visual styling, modern glassmorphism effects, flexbox grids, and UI animations.
- `script.js`: The central logic engine handling DOM manipulation, event listeners, AI simulation delays, and UI updates.
- `data.js`: The dummy database containing the array of employee profiles and handling the `localStorage` initialization.

## 🛠️ Tech Stack
- **HTML5**
- **Vanilla CSS3** (No external frameworks like Tailwind/Bootstrap used)
- **Vanilla JavaScript** (ES6+)
- **FontAwesome** (Icons)
- **Google Fonts** (Inter Typography)

## 🏃 How to Run
Since this is a client-side only application, there is no need for a Node.js server or Python backend. 
Simply navigate to the project directory and double-click `index.html` to open it in any modern web browser (Chrome, Edge, Safari, Firefox).
