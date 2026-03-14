# Grupo 54:
# 109635 Rafael Freitas
# 109485 Gonçalo Nogueira

from sys import stdin
from search import Problem, Node, depth_first_tree_search

pieces = {
    "L": [
        [ ( 0, 0 ), ( -1, 0 ), ( -2, 0 ), ( 0, 1 ) ],
        [ ( 0, 0 ), ( -1, 0 ), ( -2, 0 ), ( 0, -1 ) ],
        [ ( 0, 0 ), ( 1, 0 ), ( 2, 0 ), ( 0, 1 ) ],
        [ ( 0, 0 ), ( 1, 0 ), ( 2, 0 ), ( 0, -1 ) ],
        [ ( 0, 0 ), ( 0, -1 ), ( 0, -2 ), ( 1, 0 ) ],
        [ ( 0, 0 ), ( 0, -1 ), ( 0, -2 ), ( -1, 0 ) ],
        [ ( 0, 0 ), ( 0, 1 ), ( 0, 2 ), ( 1, 0 ) ],
        [ ( 0, 0 ), ( 0, 1 ), ( 0, 2 ), ( -1, 0 ) ]
    ],

    "I": [
        [ ( 0, 0 ), ( 1, 0 ), ( 2, 0 ), ( 3, 0 ) ],
        [ ( 0, 0 ), ( 0, 1 ), ( 0, 2 ), ( 0, 3 ) ]
    ],

    "T": [
        [ ( 0, 0 ), ( 0, 1 ), ( 0, -1 ), ( 1, 0 ) ],
        [ ( 0, 0 ), ( 0, 1 ), ( 0, -1 ), ( -1, 0 ) ],
        [ ( 0, 0 ), ( -1, 0 ), ( 1, 0 ), ( 0, 1 ) ],
        [ ( 0, 0 ), ( -1, 0 ), ( 1, 0 ), ( 0, -1 ) ]
    ],

    "S": [
        [ ( 0, 0 ), ( 0, -1 ), ( -1, 0 ), ( -1, 1 ) ],
        [ ( 0, 0 ), ( 0, 1 ), ( -1, 0 ), ( -1, -1 ) ],
        [ ( 0, 0 ), ( 1, 0 ), ( 0, -1 ), ( -1, -1 ) ],
        [ ( 0, 0 ), ( 1, 0 ), ( 0, 1 ), ( -1, 1 ) ]
    ]
}

class NuruominoState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NuruominoState.state_id

        NuruominoState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class Board:
    def __init__( self, n:int ):
        if n > 0:
            self.matrix = [ [ [ 0, None ] for _ in range( n ) ] for _ in range( n ) ]
            self.regions = {}
            self.actions = {}
            self.last_action = None
            self.regions_adjacent = {}

    def __str__( self ):
        return "\n".join( "\t".join( str( cell[ 1 ] or cell[ 0 ] ) for cell in row ) for row in self.matrix ) + "\n"

    def clone( self ):
        board = Board( 0 )

        board.matrix = [ [ [ region, piece ] for [ region, piece ] in row ] for row in self.matrix ]

        board.regions = {}
        for region, ( piece, area ) in self.regions.items():
            board.regions[ region ] = [ piece, [ position for position in area ] ]

        board.actions = {}
        for region, actions in self.actions.items():
            board.actions[ region ] = [ action for action in actions ]

        board.regions_adjacent = self.regions_adjacent

        board.last_action = self.last_action

        return board

    def adjacent_regions(self, region:int) -> list:
        regions = set()

        for (y,x) in self.regions[ region ][ 1 ]:
            for (w,z) in self.adjacent_positions( y, x ):
                r = self.matrix[ w ][ z ][ 0 ]

                if r != region:
                    regions.add( r )

        return list( regions )
    
    def all_adjacent_regions(self) -> dict:
        for region in self.regions:
            self.regions_adjacent[ region ] = self.adjacent_regions( region )

    def adjacent_positions( self, row : int, col : int ) -> list:
        n = len( self.matrix )

        return [ ( row + a, col + b ) for ( a, b ) in [ ( - 1, - 1 ), ( - 1, 0 ), ( 0, - 1 ), ( - 1, 1 ), ( 1, - 1 ), ( 1, 1 ), ( 1, 0 ), ( 0, 1 ) ] if 0 <= row + a < n and 0 <= col + b < n ]

    def place_piece( self, region : int, row : int, col : int, piece : str, rotation : int ) -> None:
        self.regions[ region ][ 0 ] = piece
        self.last_action = region
        if region in self.actions:
            del self.actions[ region ]
        for ( a, b ) in pieces[ piece ][ rotation ]:
            self.matrix[ row + a ][ col + b ][ 1 ] = piece

    def place_suitable_piece( self, region : int, area : list ) -> None:
        for ( y, x ) in area:
            for piece, rotations in pieces.items():
                for rotation, positions in enumerate( rotations ):
                    if all( ( y + pos[ 0 ], x + pos[ 1 ] ) in area for pos in positions ):
                        self.place_piece( region, y, x, piece, rotation )
                                
                        return

    def forms_square( self, r_p: int, c_p : int, piece : str, rotation : int ) -> bool:
        n = len( self.matrix )
        placing = { ( r_p + a, c_p + b ) for ( a, b ) in pieces[ piece ][ rotation ] }

        for ( row, col ) in placing:
            possible_squares = (
                ( ( row, col + 1 ), ( row + 1, col ), ( row + 1, col + 1 ) ),
                ( ( row, col - 1 ), ( row + 1, col - 1 ), ( row + 1, col ) ),
                ( ( row - 1, col ), ( row - 1, col + 1 ), ( row, col + 1 ) ),
                ( ( row - 1, col - 1 ), ( row - 1, col ), ( row, col - 1 ) ),
            )

            for square in possible_squares:
                if all( 0 <= r < n and 0 <= c < n and self.matrix[ r ][ c ][ 1 ] is not None or ( r, c ) in placing for ( r, c ) in square ):
                    return True

        return False
        
    def orthogonally_equal_pieces( self, row : int, col : int, piece : str, rotation : int ) -> bool:
        n = len( self.matrix )
        placing = ( ( row + a, col + b ) for ( a, b ) in pieces[ piece ][ rotation ] )
        region = self.matrix[ row ][ col ][ 0 ]

        for ( row_d, col_d ) in placing:
            for ( a, b ) in ( 0, 1 ), ( 0, -1 ), ( -1, 0 ), ( 1, 0 ):
                adjacent_row = row_d + a
                adjacent_col = col_d + b

                if 0 <= adjacent_row < n and 0 <= adjacent_col < n:
                    adjacent_piece = self.matrix[ adjacent_row ][ adjacent_col ][ 1 ]
                    adjacent_region = self.matrix[ adjacent_row ][ adjacent_col ][ 0 ]

                    if adjacent_piece == piece and adjacent_region != region:
                        return True
                    
        return False

    def disconnected( self ,region : int, row : int, col : int, piece : str, rotation : int ) -> bool:
        visited = set()
        placing = tuple((row + r_off, col + c_off) for r_off, c_off in pieces[piece][rotation])

        stack = [region]
        
        n = len(self.matrix)
        
        num_total_regions = len(self.regions)

        while stack:
            current_region = stack.pop()

            if current_region in visited:
                continue
            visited.add(current_region)

            if len(visited) == num_total_regions:
                return False

            current_region_piece = self.regions[current_region][0]
            
            if current_region == region:
                area = placing
            else:
                area = self.regions[current_region][1]

            for r, c in area:
                if not (current_region_piece is None or \
                        self.matrix[r][c][1]):
                    continue

                for dr, dc in ((0, 1), (0, -1), (-1, 0), (1, 0)):
                    nr, nc = r + dr, c + dc

                    if not (0 <= nr < n and 0 <= nc < n):
                        continue

                    adjacent_region = self.matrix[nr][nc][0]
                    
                    if adjacent_region == current_region or adjacent_region in visited:
                        continue

                    if self.regions[adjacent_region][0] is None or self.matrix[nr][nc][1]:
                        stack.append(adjacent_region)
                
        return len( visited ) != num_total_regions

    def orthogonally_connected( self ) -> bool:
        visited = set()
        stack = []
        regions = len( self.regions )

        stack.append( next( iter( self.regions ) ) )
        
        while stack:
            current_region = stack.pop()
            if current_region not in visited:
                visited.add(current_region)
                area = self.regions[current_region][1]
                for (y, x) in area:
                    if self.matrix[y][x][1]:
                        for ( a, b ) in (0,1 ), (0,-1 ), (-1,0), (1,0):
                            if 0 <= y + a < len(self.matrix) and 0 <= x + b < len(self.matrix):
                                adjacent_region = self.matrix[y + a][x + b][0]
                                if adjacent_region != current_region and self.matrix[y + a][x + b][1]:
                                    stack.append(adjacent_region)

            if len( visited ) == regions:
                break

        return len( visited ) == regions

    def all_actions( self ):
        actions = {}

        for region, ( piece, area ) in self.regions.items():
            if piece == None:
                for ( row, col ) in area:
                    for p in ( "I", "T", "S", "L" ):
                        for rotation, positions in enumerate( pieces[ p ] ):
                            if all( ( row + pos[ 0 ], col + pos[ 1 ] ) in area for pos in positions ):
                                if not self.forms_square( row, col, p, rotation) and not self.orthogonally_equal_pieces( row, col, p, rotation ) and not self.disconnected( region, row, col, p, rotation ):
                                    if region not in actions:
                                        actions[ region ] = [ ( region, row, col, p, rotation ) ]
                                    else:
                                        actions[ region ].append( ( region, row, col, p, rotation ) )
        self.actions = actions                   

    @staticmethod
    def parse_instance():
        board = None

        for y, line in enumerate( stdin.readlines() ):
            line = line.split( '\t' )

            if board == None:
                board = Board( len( line ) )

            for x, region in enumerate( line ):
                region = int( region )

                board.matrix[ y ][ x ][ 0 ] = region

                if region in board.regions:
                    board.regions[ region ][ 1 ].append( ( y, x ) )
                else:
                    board.regions[ region ] = [ None, [ ( y, x ) ] ]

        for region, ( _, area ) in board.regions.items():
            if len( area ) == 4:
                board.place_suitable_piece( region, area )

        board.all_adjacent_regions()
        board.all_actions()

        return board 

class Nuruomino(Problem):
    def __init__(self, board: Board):
        super().__init__( NuruominoState( board ) )

    def actions(self, state: NuruominoState):
        actions = state.board.actions

        if state.board.last_action is not None: 
            region = state.board.last_action
            adjacent_regions = state.board.regions_adjacent[ region ]
            for region in adjacent_regions:
                if region not in actions:
                    continue
                else:
                    actions[ region ] = [ ( region, row, col, p, rotation ) for ( region, row, col, p, rotation ) in actions[ region ] if
                        not (
                            state.board.forms_square( row, col, p, rotation)
                            or state.board.orthogonally_equal_pieces( row, col, p, rotation )
                            or state.board.disconnected( region, row, col, p, rotation )
                        )
                    ]

                    if len( actions[ region ] ) == 0:
                        del actions[ region ]

        actions_len = len( actions )
          
        if not actions_len or actions_len != sum( region[ 0 ] is None for region in state.board.regions.values() ):
            return []
        
        min_actions = min(len(actions[region]) for region in actions.keys())

        regions_with_min_actions = [region for region in actions.keys() 
                                if len(actions[region]) == min_actions]
        
        max_adjacencies_region = max(regions_with_min_actions, 
                                    key=lambda region: len(state.board.regions_adjacent[region]))
        
        return actions[max_adjacencies_region]

    def result(self, state: NuruominoState, action ):
        new_state = NuruominoState( state.board.clone() )
        new_state.board.place_piece( * action )

        return new_state

    def goal_test(self, state: NuruominoState):
        return len( state.board.actions ) == 0 and state.board.orthogonally_connected()

print( depth_first_tree_search( Nuruomino( Board.parse_instance() ) ).state.board )