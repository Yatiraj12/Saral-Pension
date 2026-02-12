from typing import Dict


def personalize_response(
    response: str,
    user_profile: Dict | None = None
) -> str:
    if not user_profile:
        return response

    tone = user_profile.get("tone")

    if tone == "formal":
        return response

    if tone == "simple":
        return f"{response}\n\nThis explanation is kept simple for easy understanding."

    return response
