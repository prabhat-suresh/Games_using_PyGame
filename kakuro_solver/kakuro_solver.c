#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct cell {
  int vertical_sum;
  int horizontal_sum;
  int val;
} cell;

bool is_move_ok(cell **kakuro, int num_rows, int num_cols, int i, int j,int num) {
  int minrsum=0,maxrsum=0,mincsum=0,maxcsum=0,temp=0,num_empty_col=0,num_empty_row=0;
  bool rowval[10],colval[10];

  for(int p=1;p<10;p++) rowval[p]=colval[p]=true;

  rowval[num]=colval[num]=rowval[0]=colval[0]=false;

  for (int k = i - 1; k && kakuro[k][j].val != -1; k--) {
    if(colval[kakuro[k][j].val]) colval[kakuro[k][j].val]=false;
    else return false;
  }

  for (int k = j - 1; k && kakuro[i][k].val != -1; k--) {
    if(rowval[kakuro[i][k].val]) rowval[kakuro[i][k].val]=false;
    else return false;
  }

  for (; i+1+num_empty_col<=num_rows && kakuro[i+1+num_empty_col][j].val != -1; num_empty_col++) ;

  for (; j+1+num_empty_row<=num_cols && kakuro[i][j+1+num_empty_row].val != -1; num_empty_row++) ;

  for(int it=1;it<10 && temp<num_empty_row;it++){
    if(rowval[it]){
      minrsum+=it;
      temp++;
    }
  }

  temp=0;
  for(int it=9;it && temp<num_empty_row;it--){
    if(rowval[it]){
      maxrsum+=it;
      temp++;
    }
  }

  temp=0;
  for(int it=1;it<10 && temp<num_empty_col;it++){
    if(colval[it]){
      mincsum+=it;
      temp++;
    }
  }

  temp=0;
  for(int it=9;it && temp<num_empty_col;it--){
    if(colval[it]){
      maxcsum+=it;
      temp++;
    }
  }

  if(num+minrsum>kakuro[i][j-1].horizontal_sum|| kakuro[i][j-1].horizontal_sum<1000 && num+maxrsum<kakuro[i][j-1].horizontal_sum) return false;
  if(num+mincsum>kakuro[i-1][j].vertical_sum|| kakuro[i-1][j].vertical_sum<1000 && num+maxcsum<kakuro[i-1][j].vertical_sum) return false;
  return true;
}

bool solve(cell **kakuro, int num_rows, int num_cols,int i, int j) {
  if (i==num_rows && j==num_cols+1) {
    return true;
  }
  if(j==num_cols+1){
    i++;
    j=1;
  }
  if (kakuro[i][j].val == -1) {
    return solve(kakuro, num_rows, num_cols, i, j+1);
  }
  for (int k = 1; k <= 9; k++) {
    if (is_move_ok(kakuro, num_rows, num_cols, i, j, k)) {
      kakuro[i][j].val = k;
      kakuro[i][j].vertical_sum=kakuro[i-1][j].vertical_sum-k;
      kakuro[i][j].horizontal_sum=kakuro[i][j-1].horizontal_sum-k;
      if (solve(kakuro, num_rows, num_cols, i, j+1))
        return true;
      kakuro[i][j].val = 0;
    }
  }
  return false;
}

int main() {
  int num_rows, num_cols;
  printf("Enter the number of rows and columns");
  scanf("%d%d", &num_rows, &num_cols);

  // allocating the kakuro grid
  cell **kakuro = malloc((num_rows + 1) * sizeof(cell *));
  for (size_t i = 0; i <= num_rows; i++) {
    kakuro[i] = malloc((num_cols + 1) * sizeof(cell));
  }

  printf("Enter -1 for black triangles, 0 for white triangles, and value of "
         "sum for vertical_sum triangles and horizontal_sum triangles");
  for (int i = 1; i <= num_rows; i++) {
    for (int j = 1; j <= num_cols; j++) {
      scanf("%d%d", &(kakuro[i][j].vertical_sum),
            &(kakuro[i][j].horizontal_sum));
      kakuro[i][j].val = 0;
      if (kakuro[i][j].vertical_sum == -1) {
        kakuro[i][j].vertical_sum = INT_MAX;
      }
      if (kakuro[i][j].horizontal_sum == -1) {
        kakuro[i][j].horizontal_sum = INT_MAX;
      }
      if (kakuro[i][j].horizontal_sum) {
        kakuro[i][j].val = -1;
      }
    }
  }

  for (int i = 0; i <= num_rows; i++) {
    kakuro[i][0].val = -1;
    kakuro[i][0].horizontal_sum = INT_MAX;
    kakuro[i][0].vertical_sum = INT_MAX;
  }

  for (int i = 1; i <= num_cols; i++) {
    kakuro[0][i].val = -1;
    kakuro[0][i].horizontal_sum = INT_MAX;
    kakuro[0][i].vertical_sum = INT_MAX;
  }

  solve(kakuro, num_rows, num_cols, 1, 1);

  for (int i = 1; i <= num_rows; i++) {
    for (int j = 1; j <= num_cols; j++) {
      printf("%d ", kakuro[i][j].val);
    }
    printf("\n");
  }

  return 0;
}
