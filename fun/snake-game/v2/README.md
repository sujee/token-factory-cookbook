# 🐍 LLM Snake Battle

A visual snake battle game where two LLMs compete against each other! Watch as AI models control their snakes in a battle of survival.

**Key feature:** each snake moves **independently and asynchronously** — the moment its model responds — so faster models move more often. Game speed is driven by model latency, not a fixed turn delay.

## Features

- **Two AI Players**: Pit any two LLM models against each other (searchable dropdowns)
- **Independent Movement**: Each snake moves as soon as its LLM responds; faster models move more frequently
- **Real-time Visualization**: Watch the snakes move, grow, and compete on a 30×30 canvas
- **Game Log**: Per-move event tracking with color-coded API latency (teal/yellow/red) and smart auto-scroll
- **Latency Graphs**: Interactive per-player time-series graph (hover for exact move + latency) with Min/Median/P90/Max stats
- **Configurable**: Choose models from any OpenAI-compatible API
- **Loop Mode**: Auto-restart with a 5-second countdown after each game ends (on by default)
- **Collision Avoidance Toggle**: Enable/disable LLM safe-move hints and automatic override (on by default)
- **Visibility Radius**: Adjustable snake vision (1–30 cells, default 5; 30 = full grid)
- **Debug Mode**: Console logging with masked auth headers and timestamped request/response correlation
- **Model Benchmarking**: Run a speed test on all loaded models and sort results by name or speed
- **Fancy UI**: Dark theme with glowing effects and glass panels
- **Unique Fruit Visuals**: Each fruit type has distinct appearance with animated effects:
  - 🍎 Apple: Classic red circle with leaf
  - 🍇 Grapes: Cluster of purple grapes with stem
  - ⭐ Star: Glowing 5-pointed star
  - 🍒 Cherry: Two cherries with connecting stem
  - 🦋 Butterfly: Fluttering wings with animation
  - 💎 Diamond: Sparkling gem with pulse effect and sparkles
  - 🎁 Present: Gift box with ribbon and sparkle particles
- **Wall Wrapping**: Snakes pass through walls to the opposite side
- **Smart AI**: LLMs get ASCII board views and collision-avoidance safety overrides
- **Robust API Layer**: 15s per-request timeout with retries (2s backoff; exponential backoff on HTTP 429); adaptive `max_tokens`; automatic stripping of `<thinking>` tags; forfeit after 3 consecutive failures

## How to Play

1. Open `snake.html` in your web browser
2. Enter your **API URL** (already filled with Nebius Token Factory endpoint)
3. Paste your **API Key**
4. Click **Load Models** to fetch available models
5. Select different models for Player 1 (Red) and Player 2 (Blue) via the searchable dropdowns
6. (Optional) Adjust **Options** — Visibility Radius, Collision Avoidance, Debug Mode
7. Click **Start** to begin the battle

Controls in the left pane: **Start**, **Pause** ⏸️, **Restart** 🔄, and a **Loop** toggle. The **🔧 Extra** section has the **Speed Test** benchmark and sort buttons.

## Game Rules

- Each snake starts with 3 segments on opposite sides of the grid
- Snakes move **independently** — each moves the moment its LLM responds (no shared turns)
- LLMs choose direction (up/down/left/right); a snake cannot reverse direction
- **15-second timeout**: if a model doesn't respond within 15s, it counts as an API failure and retries after 2s
- **Wall Wrapping**: Going through any wall teleports you to the opposite side! (Left ↔ Right, Top ↔ Bottom)
- Walls are SAFE - only snake collisions cause death
- **Multiple Fruits** appear on the board (3 at a time by default) - eating them makes the snake grow
- **Different Fruit Types** with varying growth values and unique visuals:
  - 🍎 Apple (+1) - 40% spawn rate - Simple red circle with green leaf
  - ⭐ Star (+3) - 25% spawn rate - Golden 5-pointed star with glow
  - 🍇 Grapes (+2) - 15% spawn rate - Purple grape cluster with stem
  - 🍒 Cherry (+2) - 10% spawn rate - Two red cherries with connecting stem
  - 🦋 Butterfly (+3) - 6% spawn rate - **Animated fluttering teal wings**
  - 💎 Diamond (+4) - 3% spawn rate - RARE! **Sparkling cyan gem with pulse effect and twinkle**
  - 🎁 Present (+5) - 1% spawn rate - RARE! **Orange gift box with ribbon and sparkle particles**
- **Collision kills**:
  - Hitting your own body
  - Hitting the enemy snake
  - Walls are SAFE (you wrap through!)
- **Head-on collision**: Both snakes crash simultaneously
- **Winner**: The snake that survives longer. If both crash in the same turn, the longer snake wins (draw if equal length).

**Tip**: Wall wrapping creates interesting strategies - you might wrap around the board quickly to reach a far-away fruit or trap your opponent!

## Tech Stack

- Pure HTML/CSS/JavaScript (no build tools required)
- Canvas API for game rendering
- OpenAI-compatible API for LLM calls
- Responsive design (stacks vertically on narrow screens)

## File Structure

```
├── snake.html      # Main HTML structure
├── style.css       # Styling and animations
├── game.js         # Game logic, rendering, and API integration
├── benchmark.js    # Model performance testing system
└── README.md       # This file
```

## Customization

You can modify the game by editing `game.js`:

```javascript
const GRID_SIZE = 30;                 // Board dimensions (30×30). Try 20 for faster games, 40 for more space
const NUM_FRUITS = 3;                 // Fruits on the board at once
const LLM_TIMEOUT_MS = 15000;         // Per-request LLM timeout (15s)
const API_RETRY_DELAY_MS = 2000;      // Retry delay after a timeout/error
const MAX_TOKENS_CASCADE = [10, 100, 1000, null]; // Adaptive token limits per player
let   VIEW_RADIUS = 5;                // Default snake vision radius (1–30, adjustable from UI)
let   collisionAvoidanceEnabled = true; // LLM hints + auto safe-move override

// Snake starting positions (controlled in initializeGame)
// LLM prompting logic (in getBoardState)
```

> **Note:** There is no fixed "turn delay" — snakes move at the natural speed of their model's responses. If you want to add artificial pacing, you would add a delay inside `moveSnakeWithLLM` before it recurses.

## API Compatibility

Works with any OpenAI-compatible API that supports:
- `GET /models` endpoint (verbose metadata is tried first for modality filtering, with plain fallback)
- `POST /chat/completions` endpoint
- Standard message format

Tested with Nebius Token Factory but should work with others (OpenAI, compatible proxies, Ollama, LM Studio). Models are filtered to text-only (audio/image/vision/speech models are excluded).

## Troubleshooting

**"Failed to load models" error:**
- Check your API URL ends with `/`
- Verify your API key is correct
- Check browser console (F12) for detailed errors
- Some APIs require CORS to be configured to work from the browser

**Snakes don't seem smart:**
- Try different models - some are better at this task than others
- Models get the full 15s timeout to respond; slower models simply move less often
- Keep Collision Avoidance on for safer gameplay, or turn it off to see raw LLM decisions
- The prompt is intentionally simple - complex strategic behavior may need prompting adjustments

**Game too slow/fast:**
- Game speed is determined by model response times — faster models move more often
- Try a faster model for comparison (the move counters and latency graph make speed differences visible)
- Smaller grid sizes (edit `GRID_SIZE` in game.js) result in quicker games

**One snake barely moves:**
- That model is slow to respond — it will move less frequently (intended behavior)
- Check the latency graph/stats for that player
- After 3 consecutive API failures a model forfeits the round

Enjoy watching AI snake battles! 🐍⚔️🐍
