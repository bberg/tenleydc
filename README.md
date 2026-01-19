# Upper Northwest DC History Website

A comprehensive Flask-based website documenting the history of Tenleytown, American University Park, and surrounding neighborhoods in Northwest Washington, D.C.

## Features

- **14 Comprehensive Historical Topics**
  - Native American prehistory (Nacotchtank people)
  - Tenleytown founding and development
  - American University Park neighborhood history
  - Fort Reno and Civil War history
  - American University and WWI chemical weapons
  - Transportation history (roads, streetcars, Metro)
  - Schools (Janney, Deal, Jackson-Reed)
  - Broadcasting history (WRC-TV, Muppets origin)
  - Historic landmarks
  - Neighborhood profiles
  - Demographics and community evolution
  - Resources and archives

- **Interactive Features**
  - Responsive sidebar navigation
  - Search functionality
  - Dark/light theme toggle
  - Table of contents for long articles
  - Reading progress indicator
  - Back to top button
  - Interactive map page

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/bb/www/au-park-history
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Website

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Open your browser to:**
   ```
   http://localhost:5000
   ```

## Project Structure

```
au-park-history/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── content/              # Markdown content files
│   ├── overview.md
│   ├── prehistory.md
│   ├── tenleytown.md
│   ├── au_park.md
│   ├── fort_reno.md
│   ├── american_university.md
│   ├── transportation.md
│   ├── schools.md
│   ├── broadcasting.md
│   ├── landmarks.md
│   ├── neighborhoods.md
│   ├── demographics.md
│   ├── timeline.md
│   └── resources.md
├── templates/            # Jinja2 HTML templates
│   ├── base.html
│   ├── home.html
│   ├── page.html
│   ├── search.html
│   ├── map.html
│   └── 404.html
└── static/               # Static assets
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/           # (Add historical images here)
```

## Content Topics

| Topic | Description |
|-------|-------------|
| Overview | Introduction to Upper Northwest DC |
| Timeline | Chronological history from prehistory to present |
| Native American History | Nacotchtank people and prehistoric settlement |
| Tenleytown | Founding, John Tennally's tavern, development |
| AU Park | American University Park neighborhood history |
| Fort Reno | Civil War fortification and Reno City |
| American University | University history and WWI chemical weapons |
| Transportation | Roads, streetcars, automobiles, Metro |
| Schools | Janney, Deal, Jackson-Reed schools |
| Broadcasting | WRC-TV, Nixon-Kennedy debate, Muppets |
| Landmarks | Historic sites and buildings |
| Neighborhoods | Wesley Heights, Spring Valley, Friendship Heights |
| Demographics | Population and community changes |
| Resources | Archives, organizations, further reading |

## Key Historical Facts

- **Tenleytown** is one of the oldest communities in DC, second only to Georgetown
- **Fort Reno** at 409 feet is the highest natural point in Washington, DC
- **American University** was a WWI chemical weapons research site; cleanup continues
- **Kermit the Frog** was created at WRC-TV studios in Tenleytown
- **Reno City**, a thriving African American community, was destroyed in the 1920s

## Sources

Content is sourced from:
- Tenleytown Historical Society
- DC Public Library archives
- Library of Congress
- National Park Service
- Wikipedia and other public sources

## License

This project is for educational purposes. Historical content is compiled from public sources.

## Contributing

To add or update content:
1. Edit the relevant `.md` file in the `content/` directory
2. Follow the existing markdown formatting conventions
3. Restart the Flask server to see changes

## Keyboard Shortcuts

- `/` - Focus search input
- `h` - Go to home page
- `Esc` - Close mobile sidebar
