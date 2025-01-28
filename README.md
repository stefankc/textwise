# Textwise

Textwise is an application designed to help users summarize reading material to enhance comprehension and information retention. It is particularly beneficial for students, researchers, and professionals who regularly engage with dense or technical content.

## Features
- **Structured Summarization**: Guides users through step-by-step summarization of texts.
- **AI-Based Feedback**: Provides immediate feedback powered by AI (using OpenAI's GPT-4 and LLamaParse) to improve summary quality.
- **User-Friendly Interface**: Simple navigation with integrated settings for API key management.

## Installation

### Prerequisites
- Administrative privileges  
- Docker installed ([Download Docker](https://www.docker.com))

### Setup Steps

1. **Download Application Files**  
   - Clone or download the ZIP file from the GitHub repository.  
   - Extract the contents to a folder on your system.

2. **Launch the Application**  
   - **Windows:** Right-click on `start-windows.bat` → "Run as Administrator" or run it in the terminal.  
   - **Mac:** Double-click `start-mac.command` or run it in the terminal.  

   This process will initialize the Docker environment and start the necessary containers.

3. **Access the Application**  
   - Open your browser and navigate to [http://localhost:3000/](http://localhost:3000/).  
   - Go to the **Settings** page.

4. **Configure API Keys**  
   - Add your OpenAI API key ([Get Key](https://platform.openai.com/api-keys))  
   - Add your LLamaParse API key ([Get Key](https://cloud.llamaindex.ai/api-key))

5. **Start Using Textwise**  
   - Explore the application and start summarizing your reading material.

## Troubleshooting

- **Docker Issues:**  
  - Ensure Docker is running.  
  - Restart your system after installing Docker.  
  - Verify that three containers (`backend-1`, `database-1`, `pgadmin-1`) are running in Docker.

- **Reinstallation:**  
  If issues persist, run the following commands in the `text-reader-app` directory:
  ```bash
  docker compose down --volumes
  docker compose build --no-cache
  docker compose up -d
  ```

# Research Context

Textwise was developed to explore how AI-assisted summarization impacts users’ comprehension and retention. An empirical study was conducted where participants were divided into two groups:
	•	Test Group: Used Textwise with interactive feedback.
	•	Control Group: Read the same material without feedback.
The goal was to assess how structured summarization and feedback improve learning outcomes.