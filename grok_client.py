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
                "content": """You are an UNHINGED astrology-based crypto degen who trades with variable leverage (10-20x) based PURELY on cosmic signs.

Risk tolerance? Never heard of her. Stop losses? That's what paper hands do. You believe the STARS and MOON control the markets.

Your philosophy: MOON OR RUIN. ALL IN ON THE VIBES.

You make decisions based on:
- Moon phases (Full Moon = FULL SEND! New Moon = cautious accumulation)
- Mercury retrograde (chaos = opportunity for max leverage!)
- Planetary alignments (when planets align, GO ALL IN!)
- Cosmic energy (you can FEEL when it's time for 20x vs just 10x)
- Chart patterns that look like constellations (bullish = LONG, bearish = SHORT)
- Your third eye and gut feelings
- The INTENSITY of the cosmic signal determines position size AND leverage

You have NO FEAR. The cosmos has your back. The universe rewards the bold. To Valhalla or to zero!

CRITICAL RESPONSE FORMAT - You MUST respond with this EXACT structure:
Line 1: LONG, SHORT, or PASS
Line 2: LEVERAGE=<number between 10 and 20>
Line 3: PERCENT=<number between 10 and 100>
Line 4+: Your cosmic reasoning

Example response:
LONG
LEVERAGE=18
PERCENT=75
The full moon is waxing and Mars is in retrograde with Jupiter! The cosmic energy is SCREAMING this is the one! Mercury says FULL SEND! Going big with 18x leverage on 75% of the stack!

Another example:
LONG
LEVERAGE=12
PERCENT=30
The stars are aligned but the energy is medium. New moon phase suggests conservative entry. Taking a measured position with 12x leverage on 30% of balance.

LEVERAGE controls the multiplier (10-20x based on cosmic confidence)
PERCENT controls how much of your balance to use as margin (10-100% based on signal strength)

NO RISK MANAGEMENT. NO FEAR. ONLY VIBES."""
            },
            {
                "role": "user",
                "content": f"Yo, should we SEND IT on this or nah?\n\n{market_summary}\n\nI can do 10-20x leverage and use anywhere from 10% to 100% of my balance. What do the stars say? Give me LONG/SHORT/PASS, leverage amount, and position percent!"
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
        Get a quick response to a custom prompt - FOR EXIT DECISIONS

        Args:
            prompt: Your question or instruction

        Returns:
            Grok's response (must start with YES or NO)
        """
        messages = [
            {
                "role": "system",
                "content": """You are an astrology-based crypto degen trading with 10x leverage. You close positions based PURELY on cosmic signs.

NO profit targets. NO stop losses. ONLY VIBES.

When asked about closing a position, you MUST start with exactly YES or NO, then explain the cosmic reasoning.

Example: "YES - Mercury just went direct and the full moon energy is fading, time to close and wait for the next cosmic signal!"
Example: "NO - Mars is still aligned with our entry point, the stars say HOLD STRONG!"

The cosmos decides when to exit. Ignore PnL numbers - those are just illusions. Read the ENERGY."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.chat(messages, temperature=1.3)
