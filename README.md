# Protex AI CV Engineering Take-Home

## Project Overview

This project implements a `computer vision rule simulation` for detecting when a Person and a Car are inside the same Region of Interest at the same time.

## Assignment
The assignment includes two main parts:

- Visualization of Regions of Interest and detected objects on a 1920x1080 black canvas.
- Event detection and Slack notification when the Person + Car rule is triggered.

## Project Structure
```bash
protex-cv-takehome/
├── data/
├── outputs/
├── src/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10+
- OpenCV
- Shapely
- python-dotenv
- requests

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Final Notes

The official `annotations.json` file is required to run the final assignment data. A small sample file will be added for local development while waiting for the official annotations file.

## Author

**Eng. Tyrone Eduardo Rodriguez Motato**  
Computer Vision & AI Engineer  
Dublin, Ireland  
Email: tyrerodr@hotmail.com