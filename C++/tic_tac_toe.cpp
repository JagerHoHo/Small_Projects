#include <iostream>

using namespace std;

class Player {
 private:
  enum Mark {
    X = -1,
    O = 1
  };

  Mark mark;

 public:
  Player() {
    srand(time(NULL));
    mark = rand() % 2 ? X : O;
  }

  char get_mark() {
    return (mark == X ? 'X' : 'O');
  }

  void get_next_player() {
    mark = static_cast<Mark>(mark * -1);
  }
};

class Board {
 private:
  char board[3][3];
  Player curr_player;
  bool has_winner = false;

  int get_pos() {
    int pos;
    cout << "Input the place you want to place your mark: ";
    cin >> pos;
    return pos - 1;
  }

  bool is_empty(int pos) {
    char mark = board[pos / 3][pos % 3];
    return mark != 'X' && mark != 'O';
  }

  void print() {
    for (const auto& row : board) {
      for (const auto& item : row) cout << item << " ";
      cout << '\n';
    }
  }

  bool has_horizontal_winner(int pos) {
    int row = pos / 3;
    int col = pos % 3;
    int neighbor_pos_1 = 1;
    int neighbor_pos_2 = 2;
    char mark = board[row][col];
    switch (col) {
      case 1:
        neighbor_pos_1--;
        break;
      case 2:
        neighbor_pos_1--;
        neighbor_pos_2--;
        break;
    }
    bool found = board[row][neighbor_pos_1] == mark && board[row][neighbor_pos_2] == mark;
    if (found) cout << "\n\nThe marks on row " << row + 1 << " are connected horizontally.\nThe winner is " << mark << '\n';
    return found;
  }

  bool has_vertical_winner(int pos) {
    int row = pos / 3;
    int col = pos % 3;
    int neighbor_pos_1 = 1;
    int neighbor_pos_2 = 2;
    char mark = board[row][col];
    switch (row) {
      case 1:
        neighbor_pos_1--;
        break;
      case 2:
        neighbor_pos_1--;
        neighbor_pos_2--;
        break;
    }
    bool found = board[neighbor_pos_1][col] == mark && board[neighbor_pos_2][col] == mark;
    if (found) cout << "\n\nThe marks on col " << col + 1 << " are connected vertically.\nThe winner is " << mark << '\n';
    return found;
  }

  bool has_diagonal_winner(int pos) {
    int row = pos / 3;
    int col = pos % 3;
    char mark = board[row][col];
    switch (pos) {
      case 0:
      case 8:
        if (board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
          cout << "\n\nThe marks are connected from top left to bottom right.\nThe winner is " << mark << '\n';
          return true;
        }
      case 2:
      case 6:
        if (board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
          cout << "\n\nThe marks are connected from top right to bottom left.\nThe winner is " << mark << '\n';
          return true;
        }
      case 4:
        bool right_to_left = board[0][2] == board[1][1] && board[1][1] == board[2][0];
        bool left_to_right = board[0][0] == board[1][1] && board[1][1] == board[2][2];
        if (right_to_left) {
          cout << "\n\nThe marks are connected from top right to bottom left.\nThe winner is " << mark << '\n';
          return true;
        }
        if (left_to_right) {
          cout << "\n\nThe marks are connected from top left to bottom right.\nThe winner is " << mark << '\n';
          return true;
        }
    }
    return false;
  }

  bool found_winner(int pos) {
    return has_horizontal_winner(pos) || has_vertical_winner(pos) || has_diagonal_winner(pos);
  }

  bool draw() {
    for (int i = 0; i < 9; i++)
      if (is_empty(i)) return false;
    cout << "\n\nNo winner this match.\n";
    return true;
  }

  void play_turn() {
    cout << "The current player is " << curr_player.get_mark() << '\n';
    int pos = get_pos();
    if (pos < 9 && pos >= 0 && is_empty(pos)) {
      board[pos / 3][pos % 3] = curr_player.get_mark();
      curr_player.get_next_player();
      has_winner = found_winner(pos) || draw();
    } else
      cout << "\nInvalid Move!\n\n";
  }

 public:
  Board() {
    for (int i = 0; i < 9; i++)
      board[i / 3][i % 3] = to_string(i + 1)[0];
  }

  void run() {
    print();
    while (!has_winner) {
      play_turn();
      print();
    }
  }
};

int main() {
  Board board;
  board.run();
}