# Safety Event Detection

## Project Overview

This project implements a `computer vision rule simulation` for detecting when a Person and a Car are inside the same Region of Interest at the same time.

## Assignment
The assignment includes two main parts:

- Visualization of Regions of Interest and detected objects on a 1920x1080 black canvas.
- Event detection and Slack notification when the Person + Car rule is triggered.

## Project Structure
```bash
cv-safety-event-detection/
│
├── data/
│   └── annotations.json
├── outputs/
│   └── output.mp4
├── src/
│   ├── config.py
│   ├── event_detector.py
│   ├── geometry.py
│   ├── main.py
│   ├── slack_notifier.py
│   ├── slack_formatter.py
│   ├── video_generator.py
│   └── visualizer.py
├── tests/
│   ├── test_event_detector.py
│   ├── test_geometry.py
│   └── test_slack_formatter.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
```bash
git clone https://github.com/tyrerodr/cv-safety-event-detection.git
cd cv-safety-event-detection
```

2. Install dependencies
```bash
python -m venv .venv

source .venv/bin/activate or source .venv/Scripts/activate

pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add:
```bash
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=your-slack-channel-id
```
> Note: The Slack bot must have the chat:write permission and must be invited to the target Slack channel.
If Slack is not configured, the project prints the formatted Slack messages locally instead of failing.
>

## Running the Project
From the project root, run:
```bash
python src/main.py
```

The output video will be saved to:
```bash
outputs/output.mp4
```
> Note: Detected events will also be sent to Slack if Slack is configured.
>

## Output
The generated video shows:
- Two predefined ROIs
- Person, Car, and Truck detections as colored points
- Frame number and timestamp
- Highlighted ROI when an event is triggered
- Event banner when Person + Car are inside the same ROI

# Test 
Run tests with:
```bash
pytest
```

## Final Notes
### Point-based ROI membership
The assignment visualization represents objects as points, so this implementation uses the bottom-center point of each bounding box to determine whether an object is inside an ROI.

This approach is simple, consistent with the visual output, and commonly useful when approximating an object's contact point with the ground plane.

*A possible future improvement would be to use bounding box overlap with the ROI instead of a single point.*

### Slack credentials
Slack credentials are not hardcoded. The project uses environment variables and includes only a .env.example file so reviewers can configure their own Slack workspace safely.

### Modular design
The project is separated into focused modules:

- Geometry calculations
- Event detection
- Frame visualization
- Video generation
- Slack formatting
- Slack notification

## Author

**Eng. Tyrone Eduardo Rodriguez Motato**  
Computer Vision & AI Engineer  
Dublin, Ireland  
Email: tyrerodr@hotmail.com
