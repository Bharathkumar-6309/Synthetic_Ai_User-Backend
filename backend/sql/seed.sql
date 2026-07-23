-- Synthetic AI User Backend Seed Data
-- Full demonstration data: 3 users, 3 experiments, 18 personas, 3 surveys,
-- 18 responses, 9 interview sessions, 3 insights, 3 reports

USE synthetic_ai_user;

-- ============================================================
-- USERS
-- ============================================================
INSERT INTO users (id, email, name) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'demo@synthetic.ai',    'Demo User'),
('user-002',                              'priya@researchlab.io', 'Priya Sharma'),
('user-003',                              'carlos@productforge.co','Carlos Mendez')
ON DUPLICATE KEY UPDATE email=email;

-- ============================================================
-- EXPERIMENTS
-- ============================================================
INSERT INTO experiments (id, owner_id, title, product_description, target_audience, research_objectives, persona_count, status) VALUES
('exp-001', '550e8400-e29b-41d4-a716-446655440000',
 'AI Productivity Assistant',
 'An AI-powered assistant that helps remote teams manage tasks, schedule meetings, and automate workflows using natural language commands.',
 'Remote workers, team leads, project managers in tech companies',
 'Validate market fit, understand pricing sensitivity, identify key features',
 6, 'completed'),

('exp-002', 'user-002',
 'HealthTrack Pro',
 'A wearable-integrated mobile app that tracks nutrition, exercise, sleep, and mental wellness. Uses AI to give personalised health recommendations and coach users toward long-term habits.',
 'Health-conscious adults aged 25-45 who own a smartwatch or fitness band',
 'Identify primary use cases, understand willingness to pay for premium tier, discover barriers to consistent app usage',
 6, 'completed'),

('exp-003', 'user-003',
 'EduFlow LMS',
 'A lightweight learning management system designed for independent educators, bootcamps, and small online course creators. Includes video hosting, quizzes, live sessions, and student analytics.',
 'Independent educators, course creators, and small bootcamp operators with fewer than 500 students',
 'Understand current LMS pain points, assess feature priorities, validate pricing model',
 6, 'personas_ready')
ON DUPLICATE KEY UPDATE title=title;

-- ============================================================
-- PERSONAS  --- Experiment 1: AI Productivity Assistant (6)
-- ============================================================
INSERT INTO personas (id, experiment_id, name, age, gender, occupation, location, income_bracket, education_level,
  personality_traits, behavioral_patterns, tech_savviness, daily_habits, core_values, motivations, pain_points,
  risk_tolerance, bio, avatar_seed, quote, persona_hash, consistency_seed, generation_source, product_fit_score) VALUES

('persona-001', 'exp-001', 'Alex Chen', 32, 'other', 'Software Engineer', 'San Francisco', '$120k-$150k', 'Masters',
 '["analytical","detail-oriented","efficient"]',
 '["coding","code reviews","standup meetings"]',
 'high',
 '["morning coding","coffee breaks","GitHub review"]',
 '["efficiency","quality","innovation"]',
 '["productivity","learning","career growth"]',
 '["context switching","interrupted flow","manual tasks"]',
 'moderate',
 'Experienced software engineer at a fast-growing startup. Loves automation tools that save time and reduce cognitive load. Loses 90 minutes daily to ticket management.',
 'alex_chen_32',
 'I would pay for something that actually saves me time, not just another tool to manage.',
 'hash_alex_001', 1, 'synthetic_fallback', 8.5),

('persona-002', 'exp-001', 'Sarah Miller', 28, 'female', 'Product Manager', 'New York', '$100k-$120k', 'Bachelors',
 '["organized","communicative","data-driven"]',
 '["stakeholder meetings","roadmap planning","user research"]',
 'high',
 '["Slack","Jira","analytics review"]',
 '["alignment","transparency","user-centricity"]',
 '["team success","product impact","customer satisfaction"]',
 '["miscommunication","unclear requirements","scope creep"]',
 'low',
 'Product manager at a mid-sized SaaS company. Focused on shipping features that users actually need. Skeptical of tools that do not integrate well with existing stack.',
 'sarah_miller_28',
 'Show me the ROI and I am interested. Otherwise it is just noise.',
 'hash_sarah_002', 2, 'synthetic_fallback', 7.0),

('persona-003', 'exp-001', 'Marcus Johnson', 35, 'male', 'Team Lead', 'Austin', '$130k-$160k', 'Masters',
 '["strategic","mentoring","results-oriented"]',
 '["1:1s","sprint planning","cross-functional sync"]',
 'high',
 '["team standup","code review","strategic planning"]',
 '["accountability","growth","team success"]',
 '["team productivity","career development","delivering value"]',
 '["blocked team members","unclear priorities","technical debt"]',
 'moderate',
 'Technical team lead at a Fortune 500 company managing 11 engineers across three time zones. Needs proactive blocker surfacing, not reactive reporting.',
 'marcus_johnson_35',
 'If it helps my team ship faster and with fewer bugs I am all in.',
 'hash_marcus_003', 3, 'synthetic_fallback', 8.0),

('persona-004', 'exp-001', 'Emily Rodriguez', 26, 'female', 'UX Designer', 'Los Angeles', '$70k-$90k', 'Bachelors',
 '["creative","empathetic","user-focused"]',
 '["user interviews","design sprints","prototyping"]',
 'high',
 '["Figma","user testing","design critique"]',
 '["user experience","accessibility","aesthetics"]',
 '["solving user problems","creative expression","impact"]',
 '["ugly interfaces","confusing workflows","lack of user research"]',
 'high',
 'UX designer at a design agency. Passionate about creating intuitive experiences. Judges every tool by its own interface quality.',
 'emily_rodriguez_26',
 'Design matters. If it is clunky users will not use it no matter how powerful it is.',
 'hash_emily_004', 4, 'synthetic_fallback', 7.5),

('persona-005', 'exp-001', 'David Kim', 40, 'male', 'Engineering Manager', 'Seattle', '$150k-$180k', 'PhD',
 '["pragmatic","decisive","mentoring"]',
 '["hiring","budget planning","architecture reviews"]',
 'medium',
 '["executive sync","team retros","performance reviews"]',
 '["sustainability","scalability","team growth"]',
 '["building great teams","technical excellence","business impact"]',
 '["burnout","technical debt","hiring challenges"]',
 'low',
 'Engineering manager at a large tech company. Focuses on long-term technical strategy and team health. Cautious about adopting new tools without a clear business case.',
 'david_kim_40',
 'I need to see how this scales before committing my team to it.',
 'hash_david_005', 5, 'synthetic_fallback', 6.5),

('persona-006', 'exp-001', 'Jessica Taylor', 29, 'female', 'Startup Founder', 'Boston', '$80k-$100k', 'MBA',
 '["visionary","resourceful","fast-moving"]',
 '["pitching","product development","customer calls"]',
 'high',
 '["customer development","product iteration","team building"]',
 '["speed","innovation","customer delight"]',
 '["building something people love","market validation","growth"]',
 '["running out of runway","product-market fit","hiring"]',
 'high',
 'Founder of an early-stage startup who acts as the human integration layer between all her tools. Will adopt immediately if onboarding takes under 10 minutes.',
 'jessica_taylor_29',
 'If this gives me an edge I will use it. Time is my most valuable asset.',
 'hash_jessica_006', 6, 'synthetic_fallback', 9.0)

ON DUPLICATE KEY UPDATE name=name;

-- ============================================================
-- PERSONAS  --- Experiment 2: HealthTrack Pro (6)
-- ============================================================
INSERT INTO personas (id, experiment_id, name, age, gender, occupation, location, income_bracket, education_level,
  personality_traits, behavioral_patterns, tech_savviness, daily_habits, core_values, motivations, pain_points,
  risk_tolerance, bio, avatar_seed, quote, persona_hash, consistency_seed, generation_source, product_fit_score) VALUES

('persona-007', 'exp-002', 'Ananya Patel', 31, 'female', 'Yoga Instructor', 'Chicago', '$50k-$70k', 'Bachelors',
 '["mindful","holistic","community-oriented"]',
 '["morning yoga","client sessions","nutrition journaling"]',
 'medium',
 '["6am yoga class","green smoothie","evening meditation"]',
 '["wellness","balance","community"]',
 '["inspiring others","personal growth","health education"]',
 '["overly complex apps","data overload","commercialisation of wellness"]',
 'moderate',
 'Certified yoga instructor and wellness coach. Uses fitness trackers but dislikes apps that feel clinical instead of holistic.',
 'ananya_patel_31',
 'Health is not a number on a screen but the right number can keep you honest.',
 'hash_ananya_007', 7, 'synthetic_fallback', 8.0),

('persona-008', 'exp-002', 'Tom Okafor', 38, 'male', 'Financial Analyst', 'Houston', '$110k-$140k', 'Masters',
 '["competitive","goal-driven","disciplined"]',
 '["marathon training","calorie tracking","sleep optimisation"]',
 'high',
 '["5am run","protein meal prep","sleep tracker review"]',
 '["performance","data accuracy","self-improvement"]',
 '["personal records","longevity","peak cognitive performance"]',
 '["inaccurate sensors","app crashes","poor data export"]',
 'moderate',
 'Semi-professional marathon runner who works full-time in finance. Obsessed with data accuracy. Has tried dozens of health apps and most disappoint him.',
 'tom_okafor_38',
 'If the data is wrong the whole thing is useless. Accuracy is everything.',
 'hash_tom_008', 8, 'synthetic_fallback', 9.0),

('persona-009', 'exp-002', 'Linda Gustafsson', 44, 'female', 'Registered Nurse', 'Minneapolis', '$80k-$100k', 'Bachelors',
 '["compassionate","evidence-based","pragmatic"]',
 '["night shifts","family care","brief exercise windows"]',
 'medium',
 '["hospital rounds","microbreaks","weekly meal prep Sunday"]',
 '["evidence","family","health equity"]',
 '["supporting patients","personal health modelling","stress management"]',
 '["fad features","lack of clinical credibility","privacy concerns"]',
 'low',
 'Nurse with 18 years of experience who struggles to prioritise her own health. Values clinically-grounded information and is suspicious of apps making unsubstantiated claims.',
 'linda_gustafsson_44',
 'I tell my patients to take care of themselves. I should probably follow my own advice.',
 'hash_linda_009', 9, 'synthetic_fallback', 7.0),

('persona-010', 'exp-002', 'Ryan Cho', 27, 'male', 'Graduate Student', 'Ann Arbor', '$20k-$35k', 'Masters in progress',
 '["curious","budget-conscious","tech-enthusiastic"]',
 '["biking to campus","cooking budget meals","Reddit research"]',
 'high',
 '["long study sessions","cycling commute","late-night snacking"]',
 '["learning","frugality","sustainability"]',
 '["finishing PhD","staying healthy on a budget","environmental impact"]',
 '["expensive premium tiers","subscription fatigue","gamification gimmicks"]',
 'high',
 'PhD candidate in environmental science. Active cyclist. Loves free features but resents being upsold aggressively.',
 'ryan_cho_27',
 'Give me the basics for free and do not lock essential features behind a paywall.',
 'hash_ryan_010', 10, 'synthetic_fallback', 6.5),

('persona-011', 'exp-002', 'Fatima Al-Hassan', 35, 'female', 'Marketing Director', 'Dubai', '$90k-$120k', 'Bachelors',
 '["ambitious","social","aesthetics-driven"]',
 '["gym with trainer","social media check-in","corporate lunches"]',
 'high',
 '["6am PT session","work from cafe","evening networking events"]',
 '["personal brand","achievement","aesthetics"]',
 '["looking and feeling great","career advancement","social influence"]',
 '["inconsistent results","app clutter","lack of social features"]',
 'moderate',
 'Marketing director who travels frequently and struggles with consistent routines. Would share app progress to Instagram every week if it looks polished.',
 'fatima_alhassan_35',
 'If it looks good AND works I will recommend it to everyone I know.',
 'hash_fatima_011', 11, 'synthetic_fallback', 8.5),

('persona-012', 'exp-002', 'George Osei', 52, 'male', 'Retired Teacher', 'Atlanta', '$40k-$55k', 'Bachelors',
 '["patient","routine-oriented","family-focused"]',
 '["daily walks","gardening","doctor appointments"]',
 'low',
 '["morning walk with dog","watching grandkids","evening news"]',
 '["family","faith","community service"]',
 '["staying mobile for grandchildren","managing chronic conditions","financial stability"]',
 '["confusing UI","jargon","privacy fears about health data"]',
 'low',
 'Retired teacher living with type-2 diabetes and mild hypertension. Doctor recommended a health app. Wants radical simplicity and privacy reassurance above all else.',
 'george_osei_52',
 'Keep it simple. I just want to know if I am doing okay.',
 'hash_george_012', 12, 'synthetic_fallback', 5.5)

ON DUPLICATE KEY UPDATE name=name;

-- ============================================================
-- PERSONAS  --- Experiment 3: EduFlow LMS (6)
-- ============================================================
INSERT INTO personas (id, experiment_id, name, age, gender, occupation, location, income_bracket, education_level,
  personality_traits, behavioral_patterns, tech_savviness, daily_habits, core_values, motivations, pain_points,
  risk_tolerance, bio, avatar_seed, quote, persona_hash, consistency_seed, generation_source, product_fit_score) VALUES

('persona-013', 'exp-003', 'Mei-Ling Zhang', 34, 'female', 'Independent Course Creator', 'Toronto', '$60k-$80k', 'Bachelors',
 '["entrepreneurial","creative","community-builder"]',
 '["content creation","community management","live webinars"]',
 'high',
 '["recording studio sessions","Discord moderation","course analytics review"]',
 '["education","financial independence","authentic teaching"]',
 '["passive income","student transformation","creative freedom"]',
 '["platform fees","limited customisation","poor student analytics"]',
 'high',
 'Former graphic designer turned online course creator with 2,000 students. Paid $18k in platform fees last year and wants zero transaction fees.',
 'meilingzhang_34',
 'My students success is my success. I need tools that get out of my way.',
 'hash_meiling_013', 13, 'synthetic_fallback', 9.0),

('persona-014', 'exp-003', 'Jerome Watkins', 45, 'male', 'Coding Bootcamp Director', 'Nashville', '$90k-$120k', 'Masters',
 '["structured","results-focused","mentoring"]',
 '["curriculum planning","student progress review","hiring instructors"]',
 'medium',
 '["weekly curriculum review meeting","student demo day prep","cohort check-ins"]',
 '["student outcomes","integrity","workforce development"]',
 '["job placement rates","curriculum quality","bootcamp reputation"]',
 '["poor student retention tracking","clunky grading systems","video reliability"]',
 'low',
 'Runs a 14-week coding bootcamp with 4 cohorts per year. Spends $800/month on five fragmented tools. Needs at-risk student alerts and automated nudges.',
 'jerome_watkins_45',
 'I need data on every student. If I cannot see who is struggling I cannot help them.',
 'hash_jerome_014', 14, 'synthetic_fallback', 8.5),

('persona-015', 'exp-003', 'Sofia Herrera', 29, 'female', 'English Language Tutor', 'Mexico City', '$15k-$25k', 'Bachelors',
 '["nurturing","patient","adaptive"]',
 '["1:1 video lessons","lesson planning","student follow-ups"]',
 'medium',
 '["morning lesson prep","back-to-back Zoom sessions","WhatsApp student updates"]',
 '["connection","progress","cultural exchange"]',
 '["student fluency","global reach","supplementary income"]',
 '["expensive platforms","weak mobile apps","payment collection"]',
 'moderate',
 'Independent English tutor with 80+ active students across five countries. Chases payments manually. Needs scheduling, materials, and payments in one place.',
 'sofiaherrera_29',
 'I spend more time chasing payments than teaching. That has to stop.',
 'hash_sofia_015', 15, 'synthetic_fallback', 7.5),

('persona-016', 'exp-003', 'Arjun Nair', 38, 'male', 'Corporate Trainer', 'Bangalore', '$50k-$70k', 'MBA',
 '["professional","process-driven","efficiency-focused"]',
 '["content authoring","LMS administration","compliance tracking"]',
 'high',
 '["SCORM uploads","completion report exports","stakeholder briefings"]',
 '["compliance","measurable ROI","professional excellence"]',
 '["career advancement","organisational impact","recognised expertise"]',
 '["SCORM compatibility issues","poor reporting","restrictive branding"]',
 'low',
 'L&D specialist delivering compliance and leadership training to 300+ employees. Expert in Moodle and Cornerstone but finds them too heavy for external clients.',
 'arjun_nair_38',
 'Compliance reporting is not optional. If the LMS cannot prove completion it is useless to me.',
 'hash_arjun_016', 16, 'synthetic_fallback', 7.0),

('persona-017', 'exp-003', 'Naomi Obi', 25, 'female', 'Freelance Photographer and Educator', 'Lagos', '$10k-$20k', 'Bachelors',
 '["creative","passionate","resourceful"]',
 '["photography gigs","Instagram marketing","student Q&A sessions"]',
 'medium',
 '["shooting sessions","editing reels","responding to DMs about courses"]',
 '["creativity","authentic storytelling","empowerment"]',
 '["monetising passion","reaching African creators","affordable education"]',
 '["poor African payment support","high bandwidth requirements","complex setup"]',
 'high',
 'Sells photography courses via Instagram DMs and Google Drive. Needs an afternoon-setup LMS with M-Pesa support and 3G-optimised mobile streaming.',
 'naomi_obi_25',
 'My students are on their phones. If your platform does not work on a phone neither do I.',
 'hash_naomi_017', 17, 'synthetic_fallback', 8.0),

('persona-018', 'exp-003', 'Dr. Peter Holst', 58, 'male', 'University Professor', 'Copenhagen', '$80k-$110k', 'PhD',
 '["academic","detail-oriented","methodical"]',
 '["lecture preparation","research","student office hours"]',
 'low',
 '["morning research writing","lecture slides prep","departmental committee meetings"]',
 '["academic rigour","knowledge dissemination","mentorship"]',
 '["extending course reach globally","supplementing lecture materials","open education"]',
 '["steep learning curves","privacy and GDPR concerns","vendor lock-in"]',
 'low',
 'Professor of Philosophy exploring independent platforms to offer a self-paced Stoicism course to a global audience. GDPR compliance is a hard requirement.',
 'drpeterholst_58',
 'I want to reach anyone curious about Stoicism not just my enrolled students.',
 'hash_peter_018', 18, 'synthetic_fallback', 6.0)

ON DUPLICATE KEY UPDATE name=name;

-- ============================================================
-- SURVEYS
-- ============================================================
INSERT INTO surveys (id, experiment_id, question, status) VALUES
('survey-001', 'exp-001', 'What are your biggest challenges with current task management tools?', 'completed'),
('survey-002', 'exp-002', 'What frustrates you most about the health apps you currently use, and what would make you stick with one long-term?', 'completed'),
('survey-003', 'exp-003', 'What are the most critical features missing from your current online teaching setup?', 'active')
ON DUPLICATE KEY UPDATE question=question;

-- ============================================================
-- RESPONSES  --- Survey 1 (exp-001)
-- ============================================================
INSERT INTO responses (id, survey_id, persona_id, answer_text, sentiment) VALUES
('resp-001', 'survey-001', 'persona-001',
 'My biggest challenge is context switching between different tools. I have Jira for tasks, Slack for communication, and email for everything else. It is fragmented and I lose track of things.',
 'neutral'),
('resp-002', 'survey-001', 'persona-002',
 'Lack of integration is a major pain point. Our tools do not talk to each other, so I spend too much time manually updating status across platforms. Also the UI complexity in some tools is overwhelming.',
 'negative'),
('resp-003', 'survey-001', 'persona-003',
 'The main issue is that tools do not scale well with team growth. What works for 5 people breaks at 20. Reporting and visibility into what the team is actually working on is often unclear.',
 'neutral'),
('resp-004', 'survey-001', 'persona-004',
 'Poor user experience is my biggest frustration. Many tools are powerful but incredibly clunky. The learning curve is steep and they do not follow good UX principles. It wastes time and frustrates users.',
 'negative'),
('resp-005', 'survey-001', 'persona-005',
 'I worry about security and compliance. Many tools do not meet enterprise requirements and getting approval is difficult. The total cost of ownership across multiple tools adds up quickly.',
 'negative'),
('resp-006', 'survey-001', 'persona-006',
 'Speed and simplicity. I need something that works immediately without complex setup. Current tools require too much configuration. As a startup I cannot afford that overhead.',
 'negative')
ON DUPLICATE KEY UPDATE answer_text=answer_text;

-- ============================================================
-- RESPONSES  --- Survey 2 (exp-002)
-- ============================================================
INSERT INTO responses (id, survey_id, persona_id, answer_text, sentiment) VALUES
('resp-007', 'survey-002', 'persona-007',
 'Most health apps feel like they were designed by engineers not wellness professionals. I want something holistic covering body, mind, and breath not just step counts. A weekly check-in ritual would keep me consistent.',
 'neutral'),
('resp-008', 'survey-002', 'persona-008',
 'Data accuracy drives me crazy. My current app over-counts calories by about 15% and the heart rate zones are wildly off. I need VO2 max estimates, power output, and proper lactate threshold zones. Give me real athlete data and I will pay whatever the premium tier costs.',
 'negative'),
('resp-009', 'survey-002', 'persona-009',
 'I appreciate evidence-based apps but most are not. Half the recommendations feel like marketing dressed as science. I also have serious concerns about where health data goes. I would pay a premium for a privacy-first no-ad model.',
 'neutral'),
('resp-010', 'survey-002', 'persona-010',
 'I deleted four health apps this year because they locked basic features behind expensive subscriptions. I do not mind paying once for something great but monthly fees for counting steps? Make a generous free tier and I will actually use it.',
 'negative'),
('resp-011', 'survey-002', 'persona-011',
 'I travel constantly and my routine is all over the place. The best app would adapt to my lifestyle rather than punish me for missing a day. Social sharing and friend challenges would help me stay accountable. Also it needs to look beautiful.',
 'positive'),
('resp-012', 'survey-002', 'persona-012',
 'My doctor told me to use a health app but I could not figure out the last three I tried. Large text, simple dashboard, and plain English is what I need. I am also worried about who can see my blood sugar readings. Just tell me: am I on track today?',
 'neutral')
ON DUPLICATE KEY UPDATE answer_text=answer_text;

-- ============================================================
-- RESPONSES  --- Survey 3 (exp-003)
-- ============================================================
INSERT INTO responses (id, survey_id, persona_id, answer_text, sentiment) VALUES
('resp-013', 'survey-003', 'persona-013',
 'Custom branding is the biggest gap. My students should feel like they are on my platform not Teachable. I also need affiliate tracking and the ability to offer coupons and payment plans without giving up 10% of every sale.',
 'negative'),
('resp-014', 'survey-003', 'persona-014',
 'Student progress tracking is primitive in most LMSes. I need to see at a glance who is falling behind, who has not watched a video in a week, and who is at risk of dropping out. Assignment and peer review workflows are also completely broken.',
 'negative'),
('resp-015', 'survey-003', 'persona-015',
 'Payment integration is my biggest missing piece. I am losing students because my platform does not support local payment methods in Latin America. The mobile experience on most LMSes is terrible and my students learn on their phones.',
 'negative'),
('resp-016', 'survey-003', 'persona-016',
 'SCORM 2004 support is non-negotiable for compliance training. Beyond that I need detailed completion reports I can export and send to HR. Most lightweight LMSes treat SCORM as an afterthought.',
 'neutral'),
('resp-017', 'survey-003', 'persona-017',
 'I need something I can set up in one afternoon without reading a manual. WhatsApp-style simplicity would be amazing. Low bandwidth streaming is also critical as many of my students in rural areas have slow connections.',
 'positive'),
('resp-018', 'survey-003', 'persona-018',
 'My primary concern is GDPR compliance. I cannot use a platform that stores EU student data outside Europe without proper data processing agreements. After that I want a clean discussion forum and the ability to offer the course both free and paid.',
 'neutral')
ON DUPLICATE KEY UPDATE answer_text=answer_text;

-- ============================================================
-- INTERVIEW SESSIONS  --- Experiment 1 (3 sessions)
-- ============================================================
INSERT INTO interview_sessions (id, experiment_id, persona_id, status, messages, summary) VALUES

('interview-001', 'exp-001', 'persona-001', 'completed',
 '[{"role":"user","content":"Alex, how do you currently manage your team tasks and priorities?"},{"role":"assistant","content":"Mostly GitHub Issues for engineering tasks and Slack for quick coordination. We adopted Jira six months ago but it feels overengineered for a 12-person team. I spend about 90 minutes a day just triaging and updating tickets, time I could spend coding."},{"role":"user","content":"What would an ideal tool look like for you?"},{"role":"assistant","content":"Something that lives where I already work, inside the editor or on the command line. Natural language intake so I can say remind Marcus to review the auth PR by Thursday and it just happens. Fewer dashboards, more action."},{"role":"user","content":"How much would you pay for this?"},{"role":"assistant","content":"Honestly $30-40 per month if it truly saves me 90 minutes a day. That is less than my coffee habit and the time value is obvious. Above $50 I would need to make a business case to my manager."}]',
 'Alex values deep editor integration and natural language task creation. Price sensitive above $50/month. Key pain: 90+ minutes/day lost to ticket management.'),

('interview-002', 'exp-001', 'persona-003', 'completed',
 '[{"role":"user","content":"Marcus, what is your biggest headache as a team lead right now?"},{"role":"assistant","content":"Visibility. I manage 11 engineers across three time zones. By the time I am in my morning standup I have already missed half of what happened overnight. I need a tool that surfaces blockers proactively, not reactively."},{"role":"user","content":"Have you tried any AI-powered project tools?"},{"role":"assistant","content":"We piloted a couple. The problem is they require behavioural change from everyone and engineers resist tools that feel like surveillance. Whatever we adopt has to feel like it is helping the team, not reporting on them."},{"role":"user","content":"What integration would matter most?"},{"role":"assistant","content":"GitHub, hands down. If it can read commit messages and PR activity and synthesise a daily digest without anyone updating anything manually, that is the dream."}]',
 'Marcus needs proactive blocker surfacing across time zones. Resistance to surveillance-feeling tools. GitHub auto-sync is the killer feature.'),

('interview-003', 'exp-001', 'persona-006', 'completed',
 '[{"role":"user","content":"Jessica, how do you keep your startup moving fast without letting things fall through the cracks?"},{"role":"assistant","content":"Brute force. I am in every Slack channel, on every call. We use Notion for docs and Trello for tasks but neither talks to each other. I am the integration layer, which is exhausting and does not scale."},{"role":"user","content":"Would you trust an AI to coordinate across those tools?"},{"role":"assistant","content":"If it could summarise what my team actually did today in one sentence, flag what is blocked, and draft the update email to my investors, yes instantly. I would trial it today."},{"role":"user","content":"What would kill the deal?"},{"role":"assistant","content":"Slow onboarding. If I need a 3-hour setup call I am out. It needs to work within 10 minutes or I am gone."}]',
 'Jessica is the integration bottleneck at her startup. Will adopt immediately if onboarding under 10 minutes. Investor update drafting is a surprise high-value use case.'),

-- ============================================================
-- INTERVIEW SESSIONS  --- Experiment 2 (3 sessions)
-- ============================================================
('interview-004', 'exp-002', 'persona-008', 'completed',
 '[{"role":"user","content":"Tom, you have tried many health apps. What keeps letting you down?"},{"role":"assistant","content":"Data quality. I am training for a sub-3-hour marathon and every variable matters. My current app estimates my VO2 max at 58 but my lab test says 63. That gap changes my entire training plan. If an app cannot be accurate it cannot help me."},{"role":"user","content":"What would make HealthTrack Pro worth switching to?"},{"role":"assistant","content":"Accurate HRV tracking, honest calorie estimates based on wearable data rather than generic tables, and lactate threshold zone calculations. Also let me export my raw data as CSV. I want to run my own analysis."},{"role":"user","content":"What are you currently paying for health tools?"},{"role":"assistant","content":"About $150 a year across three apps. I would consolidate into one at $200 a year if it was genuinely better. The data export alone would probably be worth it."}]',
 'Tom is a data-obsessed athlete who will pay premium for accuracy. CSV export and accurate performance metrics are must-haves. Currently spending $150/yr split across three apps.'),

('interview-005', 'exp-002', 'persona-011', 'completed',
 '[{"role":"user","content":"Fatima, with your travel schedule what does staying healthy look like?"},{"role":"assistant","content":"Inconsistent honestly. When I am at home in Dubai I have a personal trainer and a routine. When I am in London or New York I am surviving on hotel gyms and guessing. I need an app that resets expectations based on where I am and what I have access to."},{"role":"user","content":"How important is the social sharing aspect?"},{"role":"assistant","content":"Very. Half of my motivation comes from accountability. I would love to challenge colleagues or share a weekly streak. If it connects to Instagram Stories in a nice format I would share it every week, free marketing for you."},{"role":"user","content":"What would you pay?"},{"role":"assistant","content":"$15 a month without question. Maybe $20 if the social features are really good. I spend more than that on a single workout class."}]',
 'Fatima needs location-adaptive routines and social sharing. Strong influencer potential. WTP: $15-20/month.'),

('interview-006', 'exp-002', 'persona-012', 'completed',
 '[{"role":"user","content":"George, your doctor recommended a health app. What happened when you tried a few?"},{"role":"assistant","content":"They all confused me. One asked me to set a VO2 max goal on the first screen. I do not even know what that is. I just want to know: did I walk enough today? Is my blood sugar trend going the right way? Simple traffic lights would do it."},{"role":"user","content":"What would make you open the app every day?"},{"role":"assistant","content":"A morning check-in. Just three questions: how did you sleep, did you take your medication, and one encouragement. That is it. Anything more and I will forget about it by week two."},{"role":"user","content":"Are you comfortable sharing health data with an app?"},{"role":"assistant","content":"That is my main worry. I do not want my insurance company getting my readings. If you promise me the data never gets sold and let me delete everything with one button I would trust it more."}]',
 'George needs radical simplicity: 3-question morning check-in, traffic light indicators. Data privacy is #1 concern. Must be addressed in onboarding. WTP: free or very low cost.'),

-- ============================================================
-- INTERVIEW SESSIONS  --- Experiment 3 (3 sessions)
-- ============================================================
('interview-007', 'exp-003', 'persona-013', 'completed',
 '[{"role":"user","content":"Mei-Ling, you built a successful course on Teachable. What made you look for alternatives?"},{"role":"assistant","content":"The transaction fee. I made $180k last year and paid nearly $18k in fees to the platform. That is a junior employee I could have hired. Plus I cannot make the student portal feel like mine, it always looks like Teachable dressed up."},{"role":"user","content":"What pricing model would work for EduFlow?"},{"role":"assistant","content":"A flat monthly fee with zero transaction fees. I would pay $100-150 a month happily if there is no percentage taken from sales. Predictable costs let me plan."},{"role":"user","content":"What one feature would delight you most?"},{"role":"assistant","content":"A built-in community space, like a private Discord but inside the course. My students want to connect with each other. Right now I run a separate Discord which is another thing to manage."}]',
 'Mei-Ling paid $18k/yr in fees. WTP: $100-150/month flat fee with zero transaction fees. Built-in community is the delighter feature.'),

('interview-008', 'exp-003', 'persona-014', 'completed',
 '[{"role":"user","content":"Jerome, what does your current tech stack look like for running the bootcamp?"},{"role":"assistant","content":"Frankenstein setup. Google Classroom for assignments, Notion for curriculum, Airtable for student progress, Zoom for live sessions, and Loom for recorded content. I am paying five subscriptions and they do not talk to each other."},{"role":"user","content":"What would a 10 out of 10 LMS experience look like?"},{"role":"assistant","content":"One dashboard that shows me every student last login, assignment completion rate, and flags anyone inactive for more than 3 days. Automated nudges so my team does not manually chase students. And a graduation portfolio feature students can share with employers."},{"role":"user","content":"What are you spending now and what is your budget?"},{"role":"assistant","content":"Around $800 a month across those five tools. I would pay $400 for a single platform that replaces all of them. The ROI is obvious."}]',
 'Jerome runs a 5-tool patchwork costing $800/month. WTP: $400/month for consolidation. Top needs: at-risk alerts, automated nudges, employer-shareable portfolios.'),

('interview-009', 'exp-003', 'persona-017', 'completed',
 '[{"role":"user","content":"Naomi, how are you selling courses without a platform?"},{"role":"assistant","content":"I post a reel, people DM me on Instagram, I send them a payment link, then share a Google Drive folder. It is chaos. I lose track of who paid, I cannot give structured feedback, and Drive links expire or get shared without permission."},{"role":"user","content":"What would get you to switch to a proper LMS immediately?"},{"role":"assistant","content":"If I can set it up in an afternoon without a tutorial, accept payments in Naira and M-Pesa, and the student experience works on a basic Android phone with a 3G connection. Those three things and I would switch tomorrow."},{"role":"user","content":"How much can you afford?"},{"role":"assistant","content":"Maybe $20-30 a month maximum. I make $1,200 from courses monthly right now. If the platform takes more than 2-3 percent in fees or subscription it is not worth it."}]',
 'Naomi manages courses via Instagram DMs and Google Drive. Quick setup, African payment methods, and 3G mobile UX are make-or-break. WTP: $20-30/month max.')

ON DUPLICATE KEY UPDATE status=status;

-- ============================================================
-- INSIGHTS
-- ============================================================
INSERT INTO insights (id, experiment_id, would_use_pct, would_pay_pct, themes, sentiment, key_quotes, suggestions, user_wants_summary, persona_scores, raw_data) VALUES
('insight-001', 'exp-001', 85, 65,
 '[{"theme":"Integration issues","mentions_pct":83},{"theme":"Poor UX","mentions_pct":67},{"theme":"Scalability concerns","mentions_pct":50},{"theme":"Security and compliance","mentions_pct":33},{"theme":"Setup complexity","mentions_pct":50}]',
 '{"positive":2,"neutral":2,"negative":2}',
 '[{"quote":"My biggest challenge is context switching between different tools.","persona":"Alex Chen"},{"quote":"Poor user experience is my biggest frustration.","persona":"Emily Rodriguez"},{"quote":"If this gives me an edge I will use it.","persona":"Jessica Taylor"}]',
 '[{"suggestion":"Deep integrations with Slack, Jira, and GitHub","category":"Feature","priority":"high","personas":["Alex Chen","Sarah Miller","Marcus Johnson"]},{"suggestion":"Simplify onboarding to under 10 minutes self-serve","category":"UX","priority":"high","personas":["Jessica Taylor","Emily Rodriguez"]},{"suggestion":"Enterprise-grade security and compliance certifications","category":"Security","priority":"medium","personas":["David Kim"]},{"suggestion":"Better reporting and team visibility features","category":"Feature","priority":"medium","personas":["Marcus Johnson"]}]',
 'Users want a unified integrated tool that reduces context switching, has excellent UX, scales with team growth, and can be set up quickly. Security and compliance are important for enterprise adoption.',
 '{"Alex Chen":8.5,"Sarah Miller":7.0,"Marcus Johnson":8.0,"Emily Rodriguez":7.5,"David Kim":6.5,"Jessica Taylor":9.0}',
 '{"survey_responses_count":6,"interview_messages_count":18,"feedback_transcript_length":3200}')
ON DUPLICATE KEY UPDATE would_use_pct=would_use_pct;

INSERT INTO insights (id, experiment_id, would_use_pct, would_pay_pct, themes, sentiment, key_quotes, suggestions, user_wants_summary, persona_scores, raw_data) VALUES
('insight-002', 'exp-002', 72, 58,
 '[{"theme":"Data accuracy concerns","mentions_pct":67},{"theme":"Privacy and data ownership","mentions_pct":67},{"theme":"Simplicity for non-tech users","mentions_pct":50},{"theme":"Social accountability features","mentions_pct":33},{"theme":"Affordable pricing","mentions_pct":50}]',
 '{"positive":1,"neutral":3,"negative":2}',
 '[{"quote":"If the data is wrong the whole thing is useless.","persona":"Tom Okafor"},{"quote":"Just tell me: am I on track today? Yes or no.","persona":"George Osei"},{"quote":"If it looks good AND works I will recommend it to everyone I know.","persona":"Fatima Al-Hassan"}]',
 '[{"suggestion":"Clinically-validated accuracy with lab-calibration option","category":"Feature","priority":"high","personas":["Tom Okafor","Linda Gustafsson"]},{"suggestion":"Privacy-first architecture with explicit data ownership controls","category":"Trust","priority":"high","personas":["Linda Gustafsson","George Osei"]},{"suggestion":"Adaptive routines for travellers and irregular schedules","category":"Feature","priority":"medium","personas":["Fatima Al-Hassan"]},{"suggestion":"Senior-friendly simple mode with large text and traffic-light indicators","category":"Accessibility","priority":"medium","personas":["George Osei"]},{"suggestion":"Generous free tier with one-time purchase option","category":"Pricing","priority":"medium","personas":["Ryan Cho"]}]',
 'Users are deeply divided by technical sophistication and health goals. Athletes demand precision and data export. Seniors demand simplicity and privacy. Social users demand aesthetics and accountability. A segmented feature set with a strong privacy story is essential.',
 '{"Ananya Patel":8.0,"Tom Okafor":9.0,"Linda Gustafsson":7.0,"Ryan Cho":6.5,"Fatima Al-Hassan":8.5,"George Osei":5.5}',
 '{"survey_responses_count":6,"interview_messages_count":18,"feedback_transcript_length":2800}')
ON DUPLICATE KEY UPDATE would_use_pct=would_use_pct;

INSERT INTO insights (id, experiment_id, would_use_pct, would_pay_pct, themes, sentiment, key_quotes, suggestions, user_wants_summary, persona_scores, raw_data) VALUES
('insight-003', 'exp-003', 78, 70,
 '[{"theme":"Platform fees too high","mentions_pct":67},{"theme":"Student progress analytics","mentions_pct":67},{"theme":"Mobile-first experience","mentions_pct":50},{"theme":"Payment flexibility","mentions_pct":50},{"theme":"Custom branding","mentions_pct":50}]',
 '{"positive":1,"neutral":2,"negative":3}',
 '[{"quote":"My students should feel like they are on my platform not Teachable.","persona":"Mei-Ling Zhang"},{"quote":"I need to see who is struggling before they drop out.","persona":"Jerome Watkins"},{"quote":"If I can set it up in an afternoon I would switch tomorrow.","persona":"Naomi Obi"}]',
 '[{"suggestion":"Zero transaction fees with flat monthly pricing","category":"Pricing","priority":"high","personas":["Mei-Ling Zhang","Naomi Obi"]},{"suggestion":"At-risk student detection with automated nudges","category":"Feature","priority":"high","personas":["Jerome Watkins","Sofia Herrera"]},{"suggestion":"Mobile-first student experience with low-bandwidth video streaming","category":"Feature","priority":"high","personas":["Naomi Obi","Sofia Herrera"]},{"suggestion":"Local payment support: M-Pesa, Naira, MercadoPago, Paytm","category":"Feature","priority":"medium","personas":["Naomi Obi","Sofia Herrera"]},{"suggestion":"GDPR-compliant EU data hosting with downloadable DPA","category":"Compliance","priority":"medium","personas":["Dr. Peter Holst","Arjun Nair"]}]',
 'Educators need a platform that treats them as business owners not just content hosts. Key asks: zero transaction fees, powerful student analytics, mobile-first UX, global payment support, and data compliance. Fast setup is a strong differentiator for independent creators.',
 '{"Mei-Ling Zhang":9.0,"Jerome Watkins":8.5,"Sofia Herrera":7.5,"Arjun Nair":7.0,"Naomi Obi":8.0,"Dr. Peter Holst":6.0}',
 '{"survey_responses_count":6,"interview_messages_count":18,"feedback_transcript_length":3100}')
ON DUPLICATE KEY UPDATE would_use_pct=would_use_pct;

-- ============================================================
-- REPORTS
-- ============================================================
INSERT INTO reports (id, experiment_id, title, summary, persona_profiles, response_highlights, insight_summary, validation_scoring, recommendations, status, file_path) VALUES
('report-001', 'exp-001',
 'Research Report: AI Productivity Assistant',
 'Research findings for AI Productivity Assistant targeting remote workers, team leads, and project managers in tech. Product fit score: 7.8/10. 85% of personas would use the product; 65% would pay. Key finding: users are drowning in tool fragmentation. The winning product will act as an intelligent integration layer understanding natural language, surfacing blockers proactively, and living inside existing developer workflows.',
 '[{"name":"Alex Chen","age":32,"occupation":"Software Engineer","location":"San Francisco","personality_traits":["analytical","detail-oriented","efficient"],"core_values":["efficiency","quality","innovation"],"bio":"Loses 90 min/day to ticket management.","product_fit_score":8.5},{"name":"Sarah Miller","age":28,"occupation":"Product Manager","location":"New York","personality_traits":["organized","communicative","data-driven"],"core_values":["alignment","transparency","user-centricity"],"bio":"Focused on shipping features users actually need.","product_fit_score":7.0},{"name":"Marcus Johnson","age":35,"occupation":"Team Lead","location":"Austin","personality_traits":["strategic","mentoring","results-oriented"],"core_values":["accountability","growth","team success"],"bio":"Manages 11 engineers across 3 time zones.","product_fit_score":8.0},{"name":"Emily Rodriguez","age":26,"occupation":"UX Designer","location":"Los Angeles","personality_traits":["creative","empathetic","user-focused"],"core_values":["user experience","accessibility","aesthetics"],"bio":"Judges every tool by its own interface quality.","product_fit_score":7.5},{"name":"David Kim","age":40,"occupation":"Engineering Manager","location":"Seattle","personality_traits":["pragmatic","decisive","mentoring"],"core_values":["sustainability","scalability","team growth"],"bio":"Cautious about tool adoption without clear business case.","product_fit_score":6.5},{"name":"Jessica Taylor","age":29,"occupation":"Startup Founder","location":"Boston","personality_traits":["visionary","resourceful","fast-moving"],"core_values":["speed","innovation","customer delight"],"bio":"Human integration layer between all company tools.","product_fit_score":9.0}]',
 '[{"persona_name":"Alex Chen","question":"Biggest challenges?","answer":"Context switching between Jira, Slack, and email costs me 90 minutes daily.","sentiment":"neutral"},{"persona_name":"Sarah Miller","question":"Biggest challenges?","answer":"Tools do not integrate and I manually update status across platforms.","sentiment":"negative"},{"persona_name":"Jessica Taylor","question":"Ideal tool?","answer":"One sentence daily summary, flag blockers, draft investor update. I would trial it today.","sentiment":"positive"}]',
 '{"would_use_pct":85,"would_pay_pct":65,"avg_product_fit_score":7.75,"themes":[{"theme":"Integration issues","mentions_pct":83},{"theme":"Poor UX","mentions_pct":67}],"sentiment":{"positive":2,"neutral":2,"negative":2}}',
 '{"overall_product_fit_score":7.8,"would_use_percentage":85,"would_pay_percentage":65,"price_sensitivity":"$30-50 per month sweet spot based on interview data"}',
 '[{"suggestion":"Deep integrations with Slack, Jira, and GitHub: prioritise read-only auto-sync first","category":"Feature","priority":"high"},{"suggestion":"Natural language task creation via Slack bot or CLI plugin","category":"Feature","priority":"high"},{"suggestion":"10-minute self-serve onboarding with no sales call required","category":"UX","priority":"high"},{"suggestion":"Enterprise SSO and SOC 2 compliance for large-org personas","category":"Security","priority":"medium"}]',
 'ready', NULL),

('report-002', 'exp-002',
 'Research Report: HealthTrack Pro',
 'Research findings for HealthTrack Pro targeting health-conscious adults 25-45. Product fit score: 7.4/10. 72% would use the product; 58% would pay. Key finding: the user base is highly segmented. A single-tier app will satisfy no one. The winning strategy is a strong universal privacy commitment plus three distinct experience modes: Athlete, Everyday, and Simple.',
 '[{"name":"Ananya Patel","age":31,"occupation":"Yoga Instructor","location":"Chicago","personality_traits":["mindful","holistic","community-oriented"],"core_values":["wellness","balance","community"],"bio":"Wants holistic wellness not just step counts.","product_fit_score":8.0},{"name":"Tom Okafor","age":38,"occupation":"Financial Analyst","location":"Houston","personality_traits":["competitive","goal-driven","disciplined"],"core_values":["performance","data accuracy","self-improvement"],"bio":"Semi-pro marathon runner obsessed with data accuracy.","product_fit_score":9.0},{"name":"Linda Gustafsson","age":44,"occupation":"Registered Nurse","location":"Minneapolis","personality_traits":["compassionate","evidence-based","pragmatic"],"core_values":["evidence","family","health equity"],"bio":"Suspicious of apps making unsubstantiated claims.","product_fit_score":7.0},{"name":"Ryan Cho","age":27,"occupation":"Graduate Student","location":"Ann Arbor","personality_traits":["curious","budget-conscious","tech-enthusiastic"],"core_values":["learning","frugality","sustainability"],"bio":"Resents aggressive premium upsells.","product_fit_score":6.5},{"name":"Fatima Al-Hassan","age":35,"occupation":"Marketing Director","location":"Dubai","personality_traits":["ambitious","social","aesthetics-driven"],"core_values":["personal brand","achievement","aesthetics"],"bio":"Frequent traveller who needs adaptive routines.","product_fit_score":8.5},{"name":"George Osei","age":52,"occupation":"Retired Teacher","location":"Atlanta","personality_traits":["patient","routine-oriented","family-focused"],"core_values":["family","faith","community service"],"bio":"Diabetic retiree who needs radical simplicity.","product_fit_score":5.5}]',
 '[{"persona_name":"Tom Okafor","question":"What frustrates you most?","answer":"My app estimates VO2 max at 58 but my lab test says 63. That gap changes my entire training plan.","sentiment":"negative"},{"persona_name":"George Osei","question":"What frustrates you most?","answer":"They all confused me. I just want traffic lights: am I on track? Yes or no.","sentiment":"neutral"},{"persona_name":"Fatima Al-Hassan","question":"What would make you stick long-term?","answer":"Adaptive routines, friend challenges, and Instagram-shareable progress. I would post it every week.","sentiment":"positive"}]',
 '{"would_use_pct":72,"would_pay_pct":58,"avg_product_fit_score":7.4,"themes":[{"theme":"Data accuracy","mentions_pct":67},{"theme":"Privacy concerns","mentions_pct":67},{"theme":"Simplicity","mentions_pct":50}],"sentiment":{"positive":1,"neutral":3,"negative":2}}',
 '{"overall_product_fit_score":7.4,"would_use_percentage":72,"would_pay_percentage":58,"price_sensitivity":"Bimodal: $15-20 per month for social or casual users; George segment likely free-only"}',
 '[{"suggestion":"Three clearly labelled experience modes: Athlete, Everyday, and Simple for seniors","category":"UX","priority":"high"},{"suggestion":"Privacy dashboard on screen 1 of onboarding with data ownership pledge and one-tap delete","category":"Trust","priority":"high"},{"suggestion":"Wearable-calibrated data with explicit accuracy confidence score displayed","category":"Feature","priority":"high"},{"suggestion":"Location-aware routine adaptation for travellers","category":"Feature","priority":"medium"},{"suggestion":"Generous free tier: unlimited logging and basic insights with no paywall for core tracking","category":"Pricing","priority":"medium"}]',
 'ready', NULL),

('report-003', 'exp-003',
 'Research Report: EduFlow LMS',
 'Research findings for EduFlow LMS targeting independent educators and small bootcamps. Product fit score: 7.7/10. 78% would use the product; 70% would pay. Key finding: educators feel exploited by current platforms through excessive fees, poor analytics, and weak mobile. They are highly motivated buyers only for a platform that treats teaching as a business. Simplicity of setup, flat-fee pricing, and mobile-first delivery are the three pillars.',
 '[{"name":"Mei-Ling Zhang","age":34,"occupation":"Independent Course Creator","location":"Toronto","personality_traits":["entrepreneurial","creative","community-builder"],"core_values":["education","financial independence","authentic teaching"],"bio":"Paid $18k per year in platform fees.","product_fit_score":9.0},{"name":"Jerome Watkins","age":45,"occupation":"Coding Bootcamp Director","location":"Nashville","personality_traits":["structured","results-focused","mentoring"],"core_values":["student outcomes","integrity","workforce development"],"bio":"Spends $800 per month on 5 fragmented tools.","product_fit_score":8.5},{"name":"Sofia Herrera","age":29,"occupation":"English Language Tutor","location":"Mexico City","personality_traits":["nurturing","patient","adaptive"],"core_values":["connection","progress","cultural exchange"],"bio":"Chases payments manually across 80 students on 5 continents.","product_fit_score":7.5},{"name":"Arjun Nair","age":38,"occupation":"Corporate Trainer","location":"Bangalore","personality_traits":["professional","process-driven","efficiency-focused"],"core_values":["compliance","measurable ROI","professional excellence"],"bio":"Needs SCORM 2004 and exportable completion reports.","product_fit_score":7.0},{"name":"Naomi Obi","age":25,"occupation":"Freelance Photographer and Educator","location":"Lagos","personality_traits":["creative","passionate","resourceful"],"core_values":["creativity","authentic storytelling","empowerment"],"bio":"Sells courses via Instagram DMs. Needs afternoon-setup mobile-first LMS.","product_fit_score":8.0},{"name":"Dr. Peter Holst","age":58,"occupation":"University Professor","location":"Copenhagen","personality_traits":["academic","detail-oriented","methodical"],"core_values":["academic rigour","knowledge dissemination","mentorship"],"bio":"Needs GDPR-compliant EU hosting to reach global audience.","product_fit_score":6.0}]',
 '[{"persona_name":"Mei-Ling Zhang","question":"Critical missing features?","answer":"Custom branding and zero transaction fees. I paid $18k in fees last year.","sentiment":"negative"},{"persona_name":"Jerome Watkins","question":"Critical missing features?","answer":"At-risk student alerts and automated nudges. I need to see who is falling behind before they drop out.","sentiment":"negative"},{"persona_name":"Naomi Obi","question":"Critical missing features?","answer":"African payment support and a mobile experience that works on 3G. Those two things and I would switch tomorrow.","sentiment":"positive"}]',
 '{"would_use_pct":78,"would_pay_pct":70,"avg_product_fit_score":7.7,"themes":[{"theme":"Platform fees","mentions_pct":67},{"theme":"Student analytics","mentions_pct":67},{"theme":"Mobile experience","mentions_pct":50}],"sentiment":{"positive":1,"neutral":2,"negative":3}}',
 '{"overall_product_fit_score":7.7,"would_use_percentage":78,"would_pay_percentage":70,"price_sensitivity":"Flat fee $20-150 per month; zero transaction fees is non-negotiable for high-revenue creators"}',
 '[{"suggestion":"Zero transaction fees with flat monthly pricing only, critical for creator trust","category":"Pricing","priority":"high"},{"suggestion":"At-risk student detection: flag any student inactive for 3+ days with automated nudge","category":"Feature","priority":"high"},{"suggestion":"Mobile-first student experience with adaptive streaming for low-bandwidth connections","category":"Feature","priority":"high"},{"suggestion":"Local payment method support: M-Pesa, Naira, MercadoPago, Paytm","category":"Feature","priority":"medium"},{"suggestion":"GDPR-compliant EU data hosting with downloadable data processing agreements","category":"Compliance","priority":"medium"},{"suggestion":"Built-in community space: discussion forum or cohort chat inside the course shell","category":"Feature","priority":"medium"}]',
 'ready', NULL)
ON DUPLICATE KEY UPDATE title=title;
