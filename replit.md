# SoloCraft - Independent Project Builder

## Overview

SoloCraft is a desktop gamification application built with Python and Tkinter designed to help users build projects independently with minimal external assistance. The app implements a mission-based system where users create project tasks, manage limited help resources through a ticket system, and track their learning through insight debt management. The application encourages self-reliance while providing structured support through gamification mechanics including XP, levels, and achievement tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **UI Framework**: Tkinter-based desktop application with a main window containing multiple panels
- **Layout Structure**: Grid-based layout with header stats, left mission panel, and right insight debt panel
- **Component Organization**: Modular UI setup with separate methods for different interface sections
- **User Interaction**: Form-based input for mission creation, popup dialogs for ticket usage and insight entry

### Backend Architecture
- **Data Models**: Object-oriented design with separate classes for Mission, InsightDebt, and UserProgress
- **Business Logic**: Enum-based difficulty system, UUID-based entity identification, and datetime tracking for all operations
- **State Management**: Centralized storage manager handling all data persistence operations
- **Gamification Engine**: XP/level system with weekly ticket reset mechanism and badge achievement tracking

### Data Storage Solutions
- **Storage Type**: Local JSON file-based persistence without external database dependencies
- **File Structure**: Separate JSON files for missions, insight debts, and user progress stored in dedicated data directory
- **Data Models**: Dictionary serialization/deserialization for all entities with timestamp tracking
- **Backup Strategy**: Automatic file initialization and directory creation on first run

### Core Game Mechanics
- **Mission System**: User-created project tasks with difficulty levels, constraints, rewards, and optional punishments
- **Ticket System**: Limited help and tutorial tickets that reset weekly, consumed when accessing assistance
- **Insight Debt**: Mandatory learning documentation required after using tickets to encourage knowledge retention
- **Progress Tracking**: XP accumulation, level progression, and badge collection for long-term engagement

## External Dependencies

### Python Standard Library
- **tkinter**: Main GUI framework and all UI components including ttk widgets and dialog boxes
- **json**: Data serialization and file-based persistence operations
- **os**: File system operations and directory management
- **uuid**: Unique identifier generation for missions and other entities
- **datetime**: Timestamp tracking and weekly reset calculations
- **enum**: Type-safe difficulty level definitions

### File System Dependencies
- **Local Data Directory**: `solocraft_data/` folder for storing all application data
- **JSON Files**: missions.json, insight_debts.json, and user_progress.json for persistent storage
- **No External APIs**: Completely offline application with no network dependencies or third-party service integrations