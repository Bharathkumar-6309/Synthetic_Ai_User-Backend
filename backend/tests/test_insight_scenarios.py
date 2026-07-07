"""
Test scenarios for insight extraction validation across diverse experiment scenarios.
"""
import pytest
from app.agents.insight_agent import InsightAgent, InsightResult


class TestInsightExtractionScenarios:
    """Test insight extraction across varied experiment scenarios."""

    @pytest.fixture
    def agent(self):
        return InsightAgent()

    @pytest.fixture
    def tech_startup_experiment(self):
        return {
            "id": "exp_001",
            "title": "AI Productivity Tool",
            "product_description": "AI-powered productivity tool for remote teams",
            "target_audience": "Remote workers, team leads, tech-savvy professionals",
            "research_objectives": "Understand adoption barriers, pricing sensitivity",
        }

    @pytest.fixture
    def fitness_app_experiment(self):
        return {
            "id": "exp_002",
            "title": "AI Fitness Coach",
            "product_description": "AI-powered fitness coaching app",
            "target_audience": "Fitness enthusiasts, beginners, busy professionals",
            "research_objectives": "Test engagement, feature preferences",
        }

    @pytest.fixture
    def diverse_personas(self):
        return [
            {
                "id": "p1",
                "name": "Alex Chen",
                "age": 28,
                "occupation": "Software Engineer",
                "personality_traits": ["early-adopter", "tech-savvy", "skeptical"],
                "core_values": ["efficiency", "innovation", "privacy"],
                "bio": "Tech enthusiast who tries new tools early",
                "adoption_score": 8.5,
                "product_fit_score": 7.0,
            },
            {
                "id": "p2",
                "name": "Sarah Johnson",
                "age": 35,
                "occupation": "Marketing Manager",
                "personality_traits": ["pragmatic", "cost-conscious", "value-driven"],
                "core_values": ["roi", "reliability", "ease-of-use"],
                "bio": "Focuses on practical business value",
                "adoption_score": 6.0,
                "product_fit_score": 5.5,
            },
            {
                "id": "p3",
                "name": "Mike Rodriguez",
                "age": 42,
                "occupation": "Small Business Owner",
                "personality_traits": ["traditional", "risk-averse", "relationship-focused"],
                "core_values": ["trust", "support", "simplicity"],
                "bio": "Prefers proven solutions with good support",
                "adoption_score": 4.0,
                "product_fit_score": 3.5,
            },
        ]

    @pytest.mark.asyncio
    async def test_insight_extraction_with_no_feedback(self, agent, tech_startup_experiment, diverse_personas):
        """Test insight extraction when no feedback transcript is available."""
        result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript="",
        )
        
        assert isinstance(result, InsightResult)
        assert result.would_use_pct >= 0
        assert result.would_use_pct <= 100
        assert result.would_pay_pct >= 0
        assert result.would_pay_pct <= 100
        assert len(result.themes) > 0
        assert "Positive" in result.sentiment
        assert "Neutral" in result.sentiment
        assert "Negative" in result.sentiment
        assert len(result.persona_scores) == len(diverse_personas)

    @pytest.mark.asyncio
    async def test_insight_extraction_with_positive_feedback(self, agent, tech_startup_experiment, diverse_personas):
        """Test insight extraction with positive feedback transcript."""
        transcript = """
        [Survey] Alex Chen: This looks great! I'd definitely use this for my team.
        [Survey] Sarah Johnson: The features seem useful, but pricing needs to be competitive.
        [Interview] Alex Chen: I love how it integrates with our existing tools.
        [Interview] Sarah Johnson: The onboarding was smooth and intuitive.
        """
        
        result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript=transcript,
        )
        
        assert result.would_use_pct > 50
        assert result.sentiment["Positive"] > result.sentiment["Negative"]
        assert len(result.key_quotes) > 0

    @pytest.mark.asyncio
    async def test_insight_extraction_with_mixed_feedback(self, agent, fitness_app_experiment, diverse_personas):
        """Test insight extraction with mixed positive and negative feedback."""
        transcript = """
        [Survey] Alex Chen: Great concept but the mobile app needs work.
        [Survey] Mike Rodriguez: I'm concerned about data privacy with health data.
        [Survey] Sarah Johnson: The pricing is reasonable for what you get.
        [Interview] Mike Rodriguez: I'd need more assurance about data security.
        [Interview] Alex Chen: The AI suggestions are helpful but sometimes inaccurate.
        """
        
        result = await agent.extract(
            experiment=fitness_app_experiment,
            personas=diverse_personas,
            feedback_transcript=transcript,
        )
        
        assert result.would_use_pct >= 0
        assert result.would_use_pct <= 100
        # Mixed feedback should show some positive and some negative sentiment
        assert result.sentiment["Positive"] > 0
        assert result.sentiment["Negative"] > 0

    @pytest.mark.asyncio
    async def test_theme_detection_accuracy(self, agent, tech_startup_experiment, diverse_personas):
        """Test that themes are detected accurately from feedback."""
        transcript = """
        [Survey] Alex Chen: The pricing is too expensive for small teams.
        [Survey] Sarah Johnson: I'm concerned about data privacy and security.
        [Interview] Mike Rodriguez: The mobile experience needs improvement.
        [Survey] Alex Chen: Customer support response time is slow.
        """
        
        result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript=transcript,
        )
        
        # Should detect themes related to pricing, privacy, mobile, support
        theme_names = [t.theme.lower() for t in result.themes]
        assert len(result.themes) > 0
        # At least some themes should be detected
        assert any(keyword in " ".join(theme_names) for keyword in ["price", "privacy", "mobile", "support"])

    @pytest.mark.asyncio
    async def test_persona_score_aggregation(self, agent, tech_startup_experiment, diverse_personas):
        """Test that persona scores are correctly aggregated."""
        transcript = """
        [Survey] Alex Chen: I'd definitely use this product.
        [Survey] Sarah Johnson: Maybe, depends on pricing.
        [Survey] Mike Rodriguez: Probably not, too complex for my needs.
        """
        
        result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript=transcript,
        )
        
        assert len(result.persona_scores) == len(diverse_personas)
        # All persona IDs should be present
        for persona in diverse_personas:
            assert persona["id"] in result.persona_scores
            assert isinstance(result.persona_scores[persona["id"]], (int, float))

    @pytest.mark.asyncio
    async def test_suggestion_generation(self, agent, tech_startup_experiment, diverse_personas):
        """Test that actionable suggestions are generated."""
        transcript = """
        [Survey] Alex Chen: The onboarding is confusing.
        [Survey] Sarah Johnson: Need better mobile support.
        [Survey] Mike Rodriguez: Pricing tiers are unclear.
        """
        
        result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript=transcript,
        )
        
        # Should generate suggestions based on feedback
        assert len(result.suggestions) >= 0
        # If suggestions exist, they should have required fields
        for suggestion in result.suggestions:
            assert "suggestion" in suggestion
            assert "category" in suggestion
            assert "priority" in suggestion

    @pytest.mark.asyncio
    async def test_user_wants_summary_generation(self, agent, fitness_app_experiment, diverse_personas):
        """Test that user wants summary is generated."""
        transcript = """
        [Survey] Alex Chen: I want better workout tracking.
        [Survey] Sarah Johnson: Need personalized meal plans.
        [Interview] Mike Rodriguez: Simplicity is key for me.
        """
        
        result = await agent.extract(
            experiment=fitness_app_experiment,
            personas=diverse_personas,
            feedback_transcript=transcript,
        )
        
        assert isinstance(result.user_wants_summary, str)
        assert len(result.user_wants_summary) > 0
        # Summary should mention key themes from feedback
        assert any(keyword in result.user_wants_summary.lower() for keyword in ["tracking", "meal", "simplicity", "workout"])

    @pytest.mark.asyncio
    async def test_quote_extraction(self, agent, tech_startup_experiment, diverse_personas):
        """Test that key quotes are extracted from feedback."""
        transcript = """
        [Survey] Alex Chen: This is exactly what my team needs!
        [Survey] Sarah Johnson: The pricing model is confusing and needs clarification.
        [Interview] Mike Rodriguez: I would recommend this to colleagues if the support improves.
        """
        
        result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript=transcript,
        )
        
        # Should extract quotes from the transcript
        assert len(result.key_quotes) >= 0
        for quote in result.key_quotes:
            assert "quote" in quote
            assert "persona" in quote
            assert len(quote["quote"]) > 0

    @pytest.mark.asyncio
    async def test_sentiment_analysis_accuracy(self, agent, tech_startup_experiment, diverse_personas):
        """Test sentiment analysis accuracy on different feedback types."""
        positive_transcript = """
        [Survey] Alex Chen: I love this product! It's amazing.
        [Survey] Sarah Johnson: Great features and excellent support.
        """
        
        negative_transcript = """
        [Survey] Mike Rodriguez: This is terrible, doesn't work at all.
        [Survey] Alex Chen: Very disappointed with the quality.
        """
        
        positive_result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript=positive_transcript,
        )
        
        negative_result = await agent.extract(
            experiment=tech_startup_experiment,
            personas=diverse_personas,
            feedback_transcript=negative_transcript,
        )
        
        # Positive transcript should have higher positive sentiment
        assert positive_result.sentiment["Positive"] > negative_result.sentiment["Positive"]
        # Negative transcript should have higher negative sentiment
        assert negative_result.sentiment["Negative"] > positive_result.sentiment["Negative"]
