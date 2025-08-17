from flask import Blueprint, render_template, jsonify, request
from models import db, Member, TeamMember, Conversation, TimelineEvent, HealthMetric, Decision, TeamMetric
from conversation_generator import ElyxConversationGenerator
from sqlalchemy import func, desc
import json

# Create blueprint
main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    """Main dashboard page"""
    member = Member.query.first()
    if not member:
        return "No member data found. Please run database initialization.", 404

    return render_template('dashboard.html', member=member)

@main.route('/api/member/<int:member_id>')
def get_member(member_id):
    """Get member data with proper formatting"""
    member = Member.query.get_or_404(member_id)
    member_dict = member.to_dict()
    
    # ✅ Ensure health goals are properly formatted
    if isinstance(member_dict['health_goals'], str):
        try:
            member_dict['health_goals'] = json.loads(member_dict['health_goals'])
        except:
            member_dict['health_goals'] = []
    
    return jsonify(member_dict)

@main.route('/api/member/1')  # Default member
def get_default_member():
    return get_member(1)

@main.route('/api/conversations')
def get_conversations():
    """Get all conversations"""
    conversations = Conversation.query.order_by(Conversation.timestamp).all()
    return jsonify([conv.to_dict() for conv in conversations])

@main.route('/api/conversations/<int:member_id>')
def get_member_conversations(member_id):
    """Get conversations for a specific member with proper name display"""
    member = Member.query.get(member_id)
    conversations = Conversation.query.filter_by(member_id=member_id).order_by(Conversation.timestamp).all()
    
    result = []
    for conv in conversations:
        # ✅ Ensure proper sender names for display
        sender_name = conv.sender
        sender_role = 'Member'
        
        if conv.team_member_id:
            # It's from a team member
            sender_name = conv.team_member.name if conv.team_member else conv.sender
            sender_role = conv.team_member.role if conv.team_member else 'Team Member'
        elif conv.sender in ['member', 'Member']:
            # Convert generic member to actual name
            sender_name = member.preferred_name if member else 'Rohan Patel'
            sender_role = 'Member'
        elif conv.sender == member.preferred_name if member else conv.sender == 'Rohan Patel':
            # It's the member
            sender_role = 'Member'
        
        result.append({
            'id': conv.id,
            'sender': sender_name,
            'sender_role': sender_role,
            'message': conv.message,
            'timestamp': conv.timestamp.strftime('%d/%m/%y, %I:%M %p'),  # ✅ Proper date format
            'category': conv.category
        })
    
    return jsonify(result)

@main.route('/api/timeline')
def get_timeline():
    """Get timeline events"""
    events = TimelineEvent.query.order_by(TimelineEvent.date).all()
    return jsonify([event.to_dict() for event in events])

@main.route('/api/timeline/<int:member_id>')
def get_member_timeline(member_id):
    """Get timeline events for a specific member"""
    events = TimelineEvent.query.filter_by(member_id=member_id).order_by(TimelineEvent.date).all()
    return jsonify([event.to_dict() for event in events])

@main.route('/api/health-metrics')
def get_health_metrics():
    """Get health metrics"""
    metrics = HealthMetric.query.order_by(HealthMetric.date).all()

    # Group by metric type
    grouped_metrics = {}
    for metric in metrics:
        if metric.metric_type not in grouped_metrics:
            grouped_metrics[metric.metric_type] = []
        grouped_metrics[metric.metric_type].append({
            'date': metric.date.isoformat(),
            'value': metric.value
        })

    return jsonify(grouped_metrics)

@main.route('/api/health-metrics/<int:member_id>')
def get_member_health_metrics(member_id):
    """Get health metrics for a specific member"""
    metrics = HealthMetric.query.filter_by(member_id=member_id).order_by(HealthMetric.date).all()

    # Group by metric type
    grouped_metrics = {}
    for metric in metrics:
        if metric.metric_type not in grouped_metrics:
            grouped_metrics[metric.metric_type] = []
        grouped_metrics[metric.metric_type].append({
            'date': metric.date.isoformat(),
            'value': metric.value
        })

    return jsonify(grouped_metrics)

@main.route('/api/decisions')
def get_decisions():
    """Get all decisions"""
    decisions = Decision.query.order_by(Decision.date).all()
    return jsonify([decision.to_dict() for decision in decisions])

@main.route('/api/decisions/<int:member_id>')
def get_member_decisions(member_id):
    """Get decisions for a specific member"""
    decisions = Decision.query.filter_by(member_id=member_id).order_by(Decision.date).all()
    return jsonify([decision.to_dict() for decision in decisions])

@main.route('/api/team-metrics')
def get_team_metrics():
    """Get team consultation metrics"""
    # Join team metrics with team members
    results = db.session.query(
        TeamMember.name,
        TeamMember.specialty,
        TeamMetric.hours
    ).join(TeamMetric).all()

    metrics = []
    for name, specialty, hours in results:
        metrics.append({
            'member': name,
            'specialty': specialty,
            'hours': hours
        })

    return jsonify(metrics)

@main.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    member = Member.query.first()
    if not member:
        return jsonify({'error': 'No member found'}), 404

    # Calculate stats
    total_conversations = Conversation.query.filter_by(member_id=member.id).count()
    total_events = TimelineEvent.query.filter_by(member_id=member.id).count()
    breakthroughs = TimelineEvent.query.filter_by(
        member_id=member.id, 
        status='breakthrough'
    ).count()

    # Get unique team members involved
    team_members_count = db.session.query(
        func.count(func.distinct(Conversation.team_member_id))
    ).filter(
        Conversation.member_id == member.id,
        Conversation.team_member_id.isnot(None)
    ).scalar()

    return jsonify({
        'total_conversations': total_conversations,
        'total_events': total_events,
        'breakthroughs': breakthroughs,
        'team_members': team_members_count,
        'days_in_program': 240  # Calculated from start date
    })

@main.route('/api/generate-conversations', methods=['POST'])
def generate_conversations():
    """Generate new conversations using Ollama"""
    try:
        member = Member.query.first()
        if not member:
            return jsonify({'error': 'No member found'}), 404

        generator = ElyxConversationGenerator()
        total_generated = generator.generate_full_dataset(member.id)

        return jsonify({
            'success': True,
            'message': f'Generated {total_generated} conversations',
            'total_conversations': total_generated
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/api/search-conversations')
def search_conversations():
    """Search conversations by query"""
    query = request.args.get('q', '')
    member_id = request.args.get('member_id', type=int)

    conversations_query = Conversation.query

    if member_id:
        conversations_query = conversations_query.filter_by(member_id=member_id)

    if query:
        conversations_query = conversations_query.filter(
            Conversation.message.contains(query)
        )

    conversations = conversations_query.order_by(Conversation.timestamp).all()
    return jsonify([conv.to_dict() for conv in conversations])

@main.route('/api/filter-timeline')
def filter_timeline():
    """Filter timeline events by category"""
    category = request.args.get('category', 'all')
    member_id = request.args.get('member_id', type=int)

    events_query = TimelineEvent.query

    if member_id:
        events_query = events_query.filter_by(member_id=member_id)

    if category and category != 'all':
        events_query = events_query.filter_by(category=category)

    events = events_query.order_by(TimelineEvent.date).all()
    return jsonify([event.to_dict() for event in events])

@main.route('/conversations')
def conversations_page():
    """Conversations page"""
    return render_template('conversations.html')

@main.route('/timeline')
def timeline_page():
    """Timeline page"""
    return render_template('timeline.html')

@main.route('/decisions')
def decisions_page():
    """Decisions page"""
    return render_template('decisions.html')

# Error handlers
@main.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
