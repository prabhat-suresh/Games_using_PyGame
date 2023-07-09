#include <iostream>
#include <string>
#include <vector>
using namespace std;

bool move_is_ok(vector<string> &puzzle, int i, int j, char num) {
  for (int k = 0; k < 9; k++) {
    if (puzzle[i][k] == num) {
      return false;
    }
  }
  for (int k = 0; k < 9; k++) {
    if (puzzle[k][j] == num) {
      return false;
    }
  }
  for (int k = (i / 3) * 3; k < (i / 3) * 3 + 3; k++) {
    for (int l = (j / 3) * 3; l < (j / 3) * 3 + 3; l++) {
      if (puzzle[k][l] == num) {
        return false;
      }
    }
  }
  return true;
}

void backtrack(vector<string> &puzzle, bool *solved, int lasti, int lastj) {
  for (int i = 0; i < 9; i++) {
    for (int j = 0; j < 9; j++) {
      if (puzzle[i][j] == '0') {
        for (char c = '1'; c <= '9'; c++) {
          if (move_is_ok(puzzle, i, j, c)) {
            puzzle[i][j] = c;
            if (i == lasti && j == lastj) {
              *solved = true;
              return;
            }
            backtrack(puzzle, solved, lasti, lastj);
            if (*solved) {
              return;
            }
            puzzle[i][j] = '0';
          }
        }
        return;
      }
    }
  }
}

int main() {
  vector<string> puzzle(9);
  cout << "Enter sudoku puzzle as 9 strings with blanks as zeroes";
  for (int i = 0; i < 9; i++) {
    cin >> puzzle[i];
  }
  int lasti = 0, lastj = 0;
  for (int i = 0; i < 9; i++) {
    for (int j = 0; j < 9; j++) {
      if (puzzle[i][j] == '0') {
        lasti = i;
        lastj = j;
      }
    }
  }
  bool solved = false;
  backtrack(puzzle, &solved, lasti, lastj);
  for (int i = 0; i < 9; i++) {
    cout << puzzle[i] << '\n';
  }
  return 0;
}
