# Elyx Healthcare Dashboard

A Flask-based healthcare conversation generator and dashboard system for the Elyx Healthcare hackathon. This application generates realistic healthcare conversations using Ollama AI and provides a comprehensive dashboard to visualize member journeys, health metrics, and team interactions.

## Features

- 🤖 **AI-Powered Conversation Generation**: Uses Ollama to generate realistic healthcare conversations
- 📊 **Interactive Dashboard**: Comprehensive overview of member health journey
- 📈 **Health Metrics Visualization**: Charts showing HRV, recovery scores, and heart rate trends
- 📅 **Timeline View**: Visual timeline of member's healthcare journey
- 💬 **Conversation Management**: Browse and search through all generated conversations
- 🎯 **Decision Tracking**: Track evidence-based healthcare decisions
- 🏥 **Team Metrics**: Monitor healthcare team consultation hours

## Technology Stack

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: Vanilla JavaScript, Chart.js, Custom CSS
- **AI**: Ollama (Local LLM)
- **Database**: SQLite (easily replaceable with PostgreSQL/MySQL)

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running locally
   - Install from: https://ollama.ai
   - Required model: `llama3.1:8b`

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository (or download the files)
cd elyx_healthcare_dashboard

# Or manually setup:
python3 -m venv elyx_venv
source elyx_venv/bin/activate  # On Windows: elyx_venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Ollama

```bash
# Start Ollama server
ollama serve

# In another terminal, pull the required model
ollama pull llama3.1:8b
```

### 3. Run the Application

```bash
# Activate virtual environment (if not already activated)
source elyx_venv/bin/activate  # On Windows: elyx_venv\Scripts\activate

# Start the Flask application
python app.py
```

### 4. Access the Dashboard

Open your browser and navigate to: http://localhost:5000

## Usage

### Initial Setup
- The application automatically initializes the database with sample data
- Sample member profile (Rohan Patel) is created with basic health information

### Generating Conversations
1. Go to the main dashboard
2. Scroll down to the "Conversation Generator" section
3. Click "Generate Conversations" button
4. Wait for Ollama to generate conversations (this may take a few minutes)
5. Refresh the page to see new conversations in the dashboard

### Exploring the Dashboard

#### Overview Tab
- Member profile information
- Journey statistics (days in program, events, breakthroughs)
- Health metrics charts
- Recent timeline events

#### Timeline Tab
- Complete 8-month journey visualization
- Filter events by category
- Click events for detailed information

#### Conversations Tab
- Browse all generated conversations
- Search through conversations
- WhatsApp-style message interface

#### Decisions Tab
- Track evidence-based healthcare decisions
- See reasoning and outcomes for each decision

## API Endpoints

The application provides REST API endpoints:

- `GET /api/member/<id>` - Get member information
- `GET /api/conversations` - Get all conversations
- `GET /api/timeline` - Get timeline events
- `GET /api/health-metrics` - Get health metrics data
- `GET /api/decisions` - Get decisions data
- `GET /api/team-metrics` - Get team consultation metrics
- `POST /api/generate-conversations` - Generate new conversations
- `GET /api/search-conversations?q=<query>` - Search conversations

## Project Structure

```
elyx_healthcare_dashboard/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── routes.py             # API routes and views
├── conversation_generator.py  # Ollama conversation generator
├── database.py           # Database initialization
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── conversations.html
│   ├── timeline.html
│   └── decisions.html
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Dashboard styling
│   └── js/
│       └── dashboard.js  # Frontend JavaScript
├── setup.bat             # Setup script
└── README.md            # This file
```

## Configuration

Environment variables can be set in `.env` file:

```
SECRET_KEY=elyx-healthcare-secret-key-2025
DATABASE_URL=sqlite:///elyx_healthcare.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## Database Schema

The application uses SQLAlchemy with the following models:

- **Member**: Patient information and health goals
- **TeamMember**: Healthcare team member details
- **Conversation**: Generated WhatsApp-style conversations
- **TimelineEvent**: Major events in member's journey
- **HealthMetric**: HRV, recovery scores, heart rate data
- **Decision**: Evidence-based healthcare decisions
- **TeamMetric**: Team consultation hours and metrics

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Make sure Ollama is running: `ollama serve`
   - Check if the model is available: `ollama list`
   - Verify the URL in config: `http://localhost:11434`

2. **Database Errors**
   - Delete the database file and restart: `rm elyx_healthcare.db`
   - The app will recreate the database automatically

3. **Port Already in Use**
   - Change the port in `app.py`: `app.run(port=5001)`

4. **CSS/JS Not Loading**
   - Make sure files are in the correct directories:
     - `static/css/style.css`
     - `static/js/dashboard.js`

### Performance Notes

- Conversation generation can take 5-30 minutes depending on your system
- First-time model loading in Ollama may take additional time
- For production use, consider using a more powerful database like PostgreSQL

## Contributing

This project was created for the Elyx Healthcare hackathon. Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is created for educational and hackathon purposes.

## Contact

For questions about this implementation, please refer to the hackathon documentation or create an issue in the repository.
