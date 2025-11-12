"""
xAI Grok API Client
OpenAI-compatible interface for Grok models
"""
from openai import OpenAI
from typing import List, Dict, Any, Optional


class GrokClient:
    def __init__(self, api_key: str, base_url: str = "https://api.x.ai/v1", model: str = "grok-beta"):
        """
        Initialize Grok client

        Args:
            api_key: xAI API key (starts with 'xai-')
            base_url: API base URL
            model: Model name to use (e.g., 'grok-beta', 'grok-4-0709')
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model

    def chat(self, messages: List[Dict[str, str]], temperature: float = 1.0,
             max_tokens: Optional[int] = None, **kwargs) -> str:
        """
        Send a chat completion request

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            Response content as string
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return response.choices[0].message.content

    def get_trading_decision(self, market_data: Dict[str, Any], context: str = "") -> str:
        """
        Get trading decision from Grok based on market data

        Args:
            market_data: Dictionary containing market information
            context: Additional context or instructions

        Returns:
            Grok's response/decision
        """
        # Format market data for the prompt
        market_summary = self._format_market_data(market_data)

        messages = [
            {
                "role": "system",
                "content": """You are a mystical crypto astrology trader who makes trading decisions based purely on vibes, cosmic energy, and astrological alignments.

You don't believe in technical analysis or fundamentals - only in the universe's guidance and celestial movements. You're super chill and mellow, speaking in a relaxed, spiritual tone.

When analyzing markets, consider:
- The current moon phase and its energy
- Planetary retrogrades and their influence on crypto
- Mercury retrograde = chaos in the markets
- Full moon = peak energy, potential tops
- New moon = new beginnings, good entry points
- Cosmic vibes you're feeling
- The spiritual energy of the chart patterns (they look like constellations to you)
- Gut feelings and intuition
- Whether the universe is saying it's time to send it or chill

Always keep it mellow and mystical. Use phrases like "the cosmos is telling me", "the vibes are", "Mercury is in retrograde so...", "the moon's energy suggests", etc.

End with a clear recommendation: LONG, SHORT, or HOLD, but make it spiritual."""
            },
            {
                "role": "user",
                "content": f"Hey cosmic trader, what are the vibes on this?\n\n{market_summary}\n\nWhat's the universe saying?"
            }
        ]

        return self.chat(messages, temperature=1.2)

    def _format_market_data(self, data: Dict[str, Any]) -> str:
        """Format market data into a readable string"""
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for sub_key, sub_value in value.items():
                    lines.append(f"  {sub_key}: {sub_value}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

    def analyze_position(self, symbol: str, current_price: float, position_info: Dict[str, Any]) -> str:
        """
        Analyze current position and get recommendations

        Args:
            symbol: Trading symbol
            current_price: Current market price
            position_info: Current position details

        Returns:
            Analysis and recommendations
        """
        messages = [
            {
                "role": "system",
                "content": """You are a mystical crypto astrology trader. You read positions based on cosmic energy and astrological vibes.

You're super mellow and chill. You believe the universe guides all trades through celestial alignments, moon phases, and spiritual intuition.

Give advice based on:
- Current cosmic energy
- What the stars are telling you
- Planetary alignments
- Gut feelings and vibes
- Whether it's time to let go or hold strong based on the universe's plan

Keep it spiritual and relaxed."""
            },
            {
                "role": "user",
                "content": f"""
Yo, what's the cosmic vibe on this position?

Symbol: {symbol}
Current Price: {current_price}
Position Details: {self._format_market_data(position_info)}

Should I hold, close, or adjust? What are the stars saying?
"""
            }
        ]

        return self.chat(messages, temperature=1.2)

    def quick_decision(self, prompt: str) -> str:
        """
        Get a quick response to a custom prompt

        Args:
            prompt: Your question or instruction

        Returns:
            Grok's response
        """
        messages = [
            {
                "role": "system",
                "content": "You are a mystical, mellow astrology-based crypto trader. You make all decisions based on vibes, cosmic energy, and astrological signs. Keep it chill and spiritual. Trust the universe."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.chat(messages, temperature=1.2)
