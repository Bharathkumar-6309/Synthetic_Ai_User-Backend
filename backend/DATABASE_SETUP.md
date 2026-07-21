# Database Setup Guide

## Overview
The Synthetic AI User Backend uses MySQL with pre-defined SQL scripts for table creation and initial data seeding.

## Prerequisites

1. **MySQL Server** - Install and start MySQL
   - Windows: Download from https://dev.mysql.com/downloads/mysql/
   - Mac: `brew install mysql`
   - Linux: `sudo apt-get install mysql-server`

2. **Python Dependencies** - Already in requirements.txt
   - `aiomysql==0.2.0` - Async MySQL driver
   - `PyMySQL==1.1.1` - MySQL connector for setup script

## Setup Instructions

### 1. Configure Environment Variables
Edit `.env` file with your MySQL credentials:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=synthetic_ai_user
DATABASE_URL=mysql+aiomysql://root:your_password@localhost:3306/synthetic_ai_user
```

### 2. Run Database Setup Script
```bash
cd backend
python scripts/setup_database.py
```

This will:
- Create the `synthetic_ai_user` database
- Create all required tables (users, experiments, personas, surveys, responses, interview_sessions, insights, reports)
- Insert sample data for testing (1 user, 1 experiment, 6 personas, 1 survey, 6 responses, 1 insight, 1 report)

### 3. Verify Setup
Connect to MySQL and verify:
```bash
mysql -u root -p
USE synthetic_ai_user;
SHOW TABLES;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM personas;
```

## SQL Scripts

### schema.sql
Located at `backend/sql/schema.sql`
- Creates database if not exists
- Defines all table schemas with proper indexes and foreign keys
- Uses InnoDB engine with UTF-8 support

### seed.sql
Located at `backend/sql/seed.sql`
- Inserts sample user for testing
- Creates sample experiment with 6 diverse personas
- Adds survey with responses from all personas
- Generates insight data from the responses
- Creates a sample report

## Manual SQL Execution

If you prefer to run SQL manually:

```bash
# Create database and schema
mysql -u root -p < sql/schema.sql

# Insert seed data
mysql -u root -p synthetic_ai_user < sql/seed.sql
```

## Reset Database

To reset the database (drop and recreate):
```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS synthetic_ai_user;"
python scripts/setup_database.py
```

## Table Structure

### users
- id, email, name, timestamps
- Used for authentication (future milestone)

### experiments
- id, owner_id, title, product_description, target_audience, research_objectives
- persona_count, status, timestamps
- Links to users, personas, surveys, interviews, insights, reports

### personas
- id, experiment_id, demographic profile (name, age, gender, occupation, location, income, education)
- behavioral profile (personality_traits, behavioral_patterns, tech_savviness, daily_habits)
- psychological profile (core_values, motivations, pain_points, risk_tolerance)
- display fields (bio, avatar_seed, quote)
- consistency fields (persona_hash, consistency_seed)
- generation_source, product_fit_score

### surveys
- id, experiment_id, question, status, timestamps
- Links to responses

### responses
- id, survey_id, persona_id, answer_text, sentiment, timestamps
- Links to surveys and personas

### interview_sessions
- id, experiment_id, persona_id, status, messages (JSON), summary, timestamps
- Stores conversation history

### insights
- id, experiment_id, would_use_pct, would_pay_pct
- themes, sentiment, key_quotes, suggestions (JSON)
- user_wants_summary, persona_scores, raw_data (JSON)

### reports
- id, experiment_id, title, summary
- persona_profiles, response_highlights, insight_summary, validation_scoring, recommendations (JSON)
- status, file_path, error_message, timestamps

## Sample Data

The seed data includes:
- **1 User**: demo@synthetic.ai
- **1 Experiment**: AI Productivity Assistant
- **6 Personas**: Diverse profiles (engineer, PM, team lead, UX designer, engineering manager, founder)
- **1 Survey**: Task management challenges
- **6 Responses**: One from each persona
- **1 Insight**: Analysis of the responses
- **1 Report**: Compiled research report

This sample data can be used for testing the application without creating new experiments.

## Troubleshooting

### Connection Issues
```bash
# Check MySQL is running
# Windows
net start MySQL

# Mac/Linux
sudo systemctl start mysql
# or
brew services start mysql
```

### Permission Issues
```bash
# Grant privileges
mysql -u root -p
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Script Errors
```bash
# Check Python dependencies
pip install PyMySQL python-dotenv

# Verify SQL files exist
ls sql/schema.sql sql/seed.sql
```

## Application Integration

The application no longer auto-creates tables on startup. Tables must be created via the SQL scripts before running the application.

To start the application after database setup:
```bash
cd backend
uvicorn app.main:app --reload
```

The application will connect to the existing database and use the pre-defined schema.
