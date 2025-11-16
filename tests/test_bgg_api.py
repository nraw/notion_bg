from notion_bg.bgg_api import *


def test_bgg_api():
    import sys
    import os

    if not os.environ.get('BGG_API_KEY'):
        print('⚠ BGG_API_KEY not set - skipping API test')
        sys.exit(0)

    print('Testing BGG API client with authentication...')

    # Test 1: Create client
    try:
        bgg = BGGClient()
        print('✓ Client creation successful')
    except Exception as e:
        print(f'✗ Client creation failed: {e}')
        sys.exit(1)

    # Test 2: Get game by ID
    try:
        game = bgg.game(game_id=174430)  # Gloomhaven
        print(f'✓ Get game by ID successful: {game.name}')
        print(f'  - ID: {game.id}')
        print(f'  - Players: {game.min_players}-{game.max_players}')
        print(f'  - Rating: {game.rating_average}')
    except Exception as e:
        print(f'✗ Get game by ID failed: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print('')
    print('✓ All basic tests passed!')
