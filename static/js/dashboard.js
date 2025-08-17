// static/js/dashboard.js
class HealthcareDashboard {
    constructor() {
        this.member_id = 1;
        this.charts = {};
        this.init();
    }

    init() {
        this.loadDashboardData();
        this.setupEventListeners();
    }

    async loadDashboardData() {
        try {
            // Load member data first
            await this.loadMemberData();
            
            // Load stats
            const statsResponse = await fetch('/api/stats');
            let stats = { days_in_program: 240, total_events: 0, breakthroughs: 2, team_members: 6 };
            
            if (statsResponse.ok) {
                const fetchedStats = await statsResponse.json();
                stats = { ...stats, ...fetchedStats };
            }
            this.updateStats(stats);

            // Load health metrics
            try {
                const metricsResponse = await fetch('/api/health-metrics');
                if (metricsResponse.ok) {
                    const metrics = await metricsResponse.json();
                    this.renderHealthMetricsChart(metrics);
                } else {
                    this.renderEmptyChart();
                }
            } catch (error) {
                console.warn('Health metrics not available:', error);
                this.renderEmptyChart();
            }

            // Load recent timeline events
            try {
                const timelineResponse = await fetch('/api/timeline');
                if (timelineResponse.ok) {
                    const timeline = await timelineResponse.json();
                    this.renderRecentActivity(timeline.slice(-4));
                } else {
                    this.renderEmptyActivity();
                }
            } catch (error) {
                console.warn('Timeline not available:', error);
                this.renderEmptyActivity();
            }

        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.loadFallbackData();
        }
    }

    // ✅ NEW: Load member data for profile display
    async loadMemberData() {
        try {
            const response = await fetch('/api/member/1');
            if (response.ok) {
                const member = await response.json();
                this.updateMemberProfile(member);
            }
        } catch (error) {
            console.error('Error loading member data:', error);
        }
    }

    // ✅ NEW: Update member profile display
    updateMemberProfile(member) {
        const profileName = document.querySelector('.profile-details h4');
        if (profileName) {
            profileName.textContent = member.preferred_name || member.name;
        }

        const memberOccupation = document.querySelector('.member-subtitle');
        if (memberOccupation) {
            memberOccupation.textContent = `${member.occupation} • ${member.location}`;
        }

        const memberAge = document.querySelector('.member-stats');
        if (memberAge) {
            memberAge.innerHTML = `
                <span>Age: ${member.age}</span>
                <span>Gender: ${member.gender}</span>
                <span>Location: ${member.location}</span>
            `;
        }

        // ✅ Update health goals with proper formatting
        const healthGoalsList = document.querySelector('.health-goals ul');
        if (healthGoalsList && member.health_goals) {
            healthGoalsList.innerHTML = '';
            member.health_goals.forEach(goal => {
                const li = document.createElement('li');
                li.textContent = goal;
                healthGoalsList.appendChild(li);
            });
        }

        // ✅ Update condition tags
        const conditionTags = document.querySelector('.condition-tags');
        if (conditionTags && member.chronic_conditions) {
            conditionTags.innerHTML = '';
            member.chronic_conditions.forEach(condition => {
                const tag = document.createElement('span');
                tag.className = 'condition-tag';
                tag.textContent = condition;
                conditionTags.appendChild(tag);
            });
        }
    }

    renderRecentActivity(events) {
        const activityContainer = document.getElementById('recentActivity');
        if (!activityContainer) return;

        activityContainer.innerHTML = '';

        events.forEach(event => {
            const activityItem = document.createElement('div');
            activityItem.className = 'activity-item';
            // ✅ Proper date formatting
            const formattedDate = this.formatDate(event.date);
            activityItem.innerHTML = `
                <div class="activity-icon"></div>
                <div class="activity-content">
                    <div class="activity-title">${event.title}</div>
                    <div class="activity-date">${formattedDate}</div>
                </div>
            `;
            activityItem.addEventListener('click', () => {
                this.showEpisodeModal(event);
            });
            activityContainer.appendChild(activityItem);
        });
    }

    showEpisodeModal(event) {
        const modalTitle = document.getElementById('modalTitle');
        const modalBody = document.getElementById('modalBody');
        const modal = document.getElementById('episodeModal');
        
        if (!modalTitle || !modalBody || !modal) return;
        
        modalTitle.textContent = event.title;
        // ✅ Proper date formatting in modal
        const formattedDate = this.formatDate(event.date);
        modalBody.innerHTML = `
            <div style="margin-bottom: 16px;">
                <strong>Date:</strong> ${formattedDate}
            </div>
            <div style="margin-bottom: 16px;">
                <strong>Category:</strong> ${event.category ? event.category.charAt(0).toUpperCase() + event.category.slice(1) : 'N/A'}
            </div>
            <div style="margin-bottom: 16px;">
                <strong>Description:</strong><br>
                ${event.description || 'No description available'}
            </div>
            <div style="margin-bottom: 16px;">
                <strong>Outcome:</strong><br>
                ${event.outcome || 'No outcome recorded'}
            </div>
            <div style="margin-bottom: 16px;">
                <strong>Team Members:</strong> ${event.team_members ? event.team_members.join(', ') : 'None'}
            </div>
            <div style="margin-bottom: 16px;">
                <strong>Response Time:</strong> ${event.response_time || 'N/A'}
            </div>
            <div style="margin-bottom: 16px;">
                <strong>Time to Resolution:</strong> ${event.time_to_resolution || 'N/A'}
            </div>
            ${event.friction_points ? `
                <div style="margin-bottom: 16px;">
                    <strong>Friction Points:</strong><br>
                    ${event.friction_points}
                </div>
            ` : ''}
        `;
        modal.classList.remove('hidden');
    }

    // ✅ Improved date formatting
    formatDate(dateString) {
        const date = new Date(dateString);
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear().toString().slice(-2);
        return `${day}/${month}/${year}`;
    }

    // Rest of methods remain the same...
    updateStats(stats) {
        if (document.getElementById('totalDays')) {
            document.getElementById('totalDays').textContent = stats.days_in_program || 240;
        }
        if (document.getElementById('totalEvents')) {
            document.getElementById('totalEvents').textContent = stats.total_events || 0;
        }
        if (document.getElementById('breakthroughs')) {
            document.getElementById('breakthroughs').textContent = stats.breakthroughs || 0;
        }
        if (document.getElementById('teamMembers')) {
            document.getElementById('teamMembers').textContent = stats.team_members || 0;
        }
    }

    renderHealthMetricsChart(metrics) {
        const ctx = document.getElementById('healthMetricsChart');
        if (!ctx) return;

        const chartCtx = ctx.getContext('2d');

        let labels = [];
        let hrvData = [];
        let recoveryData = [];

        if (metrics.hrv && metrics.recovery_score) {
            labels = metrics.hrv.map(item => this.formatDate(item.date));
            hrvData = metrics.hrv.map(item => item.value);
            recoveryData = metrics.recovery_score.map(item => item.value);
        }

        this.charts.healthMetrics = new Chart(chartCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'HRV',
                    data: hrvData,
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y'
                }, {
                    label: 'Recovery Score',
                    data: recoveryData,
                    borderColor: '#FFC185',
                    backgroundColor: 'rgba(255, 193, 133, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'HRV (ms)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Recovery Score (%)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                }
            }
        });
    }

    renderEmptyChart() {
        const ctx = document.getElementById('healthMetricsChart');
        if (!ctx) return;
        
        const chartCtx = ctx.getContext('2d');
        chartCtx.fillStyle = '#64748b';
        chartCtx.fillRect(0, 0, ctx.width, ctx.height);
        chartCtx.fillStyle = 'white';
        chartCtx.font = '16px Arial';
        chartCtx.fillText('No health metrics data available', 50, ctx.height/2);
    }

    renderEmptyActivity() {
        const activityContainer = document.getElementById('recentActivity');
        if (!activityContainer) return;
        
        activityContainer.innerHTML = '<p class="text-gray-500">No recent activity available</p>';
    }

    loadFallbackData() {
        this.updateStats({ days_in_program: 240, total_events: 0, breakthroughs: 2, team_members: 6 });
        this.renderEmptyChart();
        this.renderEmptyActivity();
    }

    closeModal() {
        const modal = document.getElementById('episodeModal');
        if (modal) {
            modal.classList.add('hidden');
        }
    }

    setupEventListeners() {
        // Modal controls
        const modalClose = document.getElementById('modalClose');
        const modalOverlay = document.getElementById('modalOverlay');

        if (modalClose) {
            modalClose.addEventListener('click', () => this.closeModal());
        }

        if (modalOverlay) {
            modalOverlay.addEventListener('click', () => this.closeModal());
        }

        // Generate conversations button
        const generateBtn = document.getElementById('generateConversationsBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateConversations());
        }
    }

    async generateConversations() {
        const btn = document.getElementById('generateConversationsBtn');
        const status = document.getElementById('generationStatus');

        if (!btn || !status) return;

        btn.disabled = true;
        btn.textContent = 'Generating...';
        status.innerHTML = '<p style="color: #1FB8CD;">🤖 Connecting to Ollama and generating conversations...</p>';

        try {
            const response = await fetch('/api/generate-conversations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (result.success) {
                status.innerHTML = `
                    <p style="color: #22c55e;">✅ Successfully generated ${result.total_conversations} conversations!</p>
                    <p>Refresh the page to see the new conversations in the dashboard.</p>
                `;
            } else {
                status.innerHTML = `<p style="color: #ef4444;">❌ Error: ${result.error}</p>`;
            }
        } catch (error) {
            status.innerHTML = `
                <p style="color: #ef4444;">❌ Error generating conversations: ${error.message}</p>
                <p style="color: #f59e0b;">⚠️ Make sure Ollama is running on http://localhost:11434</p>
            `;
        } finally {
            btn.disabled = false;
            btn.textContent = 'Generate Conversations';
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('healthMetricsChart') || 
        document.getElementById('recentActivity') ||
        document.getElementById('generateConversationsBtn')) {
        new HealthcareDashboard();
    }
});
