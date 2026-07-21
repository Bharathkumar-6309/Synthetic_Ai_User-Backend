-- Synthetic AI User Backend Seed Data
-- Initial data for testing and demonstration

USE synthetic_ai_user;

-- Insert sample user
INSERT INTO users (id, email, name) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'demo@synthetic.ai', 'Demo User')
ON DUPLICATE KEY UPDATE email=email;

-- Insert sample experiment
INSERT INTO experiments (id, owner_id, title, product_description, target_audience, research_objectives, persona_count, status) VALUES 
('exp-001', '550e8400-e29b-41d4-a716-446655440000', 
'AI Productivity Assistant', 
'An AI-powered assistant that helps remote teams manage tasks, schedule meetings, and automate workflows using natural language commands.', 
'Remote workers, team leads, project managers in tech companies', 
'Validate market fit, understand pricing sensitivity, identify key features', 
6, 'personas_ready')
ON DUPLICATE KEY UPDATE title=title;

-- Insert sample personas
INSERT INTO personas (id, experiment_id, name, age, gender, occupation, location, income_bracket, education_level, personality_traits, behavioral_patterns, tech_savviness, daily_habits, core_values, motivations, pain_points, risk_tolerance, bio, avatar_seed, quote, persona_hash, consistency_seed, generation_source, product_fit_score) VALUES
('persona-001', 'exp-001', 'Alex Chen', 32, 'other', 'Software Engineer', 'San Francisco', '$120k-$150k', 'Master\'s', 
'["analytical", "detail-oriented", "efficient"]', 
'["coding", "code reviews", "standup meetings"]', 
'high', 
'["morning coding", "coffee breaks", "GitHub review"]', 
'["efficiency", "quality", "innovation"]', 
'["productivity", "learning", "career growth"]', 
'["context switching", "interrupted flow", "manual tasks"]', 
'moderate', 
'Experienced software engineer at a fast-growing startup. Loves automation tools that save time and reduce cognitive load. Always looking for ways to optimize workflows.', 
'alex_chen_32', 
'I\'d pay for something that actually saves me time, not just another tool to manage.', 
'hash_alex_001', 1, 'synthetic_fallback', 8.5),

('persona-002', 'exp-001', 'Sarah Miller', 28, 'female', 'Product Manager', 'New York', '$100k-$120k', 'Bachelor\'s', 
'["organized", "communicative", "data-driven"]', 
'["stakeholder meetings", "roadmap planning", "user research"]', 
'high', 
'["Slack", "Jira", "analytics review"]', 
'["alignment", "transparency", "user-centricity"]', 
'["team success", "product impact", "customer satisfaction"]', 
'["miscommunication", "unclear requirements", "scope creep"]', 
'low', 
'Product manager at a mid-sized SaaS company. Focused on shipping features that users actually need. Skeptical of tools that don\'t integrate well with existing stack.', 
'sarah_miller_28', 
'Show me the ROI and I\'m interested. Otherwise, it\'s just noise.', 
'hash_sarah_002', 2, 'synthetic_fallback', 7.0),

('persona-003', 'exp-001', 'Marcus Johnson', 35, 'male', 'Team Lead', 'Austin', '$130k-$160k', 'Master\'s', 
'["strategic", "mentoring", "results-oriented"]', 
'["1:1s", "sprint planning", "cross-functional sync"]', 
'high', 
'["team standup", "code review", "strategic planning"]', 
'["accountability", "growth", "team success"]', 
'["team productivity", "career development", "delivering value"]', 
'["blocked team members", "unclear priorities", "technical debt"]', 
'moderate', 
'Technical team lead at a Fortune 500 company. Balances technical excellence with business outcomes. Values tools that help scale team effectiveness.', 
'marcus_johnson_35', 
'If it helps my team ship faster and with fewer bugs, I\'m all in.', 
'hash_marcus_003', 3, 'synthetic_fallback', 8.0),

('persona-004', 'exp-001', 'Emily Rodriguez', 26, 'female', 'UX Designer', 'Los Angeles', '$70k-$90k', 'Bachelor\'s', 
'["creative", "empathetic", "user-focused"]', 
'["user interviews", "design sprints", "prototyping"]', 
'high', 
'["Figma", "user testing", "design critique"]', 
'["user experience", "accessibility", "aesthetics"]', 
'["solving user problems", "creative expression", "impact"]', 
'["ugly interfaces", "confusing workflows", "lack of user research"]', 
'high', 
'UX designer at a design agency. Passionate about creating intuitive experiences. Quick to adopt tools that enhance design workflow and user understanding.', 
'emily_rodriguez_26', 
'Design matters. If it\'s clunky, users won\'t use it no matter how powerful it is.', 
'hash_emily_004', 4, 'synthetic_fallback', 7.5),

('persona-005', 'exp-001', 'David Kim', 40, 'male', 'Engineering Manager', 'Seattle', '$150k-$180k', 'PhD', 
'["pragmatic", "decisive", "mentoring"]', 
'["hiring", "budget planning", "architecture reviews"]', 
'medium', 
'["executive sync", "team retros", "performance reviews"]', 
'["sustainability", "scalability", "team growth"]', 
'["building great teams", "technical excellence", "business impact"]', 
'["burnout", "technical debt", "hiring challenges"]', 
'low', 
'Engineering manager at a large tech company. Focuses on long-term technical strategy and team health. Cautious about adopting new tools without clear business case.', 
'david_kim_40', 
'I need to see how this scales before committing my team to it.', 
'hash_david_005', 5, 'synthetic_fallback', 6.5),

('persona-006', 'exp-001', 'Jessica Taylor', 29, 'female', 'Startup Founder', 'Boston', '$80k-$100k', 'MBA', 
'["visionary", "resourceful", "fast-moving"]', 
'["pitching", "product development", "customer calls"]', 
'high', 
'["customer development", "product iteration", "team building"]', 
'["speed", "innovation", "customer delight"]', 
'["building something people love", "market validation", "growth"]', 
'["running out of runway", "product-market fit", "hiring"]', 
'high', 
'Founder of an early-stage startup. Always looking for tools that give competitive advantage and help move faster. Willing to try new things if they promise real impact.', 
'jessica_taylor_29', 
'If this gives me an edge, I\'ll use it. Time is my most valuable asset.', 
'hash_jessica_006', 6, 'synthetic_fallback', 9.0)
ON DUPLICATE KEY UPDATE name=name;

-- Insert sample survey
INSERT INTO surveys (id, experiment_id, question, status) VALUES 
('survey-001', 'exp-001', 
'What are your biggest challenges with current task management tools?', 
'completed')
ON DUPLICATE KEY UPDATE question=question;

-- Insert sample responses
INSERT INTO responses (id, survey_id, persona_id, answer_text, sentiment) VALUES
('resp-001', 'survey-001', 'persona-001', 
'My biggest challenge is context switching between different tools. I have Jira for tasks, Slack for communication, and email for everything else. It\'s fragmented and I lose track of things.', 
'neutral'),
('resp-002', 'survey-001', 'persona-002', 
'Lack of integration is a major pain point. Our tools don\'t talk to each other, so I spend too much time manually updating status across platforms. Also, the UI complexity in some tools is overwhelming.', 
'negative'),
('resp-003', 'survey-001', 'persona-003', 
'The main issue is that tools don\'t scale well with team growth. What works for 5 people breaks at 20. Also, reporting and visibility into what the team is actually working on is often unclear.', 
'neutral'),
('resp-004', 'survey-001', 'persona-004', 
'Poor user experience is my biggest frustration. Many tools are powerful but incredibly clunky to use. The learning curve is steep, and they don\'t follow good UX principles. It wastes time and frustrates users.', 
'negative'),
('resp-005', 'survey-001', 'persona-005', 
'I worry about security and compliance. Many tools don\'t meet enterprise requirements, and getting approval is difficult. Also, the total cost of ownership across multiple tools adds up quickly.', 
'negative'),
('resp-006', 'survey-001', 'persona-006', 
'Speed and simplicity. I need something that works immediately without complex setup. Current tools require too much configuration and onboarding time. As a startup, I can\'t afford that overhead.', 
'negative')
ON DUPLICATE KEY UPDATE answer_text=answer_text;

-- Insert sample insights
INSERT INTO insights (id, experiment_id, would_use_pct, would_pay_pct, themes, sentiment, key_quotes, suggestions, user_wants_summary, persona_scores, raw_data) VALUES 
('insight-001', 'exp-001', 
85, 
65, 
'[{"theme": "Integration issues", "mentions_pct": 83}, {"theme": "Poor UX", "mentions_pct": 67}, {"theme": "Scalability concerns", "mentions_pct": 50}, {"theme": "Security/compliance", "mentions_pct": 33}, {"theme": "Setup complexity", "mentions_pct": 50}]', 
'{"positive": 2, "neutral": 2, "negative": 2}', 
'[{"quote": "My biggest challenge is context switching between different tools.", "persona": "Alex Chen"}, {"quote": "Poor user experience is my biggest frustration.", "persona": "Emily Rodriguez"}, {"quote": "If this gives me an edge, I\'ll use it.", "persona": "Jessica Taylor"}]', 
'[{"suggestion": "Deep integrations with popular tools (Slack, Jira, GitHub)", "category": "Feature", "priority": "high", "personas": ["Alex Chen", "Sarah Miller", "Marcus Johnson"]}, {"suggestion": "Simplify onboarding and reduce setup time", "category": "UX", "priority": "high", "personas": ["Jessica Taylor", "Emily Rodriguez"]}, {"suggestion": "Enterprise-grade security and compliance certifications", "category": "Security", "priority": "medium", "personas": ["David Kim"]}, {"suggestion": "Better reporting and team visibility features", "category": "Feature", "priority": "medium", "personas": ["Marcus Johnson"]}]', 
'Users want a unified, integrated tool that reduces context switching, has excellent UX, scales with team growth, and can be set up quickly. Security and compliance are important for enterprise adoption.', 
'{"Alex Chen": 8.5, "Sarah Miller": 7.0, "Marcus Johnson": 8.0, "Emily Rodriguez": 7.5, "David Kim": 6.5, "Jessica Taylor": 9.0}', 
'{"survey_responses_count": 6, "interview_messages_count": 0, "feedback_transcript_length": 1250}')
ON DUPLICATE KEY UPDATE would_use_pct=would_use_pct;

-- Insert sample report
INSERT INTO reports (id, experiment_id, title, summary, persona_profiles, response_highlights, insight_summary, validation_scoring, recommendations, status, file_path) VALUES 
('report-001', 'exp-001', 
'Research Report: AI Productivity Assistant', 
'This report summarizes research findings for AI Productivity Assistant. The product targets Remote workers, team leads, project managers in tech companies. Product fit score: 7.8/10. 85% of personas would use this product, and 65% would pay for it.

Key user needs: Users want a unified, integrated tool that reduces context switching, has excellent UX, scales with team growth, and can be set up quickly. Security and compliance are important for enterprise adoption.', 
'[
  {"name": "Alex Chen", "age": 32, "occupation": "Software Engineer", "location": "San Francisco", "personality_traits": ["analytical", "detail-oriented", "efficient"], "core_values": ["efficiency", "quality", "innovation"], "bio": "Experienced software engineer at a fast-growing startup. Loves automation tools that save time and reduce cognitive load.", "product_fit_score": 8.5},
  {"name": "Sarah Miller", "age": 28, "occupation": "Product Manager", "location": "New York", "personality_traits": ["organized", "communicative", "data-driven"], "core_values": ["alignment", "transparency", "user-centricity"], "bio": "Product manager at a mid-sized SaaS company. Focused on shipping features that users actually need.", "product_fit_score": 7.0},
  {"name": "Marcus Johnson", "age": 35, "occupation": "Team Lead", "location": "Austin", "personality_traits": ["strategic", "mentoring", "results-oriented"], "core_values": ["accountability", "growth", "team success"], "bio": "Technical team lead at a Fortune 500 company. Balances technical excellence with business outcomes.", "product_fit_score": 8.0},
  {"name": "Emily Rodriguez", "age": 26, "occupation": "UX Designer", "location": "Los Angeles", "personality_traits": ["creative", "empathetic", "user-focused"], "core_values": ["user experience", "accessibility", "aesthetics"], "bio": "UX designer at a design agency. Passionate about creating intuitive experiences.", "product_fit_score": 7.5},
  {"name": "David Kim", "age": 40, "occupation": "Engineering Manager", "location": "Seattle", "personality_traits": ["pragmatic", "decisive", "mentoring"], "core_values": ["sustainability", "scalability", "team growth"], "bio": "Engineering manager at a large tech company. Focuses on long-term technical strategy.", "product_fit_score": 6.5},
  {"name": "Jessica Taylor", "age": 29, "occupation": "Startup Founder", "location": "Boston", "personality_traits": ["visionary", "resourceful", "fast-moving"], "core_values": ["speed", "innovation", "customer delight"], "bio": "Founder of an early-stage startup. Always looking for tools that competitive advantage.", "product_fit_score": 9.0}
]', 
'[
  {"persona_name": "Alex Chen", "question": "What are your biggest challenges with current task management tools?", "answer": "My biggest challenge is context switching between different tools. I have Jira for tasks, Slack for communication, and email for everything else.", "sentiment": "neutral"},
  {"persona_name": "Sarah Miller", "question": "What are your biggest challenges with current task management tools?", "answer": "Lack of integration is a major pain point. Our tools don\'t talk to each other, so I spend too much time manually updating status.", "sentiment": "negative"},
  {"persona_name": "Emily Rodriguez", "question": "What are your biggest challenges with current task management tools?", "answer": "Poor user experience is my biggest frustration. Many tools are powerful but incredibly clunky to use.", "sentiment": "negative"}
]', 
'{"would_use_pct": 85, "would_pay_pct": 65, "themes": [{"theme": "Integration issues", "mentions_pct": 83}, {"theme": "Poor UX", "mentions_pct": 67}], "sentiment": {"positive": 2, "neutral": 2, "negative": 2}, "key_quotes": [{"quote": "My biggest challenge is context switching", "persona": "Alex Chen"}], "suggestions": [{"suggestion": "Deep integrations with popular tools", "category": "Feature", "priority": "high"}], "user_wants_summary": "Users want a unified, integrated tool that reduces context switching.", "persona_scores": {"Alex Chen": 8.5, "Sarah Miller": 7.0}}', 
'{"overall_product_fit_score": 7.8, "would_use_percentage": 85, "would_pay_percentage": 65}', 
'[
  {"suggestion": "Deep integrations with popular tools (Slack, Jira, GitHub)", "category": "Feature", "priority": "high"},
  {"suggestion": "Simplify onboarding and reduce setup time", "category": "UX", "priority": "high"},
  {"suggestion": "Enterprise-grade security and compliance certifications", "category": "Security", "priority": "medium"}
]', 
'ready', 
NULL)
ON DUPLICATE KEY UPDATE title=title;
