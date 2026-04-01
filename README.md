# AI Resume & Cover Letter Generator

## Overview

This project is a simple web app that generates resumes and cover letters based on user input and a job description.

The idea is to reduce the time spent customizing applications by using AI to tailor content for specific roles.

---

## Features

* Generates a short professional summary
* Improves experience descriptions into bullet points
* Suggests relevant skills based on the job description
* Creates a complete cover letter

---

## Tech Stack

* Python
* Streamlit
* Google Gemini API
* Requests

---

## Running the app

Clone the repo:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

---

## How it works

The user fills in their details and past experience, along with a job description.

The app sends this data as prompts to the Gemini API, which returns structured content for different sections of a resume and a cover letter.

---

## Notes

This project is still in progress. Some outputs may need manual editing depending on the job role.

---

## Future improvements

* Add export to PDF
* Better formatting for resumes
* More control over generated content

