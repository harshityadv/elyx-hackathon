import requests
import json
import subprocess
import datetime
import random
from typing import List, Dict
from models import db, Member, TeamMember, Conversation, TimelineEvent, HealthMetric, Decision, TeamMetric
from config import Config
from dateutil.parser import parse

class ElyxConversationGenerator:
    def __init__(self, model="llama3.1:8b"):
        self.model = model
        self.base_url = Config.OLLAMA_BASE_URL
        self.member_name = "Rohan Patel"

        # ✅ FIXED: Don't convert member name to database format for display
        self.sender_mapping = {
            'Rohan Patel': 'Rohan Patel',  # Keep actual name
            'Rohan': 'Rohan Patel',
            'member': 'Rohan Patel',  # Convert generic to actual
            'Ruby (Concierge)': 'Ruby',
            'Ruby': 'Ruby', 
            'Dr. Warren (Medical)': 'Dr. Warren',
            'Dr. Warren': 'Dr. Warren',
            'Advik (Performance)': 'Advik',
            'Advik': 'Advik',
            'Carla (Nutrition)': 'Carla',
            'Carla': 'Carla',
            'Rachel (PT)': 'Rachel', 
            'Rachel': 'Rachel',
            'Neel (Lead)': 'Neel',
            'Neel': 'Neel',
            'Dr. Evans': 'Dr. Evans'
        }

    def call_ollama(self, prompt: str) -> str:
        """Call Ollama API via HTTP request"""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(url, json=payload, timeout=600)
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                print(f"Ollama API error: {response.status_code}")
                return ""
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return ""

    def get_system_prompt(self) -> str:
        return """You are an expert healthcare conversation generator for Elyx Healthcare.

Generate realistic WhatsApp-style conversations between Rohan Patel (46-year-old FinTech executive based in Singapore) and healthcare team members.

CRITICAL FORMATTING - Use EXACT format:
[DD/MM/YY, HH:MM AM/PM] Sender: Message text here
[15/01/25, 2:15 PM] Rohan Patel: My Garmin is logging consistently high intensity minutes...
[15/01/25, 2:38 PM] Ruby: Hi Rohan, thank you for sharing this...

MEMBER PROFILE:
- Rohan Patel: 46-year-old Regional Head of Sales for FinTech
- Location: Singapore, travels frequently (UK, US, South Korea, Jakarta)  
- Health Issues: POTS/long COVID, family history of heart disease
- Goals: Reduce heart disease risk, enhance cognitive function, annual health screenings
- Analytical, driven, time-constrained, values data-driven approaches
- Uses Garmin watch, Whoop strap, PA named Sarah Tan
- Home cook named Javier, supportive wife, 2 young children

TEAM COMMUNICATION STYLES:
- Ruby (Concierge): Warm, organized, proactive coordination
- Dr. Warren (Medical): Authoritative, precise medical analysis  
- Advik (Performance): Data-focused, analytical, wearable insights
- Carla (Nutrition): Practical, educational, behavior-focused
- Rachel (PT): Direct, encouraging, movement expertise
- Neel (Lead): Strategic, big-picture leadership
- Dr. Evans (Stress): Calming, methodical, mindfulness-focused

Generate authentic healthcare conversations with specific data, medical reasoning, and realistic member interactions."""
    
    def generate_onboarding_conversations(self) -> str:
        prompt = self.get_system_prompt() + """

Generate 15-20 realistic conversation messages for Rohan's FIRST WEEK onboarding (January 15-22, 2025).

SCENARIO: Initial health inquiry and team introduction
- Rohan reports Garmin showing high intensity minutes despite POTS diagnosis
- Shares supplement list, discusses family history of heart disease  
- Team introduces themselves and explains their roles
- Discusses collecting medical records from Singapore and NY cardiologists
- Coordination with PA Sarah Tan for scheduling
- Ruby handles logistics, Dr. Warren provides medical oversight

FORMAT EACH MESSAGE EXACTLY AS:
[15/01/25, 2:15 PM] Rohan Patel: Ruby, my Garmin is logging consistently high intensity minutes, even on rest days. I suspect it's my POTS/long COVID. My current health management is ad-hoc. I need a proper medical review.

REQUIREMENTS:
- Mix of medical assessment, scheduling, and relationship building
- Show Rohan's analytical personality and time constraints  
- Include specific health data references (HRV, recovery scores)
- Demonstrate team expertise in their respective domains
- Realistic timestamps throughout the week (business hours Singapore time)
- Reference his travel schedule, young children, supportive wife"""

        return self.call_ollama(prompt)

    def generate_progress_conversations(self, month: int) -> str:
        scenarios = {
            2: "Early progress monitoring, Zone 2 cardio experiments, travel protocols",
            3: "Member feedback period, workout plan improvements, magnesium breakthrough",
            4: "Whoop data analysis, Zone 2 optimization, stress management introduction",
            6: "Post-illness recovery, CGM implementation, nutrition personalization",
            7: "Advanced protocols, travel optimization, glucose experiments",
            8: "Long-term goal setting, piano discussion, performance optimization"
        }

        scenario = scenarios.get(month, "General progress and protocol adjustments")

        prompt = self.get_system_prompt() + f"""

Generate 12-15 conversation messages for Month {month} (2025).

SCENARIO: {scenario}

Include realistic:
- Wearable data discussions (specific HRV, recovery numbers)
- Protocol adjustments based on member feedback
- Travel coordination and outcomes
- Health metric improvements/setbacks
- Decision-making with clear rationales
- Team coordination for member needs

Show progression in relationship and member's growing engagement with the process."""

        return self.call_ollama(prompt)

    def generate_setback_conversations(self) -> str:
        prompt = self.get_system_prompt() + """

Generate 20-25 messages for ILLNESS SETBACK period (May 2-7, 2025).

SCENARIO: Viral infection detection and management
- Whoop data shows 12bpm RHR increase, 45% HRV drop
- Board meeting scheduled for next day (critical timing)  
- Team implements sick day protocol
- Coordination for meeting rescheduling
- IV therapy arrangement, medical letter
- Recovery monitoring and gradual return

Show crisis management, team coordination, and data-driven medical decisions.
Include specific biomarker numbers and timestamps."""

        return self.call_ollama(prompt)

    def generate_breakthrough_conversations(self) -> str:
        prompt = self.get_system_prompt() + """

Generate 10-12 messages showing KEY BREAKTHROUGH moments:

1. First successful Zone 2 cardio (25 minutes stable) - April 2025
2. Sleep improvement with magnesium (8 min vs 25 min latency) - March 2025  
3. CGM sushi experiment (180→140 glucose) - July 2025
4. Blue-light glasses + shutdown ritual success - June 2025

Show member excitement, data validation, and team analysis of what worked.
Include specific numbers and member's analytical satisfaction with results."""

        return self.call_ollama(prompt)

    def parse_ollama_response(self, response: str, month: int = None) -> List[Dict]:
        """Parse Ollama response with proper date formatting"""
        conversations = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('[') and ']' in line and ':' in line:
                try:
                    end_bracket = line.find(']')
                    timestamp_str = line[1:end_bracket].strip()
                    
                    # ✅ Handle different date formats
                    if ',' in timestamp_str:
                        # Format: [DD/MM/YY, HH:MM AM/PM]
                        date_part, time_part = timestamp_str.split(', ')
                        if '/' in date_part and len(date_part.split('/')) == 3:
                            day, month_num, year = date_part.split('/')
                            # Convert to full datetime string for parsing
                            full_timestamp = f"20{year}-{month_num.zfill(2)}-{day.zfill(2)} {time_part}"
                        else:
                            full_timestamp = timestamp_str
                    else:
                        full_timestamp = timestamp_str
                    
                    remainder = line[end_bracket+1:].strip()
                    if ':' in remainder:
                        colon_pos = remainder.find(':')
                        sender = remainder[:colon_pos].strip()
                        message = remainder[colon_pos+1:].strip()
                        
                        # Clean sender name
                        if '(' in sender and ')' in sender:
                            sender = sender.split('(')[0].strip()
                        
                        # Map to actual display names
                        display_sender = self.sender_mapping.get(sender, sender)
                        
                        conversations.append({
                            'timestamp': full_timestamp,
                            'sender': display_sender,
                            'sender_role': self.get_sender_role(display_sender),
                            'message': message,
                            'category': self.categorize_message(message, display_sender),
                            'month': month or 1
                        })
                        
                except Exception as e:
                    print(f"Error parsing line '{line}': {e}")
                    continue
        
        return conversations
    
    def get_sender_role(self, sender):
        """Get sender role for UI display"""
        role_mapping = {
            'Rohan Patel': 'Member',
            'Ruby': 'Concierge',
            'Dr. Warren': 'Medical Strategist',  
            'Advik': 'Performance Scientist',
            'Carla': 'Nutritionist',
            'Rachel': 'PT/Physiotherapist',
            'Neel': 'Concierge Lead',
            'Dr. Evans': 'Stress Management'
        }
        return role_mapping.get(sender, 'Team Member')

    def categorize_message(self, message: str, sender: str) -> str:
        """Categorize message based on content"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['emergency', 'urgent', 'critical', 'immediately']):
            return 'emergency'
        elif any(word in message_lower for word in ['data', 'hrv', 'whoop', 'recovery', 'sleep']):
            return 'data_analysis'
        elif any(word in message_lower for word in ['exercise', 'zone 2', 'workout', 'cardio']):
            return 'exercise'
        elif any(word in message_lower for word in ['nutrition', 'food', 'supplement', 'cgm']):
            return 'nutrition'
        elif any(word in message_lower for word in ['travel', 'trip', 'flight', 'protocol']):
            return 'travel'
        elif any(word in message_lower for word in ['schedule', 'appointment', 'calendar']):
            return 'scheduling'
        elif sender == 'Rohan Patel':
            return 'member_inquiry'
        else:
            return 'team_response'

    def save_conversations_to_db(self, conversations: List[Dict], member_id: int):
        """Save conversations with proper member names"""
        successful_saves = 0
        
        member = Member.query.get(member_id)
        member_name = member.preferred_name if member else "Rohan Patel"
        
        for conv_data in conversations:
            try:
                # ✅ Better timestamp parsing
                timestamp_str = conv_data['timestamp']
                try:
                    timestamp = parse(timestamp_str)
                except:
                    # Fallback for date parsing
                    from datetime import datetime
                    timestamp = datetime.now()
                
                sender = conv_data['sender']
                
                # Handle team member vs member
                team_member = None
                if sender != member_name:  # It's a team member
                    team_member = TeamMember.query.filter_by(name=sender).first()
                    if not team_member:
                        team_member = TeamMember(
                            name=sender,
                            role=conv_data.get('sender_role', 'Team Member'),
                            specialty=conv_data.get('sender_role', 'Team Member'),
                            communication_style="Professional"
                        )
                        db.session.add(team_member)
                        db.session.flush()
                
                # ✅ Create conversation with proper sender name
                conversation = Conversation(
                    member_id=member_id,
                    team_member_id=team_member.id if team_member else None,
                    sender=sender,  # Use actual name for display
                    message=conv_data['message'],
                    category=conv_data.get('category', 'general'),
                    timestamp=timestamp,
                    month=conv_data.get('month', 1)
                )
                
                db.session.add(conversation)
                successful_saves += 1
                
            except Exception as e:
                print(f"Error saving conversation: {e}")
                continue
        
        db.session.commit()
        return successful_saves


    def generate_full_dataset(self, member_id: int):
        """Generate complete conversation dataset with robust error handling"""
        print("🚀 Starting conversation generation with Ollama...")
        total_generated = 0

        try:
            # Month 1: Onboarding
            print("📅 Generating Month 1 (Onboarding)...")
            try:
                response = self.generate_onboarding_conversations()
                if response.strip():  # Check if we got a response
                    conversations = self.parse_ollama_response(response, 1)
                    saved_count = self.save_conversations_to_db(conversations, member_id)
                    total_generated += saved_count
                    print(f"   ✅ Generated {saved_count} messages")
                else:
                    print("   ❌ No response from Ollama for Month 1")
            except Exception as e:
                print(f"   ❌ Error generating Month 1: {e}")

            # Continue with other months with similar error handling...
            for month in [2, 3, 4, 6, 7, 8]:
                print(f"📅 Generating Month {month} (Progress)...")
                try:
                    response = self.generate_progress_conversations(month)
                    if response.strip():
                        conversations = self.parse_ollama_response(response, month)
                        saved_count = self.save_conversations_to_db(conversations, member_id)
                        total_generated += saved_count
                        print(f"   ✅ Generated {saved_count} messages")
                    else:
                        print(f"   ❌ No response from Ollama for Month {month}")
                except Exception as e:
                    print(f"   ❌ Error generating Month {month}: {e}")

            # Month 5: Setback with error handling
            print("📅 Generating Month 5 (Illness Setback)...")
            try:
                response = self.generate_setback_conversations()
                if response.strip():
                    conversations = self.parse_ollama_response(response, 5)
                    saved_count = self.save_conversations_to_db(conversations, member_id)
                    total_generated += saved_count
                    print(f"   ✅ Generated {saved_count} messages")
            except Exception as e:
                print(f"   ❌ Error generating setback conversations: {e}")

            # Final count from database
            final_count = Conversation.query.filter_by(member_id=member_id).count()
            print(f"\n🎉 Total conversations saved to database: {final_count}")

            return final_count

        except Exception as e:
            print(f"💥 Fatal error in conversation generation: {e}")
            return total_generated
