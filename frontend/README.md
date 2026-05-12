<div align="center">
  <img src="./public/favicon.png" alt="MeloTech Logo" width="120" />
  <h1>MeloTech - Frontend</h1>
  <p>A simple, smart web app that generates thoughtful interview questions based on a job title.</p>
  <br />
  <p>
    <a href="https://melotech.vercel.app/"><strong>🌐 Live App</strong></a>
  </p>
</div>

---

## What is this?

This is the user-facing side (frontend) of the **MeloTech** application. It provides a clean, distraction-free interface where you can enter the title of a role you are hiring for (like "Customer Success Manager" or "Software Engineer"). 

Once you type in the role and click "Generate", this application securely asks the backend server to create three highly relevant, professional interview questions. It even shows you a nice loading animation with helpful status messages while it works!

**Key Features:**
- **Simple Design:** A clean layout with a crisp white and mint-green color scheme.
- **Dark Mode:** Automatically adjusts to your system preference, and includes a toggle button so you can switch between light and dark modes instantly.
- **Safe & Secure:** Built-in safeguards prevent the app from accepting invalid or overly long text, protecting the system from errors before they even happen.

---

## How to Set It Up Locally

If you want to run this application on your own computer, follow these simple steps:

### 1. Prerequisites
Make sure you have [Node.js](https://nodejs.org/) installed on your computer.

### 2. Install the Project
Open your terminal, ensure you are inside the `frontend` folder, and run the following command to download all the necessary project files:

```bash
npm install
```

### 3. Set Up Your Environment
The frontend needs to know where the backend server is located in order to get the questions. 
We have provided an example configuration file for you.

Copy the `.env.example` file and create a new file named `.env`:

```bash
cp .env.example .env
```

If you open the new `.env` file, it should look like this:
```
VITE_API_BASE_URL=http://localhost:8000
```
*(This assumes your backend will eventually be running on port 8000 on your computer).*

### 4. Start the Application
Once everything is installed and your `.env` file is ready, you can start the application:

```bash
npm run dev
```

Your terminal will provide you with a local link (usually `http://localhost:5173`). Click that link or paste it into your browser, and you will see MeloTech running live!

---

## Built With
- **React** for building the user interface.
- **Tailwind CSS** for the beautiful styling and dark mode features.
- **Vite** to make the development process fast and smooth.
- **Geist Font** for clean, modern typography.
- **Lucide Icons** for the crisp buttons and visual elements.
