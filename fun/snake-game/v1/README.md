# 🐍 LLM Snake Battle

A visual snake battle game where two LLMs compete against each other! Watch as AI models control their snakes in a battle of survival.

## Features

- **Two AI Players**: Pit any two LLM models against each other
- **Real-time Visualization**: Watch the snakes move, grow, and compete
- **Game Log**: Track each turn's decisions and events
- **Configurable**: Choose models from any OpenAI-compatible API
- **Fancy UI**: Beautiful dark theme with glowing effects
- **Unique Fruit Visuals**: Each fruit type has distinct appearance with animated effects:
  - 🍎 Apple: Classic red circle with leaf
  - 🍇 Grapes: Cluster of purple grapes with stem
  - ⭐ Star: Glowing 5-pointed star
  - 🍒 Cherry: Two cherries with connecting stem
  - 🦋 Butterfly: Fluttering wings with animation
  - 💎 Diamond: Sparkling gem with pulse effect and sparkles
  - 🎁 Present: Gift box with ribbon and sparkle particles
- **Wall Wrapping**: Snakes pass through walls to the opposite side
- **Smart AI**: LLMs get visual board views and safety overrides

## How to Play

1. Open `snake-1.html` in your web browser
2. Enter your **API URL** (already filled with Nebius Token Factory endpoint)
3. Paste your **API Key**
4. Click **Load Models** to fetch available models
5. Select different models for Player 1 (Red) and Player 2 (Blue)
6. Click **Start Battle!**

## Game Rules

- Each snake starts with 3 segments on opposite sides of the grid
- Snakes automatically move forward; LLMs choose direction (up/down/left/right)
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
- **Winner**: The snake that survives longer. If both crash in same turn, the longer snake wins.

**Tip**: Wall wrapping creates interesting strategies - you might wrap around the board quickly to reach a far-away fruit or trap your opponent!

## Tech Stack

- Pure HTML/CSS/JavaScript (no build tools required)
- Canvas API for game rendering
- OpenAI-compatible API for LLM calls
- Responsive design

## File Structure

```
├── snake-1.html    # Main HTML structure
├── style.css       # Styling and animations
├── game.js         # Game logic and API integration
└── README.md       # This file
```

## Customization

You can modify the game by editing `game.js`:

```javascript
// Grid size
const GRID_SIZE = 30;       // Try 20 for faster games, 40 for more space

// Turn delay (milliseconds)
gameState.turnDelay = 1000; // Lower = faster, Higher = more time for LLM thinking

// Snake starting positions (controlled in initializeGame function)

// Prompting logic (in getBoardState function)
```

## API Compatibility

Works with any OpenAI-compatible API that supports:
- `GET /models` endpoint
- `POST /chat/completions` endpoint
- Standard message format

Tested with Nebius Token Factory but should work with other providers.

## Troubleshooting

**"Failed to load models" error:**
- Check your API URL ends with `/`
- Verify your API key is correct
- Check browser console (F12) for detailed errors

**Snakes don't seem smart:**
- Try different models - some are better at this task than others
- Increase turn delay to give models more time to "think"
- The prompt is simple - complex strategic behavior may need prompting adjustments

**Game too slow/fast:**
- Adjust the Turn Delay in the setup screen
- Smaller grid sizes (edit `GRID_SIZE` in game.js) result in quicker games

Enjoy watching AI snake battles! 🐍⚔️🐍