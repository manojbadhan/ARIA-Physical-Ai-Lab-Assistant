# Software Requirements Specification: ARIA

**Purpose.** A voice and vision assistant for a robotics lab. It answers tech questions and tells students where lab tools were last placed.

## Users
- **Student:** asks questions by voice or text, identifies tools with the camera, checks inventory.
- **Faculty:** registers tools by photo and location, reviews photos of students using tools.

## Functional requirements
1. Wake-word voice interaction (wake word "ARIA", 20 s follow-up window).
2. Answer only tech and lab questions; otherwise ask "did you mean X?" or decline.
3. "Where is X" answered with rack/box and a photo.
4. Identify objects from the camera (YOLO first, Gemini fallback).
5. Faculty upload tool photos with almirah/rack/box; the location is stored.
6. Robot uploads photos of students using tools; faculty can view them.
7. Account signup/login with student and faculty roles.

## Non-functional
- Spoken reply under 5 s on Raspberry Pi 5 for general questions.
- Website works on phone and desktop, light and dark themes.
- Optional AI libraries must not stop the website from starting.
