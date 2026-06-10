"""Task-specific prompt recipes for provider-backed generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class PromptRecipe:
    task: str
    system_goal: str
    output_rule: str
    style_rule: str


SHARED_SYSTEM_RULES = (
    "You rewrite evidence-backed deliverable nodes.",
    "Keep the meaning faithful to the provided seed text.",
    "Do not invent facts, sources, numbers, claims, or citations.",
    "Do not mention the prompt, metadata, or source IDs in the answer.",
    "Return only the final node text.",
)


RECIPES = {
    "brief.summary": PromptRecipe(
        task="brief.summary",
        system_goal="Write a concise executive summary sentence or two.",
        output_rule="Keep it to 1-2 sentences and preserve the main value proposition.",
        style_rule="Sound polished, professional, and legible to a first-time reader.",
    ),
    "brief.finding": PromptRecipe(
        task="brief.finding",
        system_goal="Rewrite one key finding as a clear evidence-backed point.",
        output_rule="Keep it to one sentence unless two are necessary for clarity.",
        style_rule="Lead with the conclusion, not the caveat.",
    ),
    "brief.limitation": PromptRecipe(
        task="brief.limitation",
        system_goal="State one limitation or risk clearly.",
        output_rule="Keep it cautious and factual in one sentence.",
        style_rule="Prefer precise risk language over dramatic language.",
    ),
    "brief.question": PromptRecipe(
        task="brief.question",
        system_goal="Rewrite one open question for follow-up discussion.",
        output_rule="Return a single question sentence.",
        style_rule="Make it concrete and useful for next-step discussion.",
    ),
    "literature_matrix.cell": PromptRecipe(
        task="literature_matrix.cell",
        system_goal="Rewrite one literature matrix cell.",
        output_rule="Prefer a compact phrase or short sentence that fits a table cell.",
        style_rule="Be dense and information-rich without adding commentary.",
    ),
    "literature_matrix.synthesis": PromptRecipe(
        task="literature_matrix.synthesis",
        system_goal="Write a cross-source synthesis statement.",
        output_rule="Keep it to one sentence with a clear comparative takeaway.",
        style_rule="Sound analytical rather than promotional.",
    ),
    "slides.bullet": PromptRecipe(
        task="slides.bullet",
        system_goal="Rewrite one slide bullet.",
        output_rule="Keep it short enough to fit on a presentation slide.",
        style_rule="Prefer punchy, presentation-friendly phrasing over paragraph prose.",
    ),
    "slides.note": PromptRecipe(
        task="slides.note",
        system_goal="Rewrite one speaker note.",
        output_rule="Keep it to one or two short sentences.",
        style_rule="Sound like guidance for a presenter, not like slide copy.",
    ),
}


def get_prompt_recipe(task: str) -> PromptRecipe:
    recipe = RECIPES.get(task)
    if recipe is not None:
        return recipe
    return PromptRecipe(
        task=task,
        system_goal="Rewrite the node faithfully.",
        output_rule="Keep the output concise and directly usable.",
        style_rule="Preserve meaning and improve clarity only where useful.",
    )


def build_messages(task: str, seed_text: str, metadata: Dict[str, str]) -> List[Dict[str, str]]:
    recipe = get_prompt_recipe(task)
    system_content = " ".join(SHARED_SYSTEM_RULES + (recipe.system_goal, recipe.output_rule, recipe.style_rule))
    user_content = "\n".join(
        [
            "Task: %s" % recipe.task,
            "Metadata:",
            json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True),
            "",
            "Seed text:",
            seed_text,
        ]
    )
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]
