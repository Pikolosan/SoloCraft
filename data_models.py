"""
Data models for SoloCraft application.
Contains classes for Mission, Ticket System, and Insight Debt.
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from enum import Enum


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Mission:
    def __init__(self, title, description, difficulty, constraints, rewards, punishment=None, mission_id=None):
        self.id = mission_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.constraints = constraints
        self.rewards = rewards
        self.punishment = punishment
        self.created_at = datetime.now().isoformat()
        self.completed = False
        self.completed_at = None

    def complete_mission(self):
        self.completed = True
        self.completed_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'constraints': self.constraints,
            'rewards': self.rewards,
            'punishment': self.punishment,
            'created_at': self.created_at,
            'completed': self.completed,
            'completed_at': self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        mission = cls(
            title=data['title'],
            description=data['description'],
            difficulty=data['difficulty'],
            constraints=data['constraints'],
            rewards=data['rewards'],
            punishment=data.get('punishment'),
            mission_id=data['id']
        )
        mission.created_at = data['created_at']
        mission.completed = data['completed']
        mission.completed_at = data.get('completed_at')
        return mission


class InsightDebt:
    def __init__(self, ticket_type, used_for, debt_id=None):
        self.id = debt_id or str(uuid.uuid4())
        self.ticket_type = ticket_type  # 'Help' or 'Tutorial'
        self.used_for = used_for
        self.created_at = datetime.now().isoformat()
        self.cleared = False
        self.insight_entry = None
        self.cleared_at = None

    def clear_debt(self, insight_entry):
        self.cleared = True
        self.insight_entry = insight_entry
        self.cleared_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'ticket_type': self.ticket_type,
            'used_for': self.used_for,
            'created_at': self.created_at,
            'cleared': self.cleared,
            'insight_entry': self.insight_entry,
            'cleared_at': self.cleared_at
        }

    @classmethod
    def from_dict(cls, data):
        debt = cls(
            ticket_type=data['ticket_type'],
            used_for=data['used_for'],
            debt_id=data['id']
        )
        debt.created_at = data['created_at']
        debt.cleared = data['cleared']
        debt.insight_entry = data.get('insight_entry')
        debt.cleared_at = data.get('cleared_at')
        return debt


class UserProgress:
    def __init__(self):
        self.xp = 0
        self.help_tickets = 3
        self.tutorial_tickets = 2
        self.last_ticket_reset = datetime.now().isoformat()
        self.level = 1
        self.badges = []

    def add_xp(self, amount):
        self.xp += amount
        new_level = (self.xp // 100) + 1
        if new_level > self.level:
            self.level = new_level
            return True  # Level up occurred
        return False

    def use_help_ticket(self):
        if self.help_tickets > 0:
            self.help_tickets -= 1
            return True
        return False

    def use_tutorial_ticket(self):
        if self.tutorial_tickets > 0:
            self.tutorial_tickets -= 1
            return True
        return False

    def should_reset_tickets(self):
        last_reset = datetime.fromisoformat(self.last_ticket_reset)
        return datetime.now() - last_reset >= timedelta(days=7)

    def reset_tickets(self):
        self.help_tickets = 3
        self.tutorial_tickets = 2
        self.last_ticket_reset = datetime.now().isoformat()

    def to_dict(self):
        return {
            'xp': self.xp,
            'help_tickets': self.help_tickets,
            'tutorial_tickets': self.tutorial_tickets,
            'last_ticket_reset': self.last_ticket_reset,
            'level': self.level,
            'badges': self.badges
        }

    @classmethod
    def from_dict(cls, data):
        progress = cls()
        progress.xp = data.get('xp', 0)
        progress.help_tickets = data.get('help_tickets', 3)
        progress.tutorial_tickets = data.get('tutorial_tickets', 2)
        progress.last_ticket_reset = data.get('last_ticket_reset', datetime.now().isoformat())
        progress.level = data.get('level', 1)
        progress.badges = data.get('badges', [])
        return progress