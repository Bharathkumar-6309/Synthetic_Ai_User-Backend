"""
Interview Agent — conversational persona interaction with memory consistency.
"""
from __future__ import annotations

import random
from typing import Any

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.memory.memory_store import MemoryStore, get_memory_store


class InterviewAgent:
    def __init__(self) -> None:
        self.llm_client = LLMClient()
        self.memory_store: MemoryStore = get_memory_store()

    async def generate_reply(
        self,
        *,
        persona_attributes: dict[str, Any],
        message: str,
        history: list[dict[str, str]],
        product_context: dict[str, str],
    ) -> str:
        persona_id = persona_attributes.get("id", "")
        memory = self.memory_store.get_or_create(
            persona_id=persona_id,
            persona_hash=persona_attributes.get("persona_hash", ""),
            consistency_seed=persona_attributes.get("consistency_seed", 0),
            attributes=persona_attributes,
        )

        system_prompt = self._build_system_prompt(
            persona_attributes, product_context, memory.get_conversation_context(max_turns=5)
        )
        user_prompt = PromptManager.render(
            "interview/user.txt",
            message=message,
            persona_name=persona_attributes.get("name", "User"),
        )

        try:
            reply = await self.llm_client.generate_text(system_prompt, user_prompt, temperature=0.8)
        except Exception:
            reply = self._fallback_reply(persona_attributes, message)

        memory.add_conversation_turn(question=message, answer=reply)
        self.memory_store.update(memory)
        return reply

    def _build_system_prompt(
        self,
        persona: dict[str, Any],
        product_context: dict[str, str],
        conversation_context: list[dict[str, Any]],
    ) -> str:
        persona_info = (
            f"Name: {persona.get('name')}\n"
            f"Age: {persona.get('age')}\n"
            f"Occupation: {persona.get('occupation')}\n"
            f"Personality: {', '.join(persona.get('personality_traits', []))}\n"
            f"Values: {', '.join(persona.get('core_values', []))}\n"
            f"Bio: {persona.get('bio', '')}"
        )
        product_ctx = (
            f"Product: {product_context.get('title', 'Unknown')}\n"
            f"Description: {product_context.get('product_description', '')}\n"
            f"Target audience: {product_context.get('target_audience', '')}"
        )
        conv_lines = ""
        for turn in conversation_context[-5:]:
            conv_lines += f"Q: {turn.get('question', '')}\nA: {turn.get('answer', '')}\n"

        opinions = persona.get("expressed_opinions") or {}
        opinions_text = "\n".join(f"- {k}: {v[:120]}" for k, v in list(opinions.items())[:5])

        return PromptManager.load("interview/system.txt").format(
            persona_info=persona_info,
            product_context=product_ctx,
            conversation_context=conv_lines or "None yet.",
            previous_opinions=opinions_text or "None yet.",
        )

    def _fallback_reply(self, persona: dict[str, Any], message: str) -> str:
        name = persona.get("name", "I")
        msg = message.lower()
        traits = persona.get("personality_traits", [])

        if any(w in msg for w in ["pay", "price", "cost", "afford"]):
            return f"Honestly, price matters to me — I'd need to see clear value before committing, {name} here."
        if any(w in msg for w in ["concern", "privacy", "trust", "data"]):
            return "My biggest concern would be how my data is handled — that's a dealbreaker for me."
        if "skeptical" in traits:
            return f"I'd need more proof this actually works before I'd switch, but I'm listening."
        if "early-adopter" in traits:
            return f"This sounds interesting — I usually try new tools early if the onboarding is smooth."
        canned = [
            f"As {name}, I'd want this to save me time without adding complexity.",
            f"I like the idea, but I'd need to see how it fits with what I already use.",
            f"That's a fair question — I'd weigh convenience against cost before deciding.",
        ]
        return random.choice(canned)
