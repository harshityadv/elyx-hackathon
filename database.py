from models import db, Member, TeamMember, TimelineEvent, HealthMetric, Decision, TeamMetric
from datetime import datetime, date
import json

def init_database():
    """Initialize database with sample data"""
    db.create_all()

    # Create sample member
    member = Member.query.first()
    if not member:
        member = Member(
            name="Rohan Patel",
            preferred_name="Rohan Patel",
            age=46,
            gender="Male",
            location="Singapore",
            occupation="Regional Head of Sales - FinTech",
            health_goals=json.dumps([
                "Reduce heart disease risk by Dec 2026",
                "Enhance cognitive function by June 2026",
                "Annual health screenings starting Nov 2025"
            ]),
            chronic_conditions=json.dumps(["POTS/Long COVID"]),
            wearables=json.dumps(["Garmin watch", "Whoop strap"])
        )
        db.session.add(member)
        db.session.flush()

    # Create team members
    team_members_data = [
        {
            "name": "Ruby",
            "role": "Concierge",
            "specialty": "Concierge",
            "communication_style": "Empathetic, organized, proactive"
        },
        {
            "name": "Dr. Warren",
            "role": "Medical Strategist",
            "specialty": "Medical Strategy",
            "communication_style": "Authoritative, precise, scientific"
        },
        {
            "name": "Advik",
            "role": "Performance Scientist",
            "specialty": "Performance Science",
            "communication_style": "Analytical, data-driven, pattern-oriented"
        },
        {
            "name": "Carla",
            "role": "Nutritionist",
            "specialty": "Nutrition",
            "communication_style": "Practical, educational, behavioral change focused"
        },
        {
            "name": "Rachel",
            "role": "PT/Physiotherapist",
            "specialty": "Physical Therapy",
            "communication_style": "Direct, encouraging, form-focused"
        },
        {
            "name": "Neel",
            "role": "Concierge Lead",
            "specialty": "Leadership",
            "communication_style": "Strategic, reassuring, big-picture"
        },
        {
            "name": "Dr. Evans",
            "role": "Stress Management",
            "specialty": "Stress Management",
            "communication_style": "Calming, methodical, mindfulness-focused"
        }
    ]

    for tm_data in team_members_data:
        existing = TeamMember.query.filter_by(name=tm_data["name"]).first()
        if not existing:
            team_member = TeamMember(**tm_data)
            db.session.add(team_member)

    # Create sample timeline events
    timeline_events_data = [
        {
            "member_id": member.id,
            "date": date(2025, 1, 15),
            "title": "Initial Health Inquiry & Onboarding",
            "category": "onboarding",
            "status": "completed",
            "description": "Member expresses concern about high intensity minutes on Garmin",
            "outcome": "Information provided & plan proposed",
            "team_members": json.dumps(["Ruby", "Dr. Warren"]),
            "response_time": "25 minutes",
            "time_to_resolution": "3 days",
            "friction_points": "None"
        },
        {
            "member_id": member.id,
            "date": date(2025, 2, 3),
            "title": "Critical Board Presentation Preparation",
            "category": "lifestyle",
            "status": "completed",
            "description": "Member needs to be sharp for board meeting, concerned about dizziness",
            "outcome": "Travel protocol and jet lag mitigation implemented",
            "team_members": json.dumps(["Advik", "Ruby"]),
            "response_time": "10 minutes",
            "time_to_resolution": "ongoing"
        },
        {
            "member_id": member.id,
            "date": date(2025, 3, 1),
            "title": "Member Dissatisfaction & Service Feedback",
            "category": "feedback",
            "status": "resolved",
            "description": "Member frustrated with perceived lack of progress and proactivity",
            "outcome": "Service improvements and better communication protocols",
            "team_members": json.dumps(["Neel", "Ruby"]),
            "response_time": "1 day 13 hours",
            "time_to_resolution": "1 day 1 hour",
            "friction_points": "Perceived inaction, lack of proactivity, communication confusion"
        },
        {
            "member_id": member.id,
            "date": date(2025, 4, 12),
            "title": "First Successful Zone 2 Protocol",
            "category": "exercise",
            "status": "breakthrough",
            "description": "Successfully completed 25-minute cardio with stable HRV using hydration protocol",
            "outcome": "Found controllable variable for autonomic health",
            "team_members": json.dumps(["Advik"]),
            "response_time": "immediate",
            "time_to_resolution": "same day"
        },
        {
            "member_id": member.id,
            "date": date(2025, 5, 2),
            "title": "Major Illness Setback",
            "category": "medical",
            "status": "resolved",
            "description": "Viral infection requiring comprehensive sick day protocol",
            "outcome": "Successful recovery with board meeting rescheduled",
            "team_members": json.dumps(["Dr. Warren", "Advik", "Ruby", "Neel"]),
            "response_time": "5 minutes",
            "time_to_resolution": "3 weeks",
            "friction_points": "Board meeting timing conflict"
        },
        {
            "member_id": member.id,
            "date": date(2025, 6, 22),
            "title": "Multi-Pillar Sleep Success",
            "category": "breakthrough",
            "status": "completed",
            "description": "Record deep sleep using blue-light glasses and shutdown ritual",
            "outcome": "1h 30m deep sleep - personal record",
            "team_members": json.dumps(["Advik", "Dr. Evans"]),
            "response_time": "proactive",
            "time_to_resolution": "immediate"
        },
        {
            "member_id": member.id,
            "date": date(2025, 7, 16),
            "title": "Personalized Nutrition Discovery",
            "category": "nutrition",
            "status": "breakthrough",
            "description": "CGM data reveals optimal sushi consumption strategy",
            "outcome": "Glucose spike reduced from 180 to 140 with protocol",
            "team_members": json.dumps(["Carla"]),
            "response_time": "20 minutes",
            "time_to_resolution": "1 day"
        },
        {
            "member_id": member.id,
            "date": date(2025, 8, 12),
            "title": "Long-term Goals Definition",
            "category": "planning",
            "status": "active",
            "description": "Centenarian Decathlon goals set with measurable targets",
            "outcome": "Clear 12-24 month targets established",
            "team_members": json.dumps(["Rachel", "Ruby"]),
            "response_time": "immediate",
            "time_to_resolution": "same day"
        }
    ]

    for event_data in timeline_events_data:
        existing = TimelineEvent.query.filter_by(
            member_id=event_data["member_id"],
            date=event_data["date"],
            title=event_data["title"]
        ).first()
        if not existing:
            event = TimelineEvent(**event_data)
            db.session.add(event)

    # Create sample health metrics
    health_metrics_data = [
        # HRV data
        {"member_id": member.id, "metric_type": "hrv", "value": 35, "date": date(2025, 1, 1)},
        {"member_id": member.id, "metric_type": "hrv", "value": 38, "date": date(2025, 2, 1)},
        {"member_id": member.id, "metric_type": "hrv", "value": 42, "date": date(2025, 3, 1)},
        {"member_id": member.id, "metric_type": "hrv", "value": 39, "date": date(2025, 4, 1)},
        {"member_id": member.id, "metric_type": "hrv", "value": 25, "date": date(2025, 5, 1)},
        {"member_id": member.id, "metric_type": "hrv", "value": 44, "date": date(2025, 6, 1)},
        {"member_id": member.id, "metric_type": "hrv", "value": 47, "date": date(2025, 7, 1)},
        {"member_id": member.id, "metric_type": "hrv", "value": 48, "date": date(2025, 8, 1)},

        # Recovery Score data
        {"member_id": member.id, "metric_type": "recovery_score", "value": 45, "date": date(2025, 1, 1)},
        {"member_id": member.id, "metric_type": "recovery_score", "value": 52, "date": date(2025, 2, 1)},
        {"member_id": member.id, "metric_type": "recovery_score", "value": 33, "date": date(2025, 3, 1)},
        {"member_id": member.id, "metric_type": "recovery_score", "value": 58, "date": date(2025, 4, 1)},
        {"member_id": member.id, "metric_type": "recovery_score", "value": 1, "date": date(2025, 5, 1)},
        {"member_id": member.id, "metric_type": "recovery_score", "value": 72, "date": date(2025, 6, 1)},
        {"member_id": member.id, "metric_type": "recovery_score", "value": 78, "date": date(2025, 7, 1)},
        {"member_id": member.id, "metric_type": "recovery_score", "value": 82, "date": date(2025, 8, 1)},

        # Resting Heart Rate data
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 68, "date": date(2025, 1, 1)},
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 66, "date": date(2025, 2, 1)},
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 64, "date": date(2025, 3, 1)},
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 63, "date": date(2025, 4, 1)},
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 72, "date": date(2025, 5, 1)},
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 62, "date": date(2025, 6, 1)},
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 61, "date": date(2025, 7, 1)},
        {"member_id": member.id, "metric_type": "resting_heart_rate", "value": 60, "date": date(2025, 8, 1)}
    ]

    for metric_data in health_metrics_data:
        existing = HealthMetric.query.filter_by(
            member_id=metric_data["member_id"],
            metric_type=metric_data["metric_type"],
            date=metric_data["date"]
        ).first()
        if not existing:
            metric = HealthMetric(**metric_data)
            db.session.add(metric)

    # Create sample decisions
    decisions_data = [
        {
            "member_id": member.id,
            "date": date(2025, 2, 28),
            "decision_type": "device",
            "decision": "Upgrade to Whoop 4.0 strap",
            "reason": "Need high-fidelity autonomic data for POTS management",
            "triggered_by": "Dr. Warren analysis of medical records",
            "outcome": "Successful data collection enabling Zone 2 protocol optimization",
            "evidence": "Garmin provides blurry photo, need HD video of autonomic function"
        },
        {
            "member_id": member.id,
            "date": date(2025, 3, 4),
            "decision_type": "supplement",
            "decision": "Switch to Magnesium Threonate",
            "reason": "Improve sleep quality and cognitive performance",
            "triggered_by": "Carla's analysis of energy patterns and Grok supplement review",
            "outcome": "First full night sleep in months, sleep latency improved from 25 to 8 minutes",
            "evidence": "Crosses blood-brain barrier more effectively than other forms"
        },
        {
            "member_id": member.id,
            "date": date(2025, 5, 2),
            "decision_type": "protocol",
            "decision": "Implement Sick Day Protocol",
            "reason": "Whoop data showed viral infection, prevent cognitive impairment",
            "triggered_by": "12bpm RHR increase, 45% HRV decrease, elevated respiratory rate",
            "outcome": "Successful recovery, board meeting rescheduled appropriately",
            "evidence": "Biotelemetry data confirmed significant immune response"
        },
        {
            "member_id": member.id,
            "date": date(2025, 6, 20),
            "decision_type": "diagnostic",
            "decision": "Implement Continuous Glucose Monitor",
            "reason": "Real-time glucose data for personalized nutrition optimization",
            "triggered_by": "Dr. Warren recommendation for metabolic health investigation",
            "outcome": "Discovered oatmeal causes 160 spike, personalized breakfast strategy",
            "evidence": "Need data on how body responds to specific foods"
        }
    ]

    for decision_data in decisions_data:
        existing = Decision.query.filter_by(
            member_id=decision_data["member_id"],
            date=decision_data["date"],
            decision=decision_data["decision"]
        ).first()
        if not existing:
            decision = Decision(**decision_data)
            db.session.add(decision)

    # Create team metrics
    team_metrics_data = [
        {"team_member_id": 1, "hours": 25},  # Ruby
        {"team_member_id": 2, "hours": 12},  # Dr. Warren
        {"team_member_id": 3, "hours": 18},  # Advik
        {"team_member_id": 4, "hours": 8},   # Carla
        {"team_member_id": 5, "hours": 10},  # Rachel
        {"team_member_id": 6, "hours": 6},   # Neel
        {"team_member_id": 7, "hours": 4}    # Dr. Evans
    ]

    for metric_data in team_metrics_data:
        existing = TeamMetric.query.filter_by(
            team_member_id=metric_data["team_member_id"]
        ).first()
        if not existing:
            metric = TeamMetric(**metric_data)
            db.session.add(metric)

    db.session.commit()
    print("✅ Database initialized with sample data")
    return member.id
