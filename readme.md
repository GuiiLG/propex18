# AI Construction Schedule Generator

This project is an **automation system** for creating construction schedules using **AI**.  
It integrates various tools and services to generate detailed project timelines automatically through **OpenAI’s ChatGPT API**.

## Overview

The goal of this project is to simplify the process of building and managing construction schedules by combining **automation workflows** and **AI text generation**.  
The system uses **PipeDream** as a middleware platform to handle backend logic and API communication.

## Architecture

The project follows a **frontend-backend separated architecture**:

- **Frontend**:  
  - Built with **HTML**, **CSS**, and **JavaScript**.  [View index.html](./index.html)
  - Hosted on **GitHub Pages** for simplicity and free deployment. [GitHub Pages](https://GuiiLG.github.io/propex18/)
  - Sends requests directly to the backend endpoint on PipeDream.

- **Backend (Middleware)**:  
  - Implemented using **PipeDream**.  [View index.html](./automation.py)
  - Handles API calls and routes requests between the frontend and OpenAI’s API.  
  - Contains logic for processing and structuring the AI-generated schedule data.

- **AI Engine**:  
  - **OpenAI’s ChatGPT API**.  
  - Uses both the **GPT-4o** and **GPT-3.5-turbo** models to generate construction schedules and task breakdowns based on user input.

## Data Processing (ETL)

This project includes a data extraction and transformation pipeline for **ORSE**, the system used to obtain construction service data.  
ORSE provided many service documents in **PDF format**, so an **ETL (Extract, Transform, Load)** process was implemented to make that information usable by the AI. The pipeline performs the following steps:

1. **Extract** — Parse text and tables from the original PDF documents exported from ORSE.  
2. **Transform** — Clean and normalize the extracted content (remove noise, unify units and naming, and map fields to a consistent schema).  
3. **Load** — Store the transformed data as structured **JSON** files that the AI can easily consume when generating schedules.

Here's the manipulated data: [View final.json](./final.json)


## Technologies Used

| Category | Technology |
|-----------|-------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | PipeDream(Python) |
| AI | OpenAI API (GPT-4o, GPT-3.5-turbo) |
| Hosting | GitHub Pages |

## How It Works

1. The user interacts with the frontend interface.  
2. The frontend sends a request to the **PipeDream endpoint**.  
3. PipeDream processes the input and communicates with the **ChatGPT API**.  
4. ChatGPT generates a construction schedule based on the input parameters.  
5. The schedule is sent back to the frontend and displayed to the user.

## Future Improvements

- Add authentication and user management.  
- Enable saving and exporting generated schedules.  
- Introduce project templates for different types of construction workflows.  
- Improve UI/UX for better interaction and visualization.


