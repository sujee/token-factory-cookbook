# Snake Battle - Game Specification

## Overview

A visual competitive snake battle game where two Large Language Models (LLMs) control separate snakes and compete for survival and growth by collecting fruits.

**Purpose**: Demonstrate AI decision-making in a visual, real-time game environment using OpenAI-compatible APIs.

**Tech Stack**: Pure HTML/CSS/JavaScript (no build tools required)

**Key Feature**: **Independent Snake Movement** - Each snake moves asynchronously based on its model's response time, creating speed differences based on LLM performance.

---

## File Structure

```
snake-battle/
├── snake-1.html         # Main HTML structure
├── style.css            # All styling and animations
├── game.js              # Game logic, rendering, and API integration
├── benchmark.js         # Model performance testing system
├── demo.js              # Demo mode - automated tournament and leaderboard
├── README.md            # User documentation
├── CLAUDE.md            # Development guidelines for AI assistants
├── specs/game-spec.md   # This specification file
└── tests/               # Test HTML files
```

---

## Features

### Core Features
- **Two AI Players**: Competing LLM-controlled snakes
- **Real-time Visualization**: Canvas-based rendering at 60fps
- **Game Log**: Live move-by-move event tracking with smart auto-scroll
  - Player-specific move numbers: "P1 - #43: 🔴 → 234ms"
  - API latency display (in milliseconds) for each move
  - Color-coded latency: teal (<500ms fast), yellow (500-1500ms medium), red (>1500ms slow)
  - Smart auto-scroll: pauses when user scrolls up, resumes when at bottom
  - Timeout indicators with ⏱️ emoji when LLM doesn't respond within 15 seconds
- **Stats Panel**: Compact side-by-side player comparison
  - API failure tracking displays failures when timeouts or errors occur
- **Debug Mode**: Checkbox to enable detailed console logging
  - Golden/yellow checkbox with tooltip reminder
  - Timestamped request/response logs
  - Request body and response data (Authorization masked)
  - Per-player move numbers for correlation
- **Stats Panel**: Clean side-by-side comparison of both players
  - Player model names with red/blue dot indicators
  - Real-time metrics: length, moves, api calls
  - **Interactive Latency Time-Series Graph**:
    - Continuous time-series visualization showing last 50 latency samples
    - Hover tooltip displays exact turn number and latency value at cursor position
    - Faint dashed vertical line highlights hovered position
    - Circle marker indicates precise data point being inspected
    - Crosshair cursor for precise positioning
  - Adaptive color-coded latency bar (green <500ms, yellow 500-1500ms, red >1500ms)
  - Dynamic markers: white line = median, purple line = p90
  - Min/Med/P90/Max statistics displayed below bar
- **Configurable Settings**: Turn delay, model selection, collision avoidance, visibility radius
- **Collision Avoidance Toggle**: Real-time control to enable/disable automatic collision detection and safe move overrides
- **Visibility Radius Control**: Adjustable snake vision radius (1-30 cells) with real-time updates
- **Model Loading**: Fetch available models via API
- **Model Filtering**: Type-to-filter search for quick model selection
- **Model Benchmarking**: Speed test system to compare AI model performance
  - Run speed tests on all loaded models with parallel API requests
  - View results in sortable table with latency and success rate statistics
  - Sort models by name or performance for easy comparison
  - Comparative analysis with ranking and success rates
- **Loop Mode**: Auto-restart after each game ends
  - 5-second countdown before restarting
  - Enabled by default via checkbox in control bar
  - Countdown shown on canvas overlay
  - Cancellable by disabling loop mode during countdown
- **Demo Mode**: Fully automated tournament system for kiosk/presentation use
  - Automated head-to-head model battles using all loaded models
  - Best-of-three match format per tournament
  - 3-minute game timeout with visual countdown (turns red at 30 seconds)
  - Leaderboard with win/loss tracking, win rate, and game statistics
  - Leaderboard persisted to localStorage across sessions
  - Model rotation to ensure variety in matchups
  - Forfeit handling when a model fails 3 consecutive API calls
  - Exportable leaderboard data as JSON
  - Pause/resume during demo mode
  - Match history display in demo panel
- **Collapsible UI Panels**: Options and Extra sections collapse/expand with smooth animation
  - Panels start in collapsed state
  - Collapse button positioned on left side of panel header
- **API Data Tracking**: Monitor data usage and performance metrics
  - Total bytes sent/received per player for LLM communication
  - Model name display with simplified format (using last segment)
  - Enhanced error tracking with detailed statistics
- **Enhanced Security**: Improved input validation and XSS protection
  - Safe DOM manipulation for user input handling
  - API URL and API key format validation
  - Bounds checking for configuration parameters
- **Performance Optimization**: Smart rendering and resource management
  - Canvas redraw optimization with state tracking
  - Memory leak prevention with proper timeout cleanup
  - Latency data management with circular buffer (max 1000 samples)
- **Fancy UI**: Dark theme with glowing effects

### Game Mechanics
- **Independent Movement**: Each snake moves independently as soon as its LLM responds - no synchronization!
- **Move Tracking**: Each snake tracks total moves made - displayed as "P1 - #43" in log header
- **Player-Specific Move Counter**: `player1MoveNumber` and `player2MoveNumber` track moves per snake
- **15-Second Timeout**: If LLM doesn't respond within 15 seconds, timeout occurs, counted as API failure, and request is retried with 2-second delay
- **Wall Wrapping**: Snakes pass through walls and emerge on opposite side
- **Multiple Fruits**: 3 fruits spawn simultaneously, 7 different types with varying growth values
- **Smart AI Safety**: Collision detection + automatic safe move override (can be disabled via toggle)
- **Configurable Collision Avoidance**: Real-time toggle to enable/disable both LLM safe move hints and automatic collision avoidance
- **Limited Visibility System**: Snakes have adjustable vision radius (1-30 cells) with default 5-cell radius
- **Visual Board View**: LLMs receive ASCII board representation (11x11 area with wrap)
- **Danger Indicators**: ⚠️ warnings on log when snake in danger
- **Content Stripping**: Automatically strips `<thinking>` and similar tags from LLM responses

### Visual Features
- **7 Distinct Fruit Types**: Each with unique visual representation and animations
- **Fruit Legend**: Always visible compact panel showing all fruit types, values, and spawn rates
- **Animated Effects**: Pulse, flutter, sparkle animations for rare fruits
- **Control Buttons**: Compact Start Battle (always visible), Pause, Reset buttons in single row
- **Compact UI**: Reduced padding, smaller fonts for efficient space use
- **Color-coded Players**: Red (Player 1) vs Blue (Player 2)
- **Custom Scrollbar**: Styled scrollbar on game log panel

---

## UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│              🐍 Snake Battle 🐍                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  VS  ┌─────────────────────┐      │
│  │ 🔴 model-name       │      │ 🔵 model-name       │      │
│  │ len 5  moves 42     │      │ len 3  moves 38     │      │
│  │ calls 42            │      │ calls 38            │      │
│  │                     │      │                     │      │
│  │ 1250 ms [████|░|░░]│      │ 650 ms [██|░░░|░]  │      │
│  │  min  med  p90  max │      │  min  med  p90  max │      │
│  │  400  800  1200 1800│      │  300  500  800  1100│      │
│  └─────────────────────┘      └─────────────────────┘      │
├─────────────────────────────────────────────────────────────┤
│              ⏱️ Timer Display                              │
├─────────────────────────────────────────────────────────────┤
│     [Start Battle]   [⏸️]   [🔄]   [🐛 Debug Mode]        │
├─────────────────────────────────────────────────────────────┤
│  Fruit      │                              │                │
│  Legend     │       Game Canvas            │   Game Log     │
│  Panel      │      (30x30 grid)            │ (height=canvas)│
│  (7 items)  │                              │ (scrollable)   │
│             │                              │ (compact font) │
└─────────────────────────────────────────────────────────────┘
```

---

## Game Rules

### Movement
- Each snake starts with 3 segments on opposite sides of 30x30 grid
- **Snakes move INDEPENDENTLY** - each snake moves immediately when its LLM responds
- No turn synchronization - faster-responding models will move more often
- **15-Second Timeout**: If LLM doesn't respond within 15 seconds, counts as API failure, retries after 2-second delay
- LLM chooses direction: up, down, left, or right
- Cannot reverse direction (can't go back the way came)
- **Move Counter**: Tracks total moves per snake as "P1 - #N" in logs

### Collision & Death
- **Walls are SAFE**: Going through a wall wraps to opposite side
  - Left ↔ Right edge wrap: `x` position 30 becomes 0, -1 becomes 29
  - Top ↔ Bottom edge wrap: `y` position 30 becomes 0, -1 becomes 29
- **Snake Collisions are DEADLY**:
  - Hitting your own body = death
  - Hitting enemy snake = death
  - Head-on collision = both die (detected after either snake moves into position)
- Winner: Longer snake survives; if same length, draw

### Fruit System
- 3 fruits on board at all times
- Eating fruit grows snake by corresponding value (1-5 segments)
- Multiple fruits can be eaten in single turn
- Rare fruits spawn less frequently but give more growth
- Fruits spawn at random valid positions (not on snakes or other fruits)

---

## Fruit Types

| Emoji | Name | Growth | Rarity | Spawn Rate | Visual Effect |
|-------|------|--------|--------|------------|---------------|
| 🍎 | Apple | +1 | Common | 40% | Red circle with green leaf |
| ⭐ | Star | +3 | Uncommon | 25% | Golden 5-pointed star with glow |
| 🍇 | Grapes | +2 | Uncommon | 15% | Purple cluster with stem |
| 🍒 | Cherry | +2 | Rare | 10% | Two red cherries with connecting stem |
| 🦋 | Butterfly | +3 | Rare | 6% | Teal wings with **fluttering animation** |
| 💎 | Diamond | +4 | Very Rare | 3% | Sparkling gem with **pulse + sparkle** |
| 🎁 | Present | +5 | Ultra Rare | 1% | Gift box with **particle sparkles** |

**Visual Scale & Animations:**
- **Apple**: Simple 10px radius red circle, green leaf ellipse
- **Star**: 5-pointed star, outer radius 7px, inner radius 3px
- **Grapes**: 5 small circles (3.5-4px radius) forming cluster
- **Cherry**: Two 4px circles connected by curved stem
- **Butterfly**: Wings 5x6px, **animated flutter** using `Math.sin(Date.now() / 100)`
- **Diamond**: Diamond shape 7px x 8px, **pulse animation** using `Math.sin(Date.now() / 200)`
- **Present**: 10x9px rectangle with ribbon, **sparkle particles** with `Math.sin(Date.now() / 150)`

---

## API Integration

### Endpoints Required
```
GET /models                    # List available models
POST /chat/completions         # Get LLM decision
```

### Request: Load Models
```http
GET {apiUrl}models
Authorization: Bearer {apiKey}
```

Expected response format:
```json
{
  "data": [
    { "id": "model-name-1" },
    { "id": "model-name-2" }
  ]
}
```

### Request: Get LLM Decision
```http
POST {apiUrl}chat/completions
Authorization: Bearer {apiKey}
Content-Type: application/json
```

Request body:
```json
{
  "model": "{selectedModelId}",
  "messages": [
    {
      "role": "system",
      "content": "You are a snake game AI. Your goal: SURVIVE longer than your opponent while eating fruits to grow. Respond INSTANTLY with ONLY ONE WORD: up, down, left, or right. NO thinking, NO explanation, NO extra text. JUST the direction. Walls are safe - you wrap through them. Avoid your body and enemy snakes."
    },
    {
      "role": "user",
      "content": "{gameStatePrompt}"
    }
  ],
  "temperature": 0
}
```

### LLM Prompt Structure
The game state prompt includes:
1. Player identification (color, length, position, enemy info)
2. All fruits with positions, values, emojis, and distances
3. Closest fruit highlighted
4. 11x11 ASCII board view centered on player head (with wrap support)
5. Danger check for each direction (UP/DOWN/LEFT/RIGHT)
6. Rules summary including wall wrapping
7. Required response format (single word)

Example prompt snippet:
```
You are Player 1 (snake red 🔴)
Your length: 8 | Enemy length: 7
Your head at: (12, 15)
Enemy head at: (25, 15)

FRUITS (3 available):
1. 🍎 at (18, 12) - Value: 1 - Distance: 7
2. ⭐ at (5, 8) - Value: 3 - Distance: 9
3. 💎 at (28, 25) - Value: 4 - Distance: 20

Board view (11x11 area around you):
@ = your head | ★ = fruit | R/r = your body | B/b = enemy | . = empty
 Walls WRAP AROUND - going through one side brings you out the other!
...
```

---

## Configuration Options

### User-Configurable (via UI)
| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| API URL | https://api.tokenfactory.nebius.com/v1/ | - | OpenAI-compatible API endpoint |
| API Key | - | Required | Authentication key (password input) |
| Player 1 Model | First available | - | LLM controlling red snake |
| Player 2 Model | Second available | - | LLM controlling blue snake |
| Debug Mode | Off | On/Off | Enable detailed console logging for debugging |
| Collision Avoidance | On | On/Off | Enable/disable automatic collision detection and safe move overrides |
| Visibility Radius | 5 | 1-30 | Snake vision radius in cells (5=default, 30=full grid) |

### Hardcoded Constants (in game.js)
| Constant | Value | Description |
|----------|-------|-------------|
| `GRID_SIZE` | 30 | Board dimensions (30x30 = 900 cells) |
| `CELL_SIZE` | 20 | Pixel size of each cell (600x600px canvas) |
| `CANVAS_WIDTH` | 600 | Canvas width in pixels |
| `CANVAS_HEIGHT` | 600 | Canvas height in pixels |
| `NUM_FRUITS` | 3 | Number of fruits on board |
| `FRUIT_TYPES` | Array | Fruit configuration with spawn weights |

---

## UI Components

### Setup Screen
- **Title**: "🐍 Snake Battle 🐍"
- **API URL Field**: Text input pre-filled with Nebius endpoint
- **API Key Field**: Password input for authentication
- **Load Models Button**: Triggers model fetch from API
- **Loading Spinner**: Shows during API request
- **Model Filter Inputs**: Two text inputs (above dropdowns) for type-to-filter model search
  - Real-time filtering as you type
  - Case-insensitive matching
  - Automatically selects first visible model if current selection is filtered out
  - Placeholder: "Type to filter models..."
- **Model Dropdowns**: Two selects for model selection (P1 and P2)
- **Options Section**: Configurable game options with real-time adjustments
  - Visibility Radius control (1-30, default 5) with validation
  - Collision Avoidance toggle (enabled by default) with immediate effect
  - Consistent styling with debug mode checkbox
- **Turn Delay Input**: Number input for game speed (**kept for future use**)
- **Start Battle Button**: Begins game transition

### Game Screen

#### Header Row
- **Player 1 Score**: Red 🔴 with:
  - Length display (e.g., "Length: 3")
  - Move counter on next line in smaller font (e.g., "moves: 42")
  - API call count on third line in smaller font (e.g., "API calls: 42")
- **Title**: "🐍 Snake Battle 🐍"
- **Player 2 Score**: Blue 🔵 with:
  - Length display (e.g., "Length: 3")
  - Move counter on next line in smaller font (e.g., "moves: 38")
  - API call count on third line in smaller font (e.g., "API calls: 38")

#### Control Buttons
- Single compact row: Start Battle, Pause (⏸️), Reset (🔄)
- **Start Battle**: Always visible, start new game anytime
- **Pause/Resume**: Toggle game state (pauses both snake loops, aborts requests)
- **Reset/Restart**: Restart with fresh game
- **Debug**: Compact checkbox (🐛) to enable detailed console logging (tooltip at button)
- **Options**: Real-time game configuration controls
  - Collision Avoidance toggle (🛡️) to enable/disable safety features
  - Visibility Radius slider/input for adjusting snake vision (1-30 cells)
  - All options provide immediate feedback with no game restart required
- Extra-small tight padding, reduced font sizes
- Gradient styling: Green (start), Pink (pause), Purple (reset), Gold (debug), Blue (options)

#### Game Layout (Three Columns)

**Game Timer Display**
- Positioned below stats panel in center
- Shows elapsed game time in format ⏱️ MM:SS
- Compact styling with gradient background
- Updates in real-time

**Compact Control Buttons**
- Single row containing: Start Battle, Pause (⏸️), Reset (🔄)
- All buttons remain visible during gameplay
- Extra-small, tight padding and reduced font sizes
- Start Battle can be clicked to start new game anytime
- **Debug Mode**: Compact checkbox (🐛) with tooltip showing at button position

**⚙️ Options Panel**
- **Location**: Below the control buttons section in the game UI
- **Visibility Radius Control**:
  - Numerical input field for setting snake vision radius (1-30 cells)
  - Default value of 5 cells provides balanced gameplay challenge
  - Real-time adjustment with immediate effect on game state
  - Hint text showing valid range and default value
- **Collision Avoidance Toggle**:
  - Checkbox with shield emoji (🛡️) for enabling/disabling safety features
  - Enabled by default for safer gameplay
  - Controls both LLM safe move hints and automatic collision avoidance
  - Immediate effect with visual feedback in game log
- **Styling**: Consistent with other compact UI controls, minimal padding and reduced font sizes

**Left: Fruit Legend Panel**
- Always visible, compact panel showing all fruit types
- 7 fruit items with smaller, condensed layout:
  - Emoji icon (reduced size)
  - Fruit name (smaller font)
  - Growth value (color-coded, not bold)
  - Rarity percentage (smaller font)
- Minimal padding and gaps

**Player Stats Cards** (in stats panel):
- Compact bordered cards for each player (Player 1 + Player 2)
- Model name with colored dot indicator (red/blue)
- Real-time metrics: length, moves, api failures (not bold, regular font)
- **Interactive Latency Time-Series Graph**:
  - Shows last 50 latency samples as time-series line
  - Gradient fill under the line
  - Smaller, non-bold latency stats below graph
  - **Hover Interaction**:
    * Tooltip shows "P1 Move: #43" with player identifier
    * Dashed vertical line highlights hovered position
    * Circle marker on data point
    * Crosshair cursor for precise positioning
- Min/Med/P90/Max stats in compact, spaced layout

**Center: Game Canvas**
- 600x600 pixel canvas (30x30 grid at 20px per cell)
- Dark background (#0a0a15)
- Subtle grid lines (rgba(255,255,255,0.05))
- Glowing border effect
- Vertically aligned with fruit legend and game log panels

**Right: Game Log Panel**
- Title: "Game Log"
- Width: 250px, max-height: 400px (constrained to match canvas height)
- Always-visible scrollbar with custom styling
- **Compact font sizes** for better space efficiency
- Border-bottom separator on title
- Turn-by-turn event tracking with color-coding:
  - Turn numbers
  - Red moves (↑↓←→) independent of blue moves
  - Blue moves
  - Danger warnings (⚠️) when snake in deadly position
  - Food consumption (fruit emoji + growth)
  - Collision/crash events
  - API latency display (color-coded: teal/yellow/red for fast/medium/slow)
  - Timeout indicators (⏱️) when LLM doesn't respond within 15 seconds
- Smart auto-scroll: pauses when user scrolls up, resumes when at bottom
- Custom scrollbar styling (teal gradient thumb)

**Bottom: Latency Meter**
- Title: "📊 API Latency Meter"
- Two player latency meters side by side:
  - 🔴 Player 1 (Red snake) meter
  - 🔵 Player 2 (Blue snake) meter
- Each meter shows:
  - Visual bar with gradient colors (teal → yellow → red based on latency)
  - White line marker for median latency
  - Magenta line marker for p90 latency
  - Sample count below each meter
- Hover tooltip with detailed statistics:
  - Min, Max, Mean, Median, P90, P95, P99 latencies
  - Standard deviation (Std Dev)
  - Total sample count
- Ruler scale at bottom: 0ms to 3000ms in 500ms increments
- Tick marks on meter: minor every 50ms, major every 500ms
- Bar width represents up to 95th percentile for better visualization
- Updates in real-time as API calls are made
- Resets when game restarts

#### Log Entry Format
```
<span style="color: #FF6B6B;">P1 - #43</span>: 🔴⚠️ → 234ms
<span style="color: #4ECDC4;">P2 - #38</span>: 🔵 ↓ 567ms
<span style="color: #FF6B6B;">P1 - #44</span>: 💎 Ate +4
<span style="color: #4ECDC4;">P2 - #39</span>: ⏱️ Timeout (10s) - retrying...
<span style="color: #FF6B6B;">P1 - #45</span>: 💥 HEAD-ON COLLISION!
```

**Log Format Notes:**
- Player header: "P1" or "P2" with color matching snake (red/blue)
- Move number: "#43" increments per player independently
- Snake emoji: 🔴 (red snake), 🔵 (blue snake), with ⚠️ if in danger
- Direction arrow: ↑↓←→ matching actual movement direction
- Latency: in milliseconds if available, color-coded
- Timeout: ⏱️ emoji when LLM times out with duration
- Food: Emoji with growth value (+1 to +5)
- Crashes: 💥💀 emojis with collision details

**Latency Color Coding:**
- Teal (< 500ms): Fast response
- Yellow (500-1500ms): Medium response
- Red (> 1500ms): Slow response

---

## Code Architecture

### Game State Object
```javascript
{
    snake1: [{x, y}, ...],           // Red snake segments [head, ...tail]
    snake2: [{x, y}, ...],           // Blue snake segments [head, ...tail]
    fruits: [                        // Array of fruit objects
        {
            x: number,              // Grid X position
            y: number,              // Grid Y position
            type: {                 // Fruit type object
                emoji: string,      // Emoji display
                value: number,      // Growth amount
                color: string       // Rendering color
            },
            spawned: timestamp       // Spawn timestamp
        },
        ...
    ],
    direction1: {x: y},              // Current direction vector for P1
    direction2: {x, y},              // Current direction vector for P2
    nextDirection1: {x, y},          // Buffer for next turn
    nextDirection2: {x, y},
    gameOver: boolean,
    paused: boolean,
    player1Dead: boolean,            // Tracks if P1 has died
    player2Dead: boolean,            // Tracks if P2 has died
    player1Moves: number,            // Total moves made by P1
    player2Moves: number,            // Total moves made by P2
    player1MoveNumber: number,         // Move counter for P1 (displayed as P1 - #N)
    player2MoveNumber: number,         // Move counter for P2 (displayed as P2 - #N)
    player1ApiCalls: number,         // Total API calls made by P1
    player2ApiCalls: number,         // Total API calls made by P2
    player1ApiFailures: number,       // API failures for P1 (counted since v2.6)
    player2ApiFailures: number,       // API failures for P2 (counted since v2.6)
    turnDelay: number,               // Milliseconds between turns (legacy)
    apiUrl: string,
    apiKey: string,
    player1Model: string,
    player2Model: string,
    debugMode: boolean,              // Enable console logging
    collisionAvoidanceEnabled: boolean, // Enable/disable collision avoidance (default: true)
    loopMode: boolean,               // Auto-restart games when loop mode is enabled
    finalElapsedTime: number,        // Frozen elapsed time when game ends (for display)
    loopCountdownRemaining: number,  // Countdown seconds remaining before auto-restart
    loopCountdownInterval: any       // Timer ID for loop countdown
}
```

### Key Functions

#### Initialization
- `initializeGame()` - Reset game state, spawn fruits at valid positions, reset move counters
- `populateFruitLegend()` - Build legend UI from FRUIT_TYPES array
- `startAnimation()` - Begin 60fps continuous render loop

#### Model Selection & Filtering
- `loadModels()` - Fetch available models from API `GET /models` endpoint
- `populateModelSelects()` - Populate both player dropdowns with available models and setup filter functionality
- `setupModelFilters()` - Attach input event listeners to model filter inputs
- `filterModels(selectElement, filterText)` - Filter dropdown options in real-time
  - Hides options that don't match filter text (case-insensitive)
  - Automatically selects first visible option if currently selected one is hidden

#### Game Loop
- `gameLoop()` - Entry point that starts both snake loops
  - Calls `moveSnakeWithLLM(1)` and `moveSnakeWithLLM(2)` in parallel
  - Snake loops run independently, no synchronization

- `moveSnakeWithLLM(playerNum)` - **Independent snake movement**
  1. Check if game over or snake already dead
  2. Get LLM decision via API (async - takes however long model responds)
     - Returns `{ direction, latency }` with API response time
  3. Apply safe move override if needed
  4. Call `moveSingleSnake(playerNum, latency)` to immediately move snake
  5. Recursively call itself for next move (if game continues)
  - **Result**: Each snake moves as fast as its model responds

- `moveSingleSnake(playerNum, latency)` - Handle single snake movement
  1. Check if paused, game over, or snake dead
  2. Increment move counter and turn counter
  3. Update score displays (length + moves)
  4. Log direction with danger warnings and API latency
  5. Move snake with wall wrapping
  6. Check collisions and handle deaths
  7. Check fruit consumption
  8. Grow/shrink snake
  9. Check game over condition
  10. Draw frame

- `checkGameOver()` - Determine winner/end game
  1. Check if both snakes dead → longer snake wins (or draw)
  2. Check if one snake dead → other wins
  3. Handle game over UI and log messages

#### Movement & Collision
- `moveSnake(snake, direction)` - Add new head at front with wall wrapping
- `wrapPosition(x, y)` - Handle wall wrapping: `((x % GRID_SIZE) + GRID_SIZE) % GRID_SIZE`
- `isMoveDeadly(snake, direction, otherSnake)` - Check if move causes death
- `checkCollision(snake, head, otherSnake)` - Detect collision type (self/enemy)
- `checkHeadToHead(head1, head2)` - Detect simultaneous crash at same position

#### LLM Integration
- `getLLMDirection(playerNum)` - Request LLM decision via API
  - Returns `{ direction, latency }` object
  - Tracks API response time in milliseconds
  - Calls `getBoardState(playerNum)` for prompt
  - Sends POST request to chat/completions endpoint
  - **15-Second Timeout**: Uses `Promise.race` with 15-second timeout
  - **Timeout Handling**: Counts as API failure, retries after 2-second delay
  - **Error Handling**: Gracefully handles API errors (429 rate limit, etc.)
  - Logs detailed request/response info if debug mode enabled
  - Parses response and extracts direction
  - Strips `<thinking>`, `<think>`, `<thought>`, `<reasoning>` tags from response
  - Applies safety override if move is deadly
  - Falls back to `getSafestDirection()` on error or invalid response
  - Returns latency even when using fallback logic
  - Includes timestamps in debug logs for correlation
  - **Pause Support**: Aborts outstanding requests when game is paused
- **Adaptive max_tokens Management**: Intelligent token limit handling
  - Starts with conservative `max_tokens=10` for fast responses
  - Automatically increases to 100, then 1000 if responses are cut off or null
  - Removes max_tokens restriction entirely if still insufficient
  - Independent per-player optimization based on individual model behavior
  - Visual logging in game log when adjustments occur (⚙️ Upping max_tokens: X → Y)

- `getBoardState(playerNum)` - Generate prompt from game state
  - Calculate distances to all fruits and enemy
  - Find closest fruit for targeting
  - Build ASCII board view centered on player head with configurable radius (1-30 cells)
  - Board view accounts for wall wrapping (no walls shown)
  - List all fruits with positions, values, emojis
  - Danger check for all 4 directions (UP/DOWN/LEFT/RIGHT)
  - Include rules about wall wrapping and current visibility radius
  - System prompt informs AI of exact vision radius for strategic decision-making

#### AI Safety System
- `getSafestDirection(snake, currentDir, otherSnake)` - Find best safe move
  - Filter out reverse direction
  - Separate safe vs deadly moves
  - Among safe moves, pick closest to fruit
  - If no safe moves, pick least deadly (closest to fruit anyway)
  - Prevents self-inflicted wall deaths (before wall wrapping was added)

#### Fruit Management
- `placeFruit()` - Spawn new fruit at random valid position
  - Tries up to 100 times to find unoccupied position
  - Weighted random selection based on spawn probabilities
  - Returns null if no valid position found
- `removeFruit(x, y)` - Remove fruit from fruits array (returns removed object)

#### Rendering
- `draw()` - Main draw function, called every frame
  1. Clear canvas with background color
  2. Draw subtle grid lines
  3. Draw all fruits with unique visuals and animations
  4. Draw both snakes (bodies then heads)
  5. Draw snake eyes on heads
  6. Draw game over overlay if active
- `drawSnake(snake, bodyColor, headColor)` - Render single snake
  - Draws all segments with body color
  - Head gets different color and glow effect
  - Eyes drawn on head segment

#### Fruit-Specific Drawing
Each fruit type has custom rendering:
- **Apple**: Red circle with green leaf (static)
- **Star**: Golden 5-pointed star (static)
- **Grapes**: Purple cluster with stem (static)
- **Cherry**: Two cherries with stem (static)
- **Butterfly**: Teal wings, animated flutter using `Math.sin(Date.now() / 100)`
- **Diamond**: Cyan gem, pulse animation using `Math.sin(Date.now() / 200)`, sparkles
- **Present**: Orange box with ribbon, sparkle particles with offset animation

#### UI Updates
- `updateScores()` - Update length, move, and API call displays (P1 and P2)
  - Updates: snake lengths, move counters, API call counters
  - Displays length on main line, moves on second line, API calls on third line
  - Note: Currently moves = API calls (1:1 ratio), tracked separately for clarity
- `addLog(message)` - Add log entry with auto-scroll
  - Creates paragraph element
  - Formats with turn number
  - Appends to log container
  - Smoothly scrolls to bottom using `requestAnimationFrame`
- `togglePause()` - Pause/resume both snake loops
- `toggleDebug()` - Toggle debug mode for console logging
- `toggleCollisionAvoidance()` - Toggle collision avoidance feature on/off
  - Updates collisionAvoidanceEnabled flag globally
  - Provides immediate visual feedback in game log
  - Affects both LLM safe move hints and automatic collision avoidance
- `updateViewRadius(radius)` - Update snake vision radius in real-time
  - Validates radius value between 1-30 cells
  - Updates VIEW_RADIUS constant immediately
  - Triggers redraw to reflect new visibility area
  - Ensures safe bounds checking for extreme values
- `showDebugTooltip()` - Show "Check console logs" tooltip when enabling debug
- `restartGame()` - Reset everything and start fresh
- `backToSetup()` - Return to model selection screen
- `loadModels()` - Fetch and display available models from API
- `toggleLoopMode()` - Toggle loop mode on/off, manage countdown
- `startLoopCountdown()` - Begin 5-second countdown before auto-restart
- `updateLoopCountdownDisplay()` - Update countdown overlay on canvas
- `stopLoopCountdown()` - Cancel auto-restart countdown
- `startGame(fromDemoMode)` - Start game, interceptable by demo mode

#### Demo Mode Architecture (demo.js)
`DemoMode` class — instantiated as `window.demoMode` after models are loaded.

**Key Properties**:
- `isActive`, `isPaused` — demo state flags
- `currentMatch`, `currentGame` — tournament progress counters
- `seriesScore` — `{player1, player2}` win counts for current best-of-3
- `leaderboard` — model stats object, persisted to `localStorage`
- `matchHistory` — array of match records for history display
- `gameTimeout` / `gameCountdownInterval` — 3-minute per-game timer

**Key Methods**:
- `toggleDemoMode()` — start or stop demo mode
- `startDemoMode()` — initialize and kick off first match
- `stopDemoMode()` — stop all timers, restore config UI
- `startNextMatch()` — select random model pair, set game state, start game
- `selectRandomModels()` — picks two distinct models, rotates through all loaded models
- `handleGameEnd(winner)` — update series score, decide next action (next game or series end)
- `handleSeriesComplete()` — update leaderboard, trigger next tournament after 10-second countdown
- `handleGameTimeout()` — end game as tie, start next game after 3 seconds
- `handleForfeit(player)` — immediately end series when a model forfeits
- `startGameTimeout()` — 180-second `setTimeout` per game
- `startGameCountdown()` / `stopGameCountdown()` — live countdown display in demo panel
- `startCountdown(duration, callback)` — generic between-game countdown display
- `updateLeaderboard(model, result, stats)` — record win/loss, moves, max length
- `showLeaderboard()` / `hideLeaderboard()` — modal display of ranked leaderboard table
- `exportLeaderboard()` — download `snake-demo-leaderboard.json`

**Custom DOM Events dispatched**:
- `modelsLoaded` — enables demo controls when models finish loading
- `gameEnded` — triggers `handleGameEnd()` with winner detail
- `gamePaused` / `gameResumed` — sync demo pause state with game pause button
- `gameRestarted` — handled to advance demo state
- `playerForfeited` — triggers forfeit logic in demo mode

#### Latency Tracking & Display
- `trackLatency(playerNum, latency)` - Record latency sample and update meter
  - Pushes latency to appropriate player's latency array
  - Calls updateLatencyMeter to refresh display
  - Calls updateLatencyGraph to redraw time-series graph

- `updateLatencyMeter(playerNum)` - Refresh latency meter display
  - Updates sample count display
  - Calls updateLatencyBar for visual update
  - Calls updateLatencyStats for tooltip statistics

- `updateLatencyBar(playerNum, latencies)` - Update visual bar with markers
  - Calculates median and p90 percentiles
  - Positions white line marker for median
  - Positions magenta line marker for p90
  - Sets bar width based on 95th percentile for optimal visualization
  - Scale adjusts to minimum 3000ms or max latency

- `updateLatencyStats(playerNum, latencies)` - Update tooltip statistics
  - Calculates: Min, Max, Mean, Median, P90, P95, P99, Standard Deviation
  - Updates all tooltip stat elements
  - Handles empty array case with "-" display

- `calculatePercentile(sortedArray, percentile)` - Calculate percentile value
  - Interpolates between values for precise percentile calculation
  - Handles edge cases for array bounds

- `drawLatencyGraph(playerNum, latencies)` - Render time-series graph
  - Draws continuous line graph of latency history (last 50 samples)
  - Calculates adaptive scale based on visible window, not global data
  - Draws background grid and threshold lines (fast=500ms, slow=1500ms)
  - Applies player-specific colors (red=P1, teal=P2)
  - Adds current value dot with color coding
  - Stores graph data in canvas dataset for mouse interaction

- `createLatencyTooltip()` - Initialize tooltip DOM element
  - Creates reusable tooltip with turn number and latency value
  - Adds CSS styles dynamically if not present
  - Tooltips populate with data from hovered graph position

- `handleLatencyGraphMouseMove(event, canvas, playerNum)` - Process mouse hover
  - Detects mouse position within canvas bounds
  - Finds closest data point based on X coordinate
  - Positions tooltip near mouse with smart boundary detection
  - Updates tooltip content with turn number and latency value
  - Calls redrawGraphWithOverlay to show indicators
  - Stores hover state for future redraws

- `redrawGraphWithOverlay(canvas, playerNum, highlightIndex)` - Draw hover indicators
  - Uses separate overlay canvas for non-destructive rendering
  - Draws dashed vertical line at hovered position
  - Draws circle marker at data point (white outer, player-colored inner)
  - Applies player-specific colors for the inner dot

- `handleLatencyGraphMouseLeave(canvas)` - Clean up on mouse exit
  - Hides tooltip with smooth transition
  - Clears hover state from canvas dataset
  - Clears overlay canvas indicators

- `hideLatencyTooltip()` - Hide tooltip with transition
  - Removes 'visible' class for opacity fade
  - Pointer events disabled on tooltip to avoid interference

- `resetLatencyTracking()` - Clear all latency data
  - Empties player1Latencies and player2Latencies arrays
  - Resets both latency meters to empty state
  - Clears both canvas elements
  - Clears stats displays
  - Called in initializeGame() and restartGame()

---

## Visual Design

### Color Palette

| Element | Color | Purpose |
|---------|-------|---------|
| Background | `#0a0a15` | Canvas background |
| Grid Lines | `rgba(255,255,255,0.05)` | Subtle grid overlay |
| Player 1 Body | `#FF6B6B` | Red snake body |
| Player 1 Head | `#FF4444` | Bright red head with glow |
| Player 2 Body | `#4ECDC4` | Teal/blue snake body |
| Player 2 Head | `#44B3AC` | Brighter teal head with glow |
| Accent / UI | `#4ECDC4` | Primary accent color |
| Text (Primary) | `#FFFFFF` | Main headings, labels |
| Text (Secondary) | `#E0E0E0` | Secondary text, body |
| Text (Moves) | `#888` | Move counter (smaller, grayed) |
| Error | `#FF6B6B` | Error messages |
| Log Red Actions | `#FF6B6B` | Player 1 moves |
| Log Blue Actions | `#4ECDC4` | Player 2 moves |
| Log Food | `#FFD93D` | Fruit consumption |
| Log Crash | `#FF6B6B` | Death/crash events |
| Latency Fast (<500ms) | `#4ECDC4` | Teal with semi-transparent bg |
| Latency Medium (500-1500ms) | `#FFDD59` | Yellow with semi-transparent bg |
| Latency Slow (>1500ms) | `#FF6B6B` | Red with semi-transparent bg |

### Fruit Colors
- Apple: `#FF6B6B` (red)
- Grapes: `#9B5DE5` (purple)
- Star: `#FFD93D` (gold)
- Cherry: `#FF4444` (dark red)
- Butterfly: `#00F5D4` (teal)
- Diamond: `#00D9FF` (cyan)
- Present: `#FF9F1C` (orange)

### Effects
- **Glow**: `shadowBlur: 10-20px` on snake heads and fruits
- **Glass Effect**: `backdrop-filter: blur(10px)` on all panels
- **Gradients**: Linear gradients on buttons (`135deg`)
- **Hover Transform**: `translateY(-2px)` on buttons and fruit legend items
- **Animation**: 60fps continuous rendering via `requestAnimationFrame`

### Fruit-Specific Animation Formulas
```javascript
// Butterfly wings flutter
const flutter = Math.sin(Date.now() / 100) * 0.1;

// Diamond pulse
const pulse = Math.sin(Date.now() / 200) * 2;

// Present sparkles
const offset = Math.sin(Date.now() / 150 + p.dx + p.dy) * 1;
```

### Move Counter Styling
```css
.moves {
    font-size: 0.8em;        /* 80% of normal size */
    color: #888;             /* Gray color */
}
```

### Model Filter Input Styling
```css
.model-filter {
    width: 100%;
    padding: 10px 14px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    font-size: 14px;
    margin-bottom: 8px;
    transition: all 0.3s;
}

.model-filter:focus {
    outline: none;
    border-color: #4ecdc4;    /* Teal accent on focus */
    background: rgba(255, 255, 255, 0.15);
}

.model-filter::placeholder {
    color: rgba(255, 255, 255, 0.5);
}
```

### Latency Tooltip Styling
```css
.latency-graph-tooltip {
    position: fixed;
    background: rgba(0, 0, 0, 0.95);
    border: 1px solid rgba(78, 205, 196, 0.5);
    border-radius: 6px;
    padding: 8px 12px;
    z-index: 10000;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.15s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
    font-size: 12px;
}

.latency-graph-tooltip.visible {
    opacity: 1;
}

.tooltip-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 4px;
}

.tooltip-row:last-child {
    margin-bottom: 0;
}

.tooltip-label {
    color: #888;
}

.tooltip-value {
    color: #4ecdc4;
    font-weight: 600;
}

.latency-graph-overlay {
    position: absolute;
    top: 0;
    left: 0;
    pointer-events: none;
    z-index: 10;
}
```

### Latency Graph Styling
```css
.latency-timegraph {
    margin-top: 8px;
    width: 100%;
    height: 80px;
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

.latency-graph-container {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.latency-timegraph canvas {
    position: relative;
    display: block;
    width: 100%;
    height: 80px;
    z-index: 1;
    cursor: crosshair;
}
```

### Latency Stats Styling
```css
.latency-stats {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin-top: 6px;
    padding: 4px 0;
}

.latency-stat {
    flex: 1;
    text-align: center;
    font-size: 0.65em;
    color: #888;
}

.latency-stat label {
    display: block;
    margin-bottom: 2px;
    color: #666;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.latency-stat value {
    font-size: 1.2em;
    font-weight: bold;
    color: #e0e0e0;
}
```
    margin-bottom: 8px;
    transition: all 0.3s;
}

.model-filter:focus {
    outline: none;
    border-color: #4ecdc4;    /* Teal accent on focus */
    background: rgba(255, 255, 255, 0.15);
}

.model-filter::placeholder {
    color: rgba(255, 255, 255, 0.5);
}
```

### Scrollbar Styling
- **Width**: 10px
- **Thumb**: Linear gradient from `rgba(78, 205, 196, 0.4)` to `rgba(78, 205, 196, 0.6)`
- **Track**: `rgba(0, 0, 0, 0.3)`
- **Hover**: Brighter gradient on thumb
- **Border**: 1px teal border on thumb
- **Firefox**: `scrollbar-width: thin`

---

## Browser Compatibility

- **Browsers**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Features Required**:
  - Canvas API (2D context)
  - Fetch API (for HTTP requests)
  - ES6+ JavaScript (arrow functions, template literals, destructuring, spread, async/await)
  - CSS Grid & Flexbox (for layout)
  - `requestAnimationFrame` (for animation loop)
  - `backdrop-filter` (optional, glass effect degrades gracefully)

---

## Dependencies

**None** - Pure vanilla HTML/CSS/JavaScript

**External Services**:
- OpenAI-compatible LLM API (for AI decisions)
- No native dependencies or build tools required

---

## Build Instructions

No build process required. Simply:
1. Clone/download all 4 files (index.html, style.css, game.js)
2. Open `index.html` in a modern web browser
3. Enter API URL and API key
4. Click "Load Models"
5. Select models for both players
6. Click "Start Battle!"

**For development server** (optional):
```bash
# Python:
python3 -m http.server 8000
# Then visit http://localhost:8000

# Node.js (if available):
npx serve .
# Then visit the URL shown
```

---

## Configuration for Different APIs

### OpenAI
```
API URL: https://api.openai.com/v1/
Models: gpt-4, gpt-4-turbo, gpt-3.5-turbo, gpt-4o, etc.
Key: sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### Anthropic (via compatible proxy)
```
API URL: {proxy-url}/v1/
Models: claude-3-sonnet-20240229, claude-3-haiku-20240307, etc.
Key: sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```

### Nebius Token Factory (default - pre-filled)
```
API URL: https://api.tokenfactory.nebius.com/v1/
Models: Llama 3.x, Mistral, etc.
Key: (user-provided)
```

### Local LLM (e.g., Ollama)
```
API URL: http://localhost:11434/v1/
Models: llama3, mistral, codellama, etc.
Key: (often not required for local)
```

### LM Studio
```
API URL: http://localhost:1234/v1/
Models: Available models in LM Studio GUI
Key: (may use "lm-studio" or leave blank)
```

---

## Extension Ideas

### Potential Enhancements
- **Multiplayer**: Human vs AI or Human vs Human keyboard controls
- **Obstacles**: Static barriers or terrain features on the board
- **Power-ups**: Speed boost, invincibility, shrink enemy, teleport
- **Tournament Mode**: Round-robin AI matchups with leaderboards
- **Replay System**: Record and replay entire games
- **Save/Load**: Save game state to browser storage
- **Custom Prompts**: Allow user to edit system prompts
- **Board Themes**: Different color schemes, grid sizes, backgrounds
- **Sound Effects**: Audio feedback for food, crash, win events
- **Statistics Dashboard**: Track win rates, avg length, match history, move counts
- **More Fruit Types**: Add seasonal or themed fruits
- **Spectator Mode**: Dropdown to select any two models to watch
- **Visualization**: Real-time graph showing move count over time

---

## Troubleshooting

### Common Issues

**"Failed to load models"**
- Check API URL ends with `/`
- Verify API key is correct (not expired)
- Check browser console (F12 → Console tab) for errors
- Ensure API is accessible from your location (CORS may be an issue)
- Test API URL manually with curl or Postman

**Snakes move erratically or crash early**
- LLM might not understand the prompt format well
- Safety override system should prevent obvious crashes
- Try different models (some are better at this task)
- Check game log for ⚠️ danger warnings

**One snake barely moves**
- The model may be very slow responding
- Try a faster model for comparison
- Move counter makes this speed difference visible
- This is intended behavior - models with better response times have advantage

**Game too slow/fast**
- Game speed is now determined by model response times
- There is no fixed turn delay - snakes move as soon as they get a decision
- Faster models = more frequent moves = faster snake

**Visual artifacts or canvas issues**
- Some browsers may not support `backdrop-filter` (glass effect)
- Game should still function with solid backgrounds
- Try updating to latest browser version
- Disable hardware acceleration if canvas flickers

**Scrollbar doesn't appear**
- Scrollbar appears only when content overflows
- Game needs to progress enough to fill log
- Check if log container has proper height set (600px)
- Browser may hide scrollbar on trackpad/mouse (settings)

**Auto-scroll not working**
- `requestAnimationFrame` ensures smooth scrolling
- User manually scrolling pauses auto-scroll momentarily
- Log container uses `scroll-behavior: smooth` for smooth transitions
- Check browser console for JavaScript errors

---

## Performance Considerations

- **API Calls**: Each snake makes requests independently at its own pace
- **Rendering**: 60fps continuous loop (lightweight, mostly static)
- **Memory**: Game state ~2KB, log grows with turns
- **Network**: Dependent on API latency and response time per model
- **Canvas**: 600×600 pixels, optimized drawing
- **Independent Loops**: Two async loops running simultaneously
- **Recommendations**:
  - No turn delay needed - snakes move at natural model speed
  - Fast models (LLaMA, Mistral) will dominate vs slower ones
  - Move counters clearly show speed differences
  - Memory usage grows with log length (can manually clear if needed)

---

## Security Notes

- **API Keys**: Displayed as password input (bullets), not logged
- **Key Storage**: Only stored in memory (session-based, cleared on refresh)
- **No Data Persistence**: All game data is in-memory only
- **No Encryption**: API calls use HTTPS but key stored in plain text in memory
- **CORS**: Some APIs may require CORS configuration to work from browser
- **Token Factory Integration**: Uses provided credentials for Authentication header

---

## Latest Changes

### v2.3 - Game Log Panel Height Constraint (March 2026)
- **UI Fix**: Game log panel now constrained to match canvas height
  - Added `max-height: 600px` constraint to prevent panel from growing beyond canvas height
  - Maintained `overflow-y: auto` for scrollbar that appears only when needed
  - Panel now maintains proper size alignment with canvas even when empty or with few entries
- **Layout Improvements**:
  - Right panel properly aligned with canvas height (600px)
  - Media queries maintain responsive behavior
  - Game center panel and layout adjusted to maintain proper height constraints
- **Documentation updates**:
  - Updated Game Log Panel dimensions: `max-height: 600px`, `width: 250px`
  - Updated UI layout diagram to reflect height=canvas constraint
  - Maintained note about scrollbar with custom styling

### v2.2 - API Latency Tracking (February 2026)
- **New Feature**: Real-time API latency display in game logs
  - Measures and displays API response time for each LLM call
  - Latency shown in milliseconds (e.g., "423ms", "1567ms")
  - Color-coded latency:
    - Teal: < 500ms (fast response)
    - Yellow: 500-1500ms (medium response)
    - Red: > 1500ms (slow response)
  - Semi-transparent background for better visibility
  - Latency display included even when fallback logic is triggered
- **Function changes**:
  - `getLLMDirection()`: Now returns `{ direction, latency }` object instead of just direction
  - `moveSingleSnake()`: Now accepts `latency` parameter
  - `moveSnakeWithLLM()`: Unpacks latency from result and passes to move function
- **Documentation updates**:
  - Updated Core Features section with latency display information
  - Enhanced Log Entry Format section with latency examples and color coding
  - Updated function signatures in Key Functions section
  - Added latency colors to Color Palette table
  - Updated Color Palette with latency styling definitions

### v2.1 - Model Filter Enhancement (February 2026)
- **New Feature**: Type-to-filter model selection
  - Added search filter inputs above both Player 1 and Player 2 model dropdowns
  - Real-time filtering as user types (case-insensitive)
  - Automatically selects first visible model if current selection is filtered out
  - Styling matches existing design with teal focus accent
- **Documentation updates**:
  - Updated Core Features section to include model filtering
  - Enhanced Setup Screen documentation with filter input details
  - Added Model Selection & Filtering subsection to Key Functions
  - Added Model Filter Input Styling to Visual Design section

### v2.0 - Independent Snake Movement
### Spec Updates
- Added independent snake movement mechanics
- Removed synchronized turn-based gameplay
- Added move counter display in score header
- Updated UI layout with move counter styling
- Documented `player1Moves` and `player2Moves` state fields
- Updated game loop architecture documentation
- Noted turn delay is now unused/may be removed in future

### Code Improvements
- Independent async loops for each snake
- Move counters updated on each snake move
- `moveSnakeWithLLM()` function for independent movement
- `moveSingleSnake()` for per-snake movement logic
- `checkGameOver()` for centralized end-game detection
- Snake death flags (`player1Dead`, `player2Dead`)
- Updated score display to show moves

---

## Version History

### v2.3 - Current (February 2026)
- **New Feature**: Real-time latency meter with statistics
  - Visual bar display showing latency distribution
  - White line marker for median latency position
  - Magenta line marker for p90 latency position
  - Hover tooltip with detailed statistics:
    * Min, Max, Mean, Median, P90, P95, P99 latencies
    * Standard deviation calculation
    * Total sample count
  - Separate meters for each player with sample tracking
  - Ruler scale from 0ms to 3000ms
  - Tick marks (minor every 50ms, major every 500ms)
  - Bar width represents up to 95th percentile for optimal visualization
  - Updates in real-time as API calls are made
  - Resets when game restarts
- New latency tracking functions:
  * `trackLatency()` - Record latency samples
  * `updateLatencyMeter()` - Refresh meter display
  * `updateLatencyBar()` - Update visual bar with markers
  * `updateLatencyStats()` - Update tooltip statistics
  * `calculatePercentile()` - Calculate precise percentile values
  * `resetLatencyTracking()` - Clear latency data
- Global arrays `player1Latencies` and `player2Latencies` for sample storage
- Documentation updates with complete latency meter specifications

### v2.2 - API Latency Tracking
- **New Feature**: API latency tracking
  - Tracks and displays LLM API response time for each move
  - Color-coded latency indicators (teal/yellow/red)
  - Makes model performance differences visible in real-time
- Enhanced `getLLMDirection()` to return latency with direction
- Updated game log display to show latency for each move
- Documentation updates for latency feature

### v2.1 - Model Filter Enhancement
- **New Feature**: Model filter search inputs
  - Type-to-filter functionality for both player model dropdowns
  - Real-time filtering with case-insensitive matching
  - Automatic selection handling when filtering
  - Consistent styling with existing UI
- Updated documentation to reflect filter functionality

### v2.0 - Independent Snake Movement
- **Major Update**: Independent snake movement
  - Snakes move asynchronously based on model response time
  - Faster models move more frequently
  - Move counters show total moves per snake
  - No synchronized turns - continuous gameplay
- Added move tracking UI
- Refactored game loop for independent movement

### v2.4 - Interactive Latency Graph Tooltips (Current)
- **New Feature**: Interactive tooltips on latency time-series graph
  - Displays turn number and exact latency value on mouse hover
  - Faint dashed vertical line highlights hovered position
  - Circle marker indicates precise data point being inspected
  - Crosshair cursor for precise positioning
  - Smart positioning prevents tooltip from going off-screen
- **Enhanced Graph Interaction**:
  - Mouse events (mousemove, mouseleave) on both player graphs
  - Overlay canvas for non-destructive visual indicators
  - Real-time data point detection based on mouse X position
- **New Functions**:
  - `createLatencyTooltip()` - Creates reusable tooltip DOM element
  - `handleLatencyGraphMouseMove()` - Handles hover detection and positioning
  - `redrawGraphWithOverlay()` - Draws indicator line and circle via overlay
  - `handleLatencyGraphMouseLeave()` - Cleans up on mouse exit
  - `hideLatencyTooltip()` - Hides tooltip with smooth transition
- **CSS Updates**:
  - `.latency-graph-tooltip` styling with dark background and teal accent
  - `.latency-graph-overlay` for indicator rendering
  - Crosshair cursor on latency graphs
  - Tooltip transition effects for smooth appearance
- **Refactored Stats Panel**: Cleaner, side-by-side player comparison
  - Red/blue dot indicators next to model names
  - Bordered player cards for visual separation
  - Larger metrics font (length, moves, api calls)
  - Smaller, cleaner current latency display
- **Enhanced Latency Visualization**:
  - Adaptive color-coded bar (green/yellow/red zones)
  - Dynamic markers: white = median, purple = p90
  - Positioned markers update in real-time
  - Min/Med/P90/Max stats displayed in spaced layout
- **Code cleanup**: Removed unused CSS classes and JavaScript functions from previous version

### v2.5 - Debug Mode and Timeout System (Current)
- **Debug Checkbox**: Golden/yellow checkbox to enable console logging
  * Tooltip reminder "Check console logs" when enabled
  * Authorization header masked in logs
  * Timestamped outputs `[HH:MM:SS.mmm]`
  * Request/response correlation with player move numbers
- **Timeout System**: Robust timeout handling for LLM API calls
  * `Promise.race` with 15-second timeout per request (increased from 10s in v2.6)
  * Timeouts count as API failure, 2-second delay before retry
  * ⏱️ Timeout indicators in game log with duration
  * Console warnings when timeout occurs
- **Smart Auto-Scroll**: Intelligent game log scrolling
  * Pauses when user scrolls up to review history
  * Resumes automatically when scrollbar is at/near bottom
  * 50-pixel threshold for "at bottom" detection
- **System Prompt Optimization**: Faster LLM responses
  * Changed temperature from 0.3 to 0 (more deterministic)
  * Stronger "NO thinking" directive for instant responses
  * Kept survival goal in prompt
- **Adaptive max_tokens Strategy**: Intelligent token limit management
  * Starts with conservative `max_tokens=10` for fast responses
  * Automatically increases to 100, then 1000 if responses are cut off
  * Removes max_tokens restriction entirely if still insufficient
  * Independent per-player optimization based on individual model behavior
  * Visual logging in game log when adjustments occur (⚙️ Upping max_tokens: X → Y)
- **Content Stripping**: Automatic cleanup of thinking tags
  * Strips `<thinking>...</thinking>` and similar tags from responses
  * Handles multiple tag types: `</thinking>`, `, <thought>, <reasoning>`
  * Case-insensitive matching with backreferences
- **Move Tracking Updates**: Renamed "turn" to "move" throughout
  * `player1MoveNumber` and `player2MoveNumber` instead of `player1Turn`/`player2Turn`
  * Game log shows "P1 - #43" format instead of "Turn 43: P1"
  * Debug logs show "P1: Move 43" instead of "P1: Turn 43"
  * Tooltip shows "P1 Move: #43" instead of "P1 Turn: #43"
  * Game over shows "P1 Moves: 43" instead of "P1 Turns: 43"
- **Log Format Improvements**: Cleaner move entries
  * Direction arrows match actual movement (↑↓←→)
  * No length shown in logs (only emojis and latency)
  * Format: "P1 - #43: 🔴 → 234ms"
- **New Helper Functions**:
  * `formatTimestamp(date)` - Format timestamps as HH:MM:SS.mmm
  * `toggleDebug()` - Switch debug mode on/off
  * `showDebugTooltip()` - Display tooltip reminder
- **Updated State Fields**:
  * Added `debugMode: boolean` to gameState
  * Added `player1MoveNumber` and `player2MoveNumber` (replaced turn counters)
  - Removed `turn` counter (now using per-player move numbers)

### v2.7 - Security & Performance Optimization (Current)
- **Critical Security Fixes**: XSS vulnerability mitigation
  - Replaced dangerous `innerHTML` usage with safe DOM manipulation in game logs
  - Proper parsing and creation of latency spans to prevent XSS attacks
  - Input validation for API URLs and API keys
  - Bounds checking for `max_tokens` level to prevent overflow
- **Performance Optimizations**:
  - Canvas performance optimization with smart redraw system
  - Added `needsRedraw` flag to prevent unnecessary canvas repainting
  - State tracking to only redraw when game state actually changes
  - Memory leak fixes with proper timeout tracking and cleanup
- **Memory Management**:
  - Implemented circular buffer for latency data (max 1000 samples)
  - Comprehensive resource cleanup function `cleanupAllResources()`
  - Proper tracking of all setTimeout calls for cleanup
  - Abort controller cleanup for pending requests
- **New Features**:
  - Benchmark system with model performance testing (benchmark.js)
  - Speed test button for comparing model response times
  - Benchmark results modal with sortable table display
  - Sort by name and sort by speed functionality
- **API Data Tracking**:
  - Track total bytes sent/received per player for LLM requests
  - Display model names in cleaner format (last segment of model ID)
  - Enhanced error handling with proper JSON parsing and validation
- **Layout Structure Fixes**:
  - Fixed HTML div nesting issues that broke game panel layout
  - Proper game panel structure: fruit legend (left) + canvas (center) + game log (right)
  - Canvas and game log panel heights matched at 600px
  - Responsive breakpoint adjusted to 600px for better mobile support
- **Code Quality Improvements**:
  - Comprehensive validation functions for API inputs
  - Better error handling with meaningful error messages
  - Improved game log display with proper styled latency indicators
  - Fixed JavaScript syntax errors and removed duplicate code blocks
- **New Files**:
  - `benchmark.js`: Complete model performance testing system
  - `CLAUDE.md`: Development guidelines with UI layout preservation rules
- **Documentation Updates**:
  - Added security and performance optimization sections
  - Updated version history with v2.7 changes
  - Documented new benchmark functionality
  - Added development workflow guidelines

### v2.6 - UI Compactness and Enhanced Error Handling (Current)
- **Compact UI Design**: Significant reduction in padding, font sizes, and spacing
  - Smaller, tighter game control buttons (Start Battle, Pause, Reset) in single row
  - Start Battle button always visible, not hidden during gameplay
  - Reduced stats panel padding and font sizes
  - Latency stats now use regular font (not bold) with smaller size
  - Fruit legend displayed in compact, always-visible panel
  - Game log uses compact font sizes for better space utilization
  - Debug checkbox made very compact with minimal padding
- **Timer Repositioning**: Game timer moved to compact display below stats panel
  - Centered position with gradient background
  - Shows elapsed time in MM:SS format
- **Improved Error Handling**: Graceful handling of API errors and timeouts
  - API timeout increased from 10 to 15 seconds
  - Timeouts now count as API failures and increment failure counter
  - 2-second delay before retrying after timeout (prevents rapid-fire retries)
  - Proper handling of 429 rate limit errors and other API errors
  - Validation of API response structure (checks for data.choices array)
  - Pause functionality now aborts outstanding API requests
  - Avoids logging aborted/paused requests to game log
- **Layout Improvements**:
  - Fruit legend, game canvas, and game log vertically aligned
  - Removed "Back to Setup" button (not needed)
  - All game control buttons remain visible during gameplay
  - Debug tooltip now positions at button location
- **Always-Visible Fruit Legend**: Fruit legend displayed on page load
- **Updated State Fields**:
  * Added `player1ApiFailures` and `player2ApiFailures` to track API errors
  * Added API failure indicators in stats panel

### v2.9 - Visibility Radius Configuration (March 2026)
- **New Feature**: Configurable snake vision radius with real-time adjustment
  - Added Options section with visibility radius control (1-30, default 5)
  - Implemented real-time visibility adjustment with validation
  - Updated system prompts to reflect limited visibility with VIEW_RADIUS parameter
  - Added UI styling for options section with compact layout
  - Made VIEW_RADIUS configurable from UI while maintaining safety constraints
- **Enhanced System Prompts**: Updated AI instructions to clearly indicate limited visibility radius
  - Snakes now know their exact vision radius in cells
  - Prompts specify when snakes have full grid visibility (radius=30) vs limited visibility
- **UI Improvements**: Refined options panel layout for better space utilization
  - Restructured visibility radius hint text layout for better readability
  - Unified styling across all option controls for consistent appearance
  - Adjusted spacing and alignment for compact options panel

### v2.8 - Collision Avoidance Toggle (March 2026)
- **New Feature**: Real-time collision avoidance control with toggle switch
  - Added "Collision Avoidance" checkbox in Options section (enabled by default)
  - Real-time toggle: changes take effect immediately without game restart
  - Dual collision control: disables both LLM safe move hints and automatic collision avoidance
  - Add game log entries when collision avoidance is toggled
  - Unify UI styling across all option controls for consistent appearance
- **Enhanced Safety System**: Improved collision detection with configurable behavior
  - Collision avoidance can now be completely disabled for advanced testing
  - LLM safe move hints now tied to same toggle as automatic collision avoidance
  - Visual feedback in game log when collision avoidance is activated/deactivated
- **UI Improvements**: Added shield icon for collision avoidance toggle
  - Consistent styling with other option controls
  - Immediate visual feedback showing toggle state

### v3.1 - Demo Mode and Tournament System (March 2026)
- **New File**: `demo.js` — `DemoMode` class implementing full tournament automation
- **Demo Mode Features**:
  - Automated head-to-head model battles using all loaded models
  - Best-of-three match format; winner determined when a model wins 2 games
  - 3-minute per-game timeout with live countdown in demo panel (turns red at ≤30s)
  - Forfeit logic: if a model fails 3 consecutive API calls it forfeits the series
  - 3-second countdown between games, 10-second countdown between series
  - Match history panel shows recent results (newest first)
  - Leaderboard with wins, losses, games, win%, moves, and max length
  - Leaderboard persisted to `localStorage` across sessions
  - Export leaderboard as `snake-demo-leaderboard.json`
  - Pause/resume fully integrated with existing game pause controls
  - Demo toggle button: "▶️ Start Demo" / "⏹️ Stop Demo"
  - Config sections hidden and demo display shown during active demo
- **Loop Mode** (game.js):
  - `loopMode` flag in `gameState` (disabled by default, checkbox in control bar)
  - 5-second countdown shown on canvas overlay after each game ends
  - `startLoopCountdown()`, `updateLoopCountdownDisplay()`, `stopLoopCountdown()`
  - `finalElapsedTime` field freezes timer display at game-end value
- **Collapsible Panels**: Options and Extra sections start collapsed, toggle with smooth CSS animation
- **Bug Fixes**:
  - Game timer now freezes at end-of-game value (uses `finalElapsedTime`)
  - Model dropdown correctly shows filtered results when typing
  - Console logging gated behind debug mode (reduced log spam)
  - Winner variable properly scoped in `checkGameOver()`
- **Code Quality**:
  - Removed dead code: `SYSTEM_PROMPT2`, `needsRedrawCheck`, `previousGameState`
  - `cleanupResources()` aliased to `cleanupAllResources()`
  - Removed unused `selectedDisplay` parameter from `setupSearchableDropdown()`

### v1.0
- Initial public release
- All features implemented:
  - Two AI snake players
  - Synchronized turn-based movement
  - Wall wrapping
  - 7 fruit types with animations
  - Fruit legend panel
  - Game log with scrollbar
  - Smart AI safety overrides
  - Token Factory branding
  - Modern dark UI

---

## Support & Feedback

### Debugging
If you encounter issues:
1. Open browser Developer Tools (F12)
2. Check **Console** tab for JavaScript errors
3. Check **Network** tab for API calls (responses, status codes)
4. Verify API service is running and accessible
5. Test API with curl or Postman to confirm credentials
6. Watch move counters to see speed differences between models

### Logs
The game logs useful information to browser console:
- Model loading success/failure
- API errors with details
- Turn-by-turn decisions (independent per snake)
- Collision and death events
- Move counts

---

*End of Specification*