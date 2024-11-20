# Vimeo Videos Metadata Extraction

This project uses the Vimeo API to fetch metadata about videos from a user's Vimeo account and save it in a CSV format.
The extracted metadata is saved in a structured format for further use, making it suitable for workflows involving video-based experiments.

### Background
This project was developed as part of my research, where I have conducted an experiment conducted using Qualtrics. 168 videos hosted on Vimeo were embedded in the survey as experimental manipulations. The script automates the process of retrieving metadata (e.g., video names, URIs, and embed codes) for integration into the experimental pipeline (survey creation, data analysis).

### How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/LuisaCarrer/Vimeo-metadata.git
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Set up your `.env` file with your Vimeo API token:
   ```bash
   VIMEO_TOKEN=your_vimeo_api_token_here
   ```
2. Run the Python script:
   ```bash
   python VimeoMetadata.py
   ```