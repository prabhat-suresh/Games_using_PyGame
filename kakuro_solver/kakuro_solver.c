#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct cell {
  int vertical_sum;
  int horizontal_sum;
  int val;
} cell;

typedef struct element {
  int x;
  int y;
  int priority;
} element;

int abs(int x){
  if(x<0) return -x;
  return x;
}

int min(int a,int b){
  if(a<b) return a;
  return b;
}

int max(int a,int b){
  if(a<b) return b;
  return a;
}

int cmp(const void *a, const void *b)
{
  return ((element *)a)->priority - ((element *)b)->priority;
}

bool is_move_ok(cell **kakuro, int num_rows, int num_cols, int i, int j,int num) {
  int rowsum=0,rsum=0,colsum=0,csum=0,num_empty_col=0,num_empty_row=0;
  int k;
  bool rowval[9],colval[9];

  for(int p=0;p<9;p++){
    rowval[p]=colval[p]=true;
  }

  for (k = i - 1; k && kakuro[k][j].val != -1; k--) {
    if (num == kakuro[k][j].val)
      return false;
    if(kakuro[k][j].val){
      csum+=kakuro[k][j].val;
      colval[kakuro[k][j].val-1]=false;
    }
    else num_empty_col++;
  }
  colsum=kakuro[k][j].vertical_sum;

  for (k = j - 1; k && kakuro[i][k].val != -1; k--) {
    if (num == kakuro[i][k].val)
      return false;
    if(kakuro[i][k].val){
      rsum+=kakuro[i][k].val;
      rowval[kakuro[i][k].val-1]=false;
    }
    else num_empty_row++;
  }
  rowsum=kakuro[i][k].horizontal_sum;

  for (k = i + 1; k<=num_rows && kakuro[k][j].val != -1; k++) {
    if (num == kakuro[k][j].val)
      return false;
    if(kakuro[k][j].val){
      csum+=kakuro[k][j].val;
      colval[kakuro[k][j].val-1]=false;
    }
    else num_empty_col++;
  }

  for (k = j + 1; k<=num_cols && kakuro[i][k].val != -1; k++) {
    if (num == kakuro[i][k].val)
      return false;
    if(kakuro[i][k].val) {
      rsum+=kakuro[i][k].val;
      rowval[kakuro[i][k].val-1]=false;
    }
    else num_empty_row++;
  }

  int minrsum=0,maxrsum=0,mincsum=0,maxcsum=0,temp=0;
  rowval[num-1]=colval[num-1]=false;

  for(int it=1;it<10 && temp<num_empty_row;it++){
    if(rowval[it-1]){
      minrsum+=it;
      temp++;
    }
  }

  temp=0;
  for(int it=9;it && temp<num_empty_row;it--){
    if(rowval[it-1]){
      maxrsum+=it;
      temp++;
    }
  }

  temp=0;
  for(int it=1;it<10 && temp<num_empty_col;it++){
    if(colval[it-1]){
      mincsum+=it;
      temp++;
    }
  }

  temp=0;
  for(int it=9;it && temp<num_empty_col;it--){
    if(colval[it-1]){
      maxcsum+=it;
      temp++;
    }
  }

  if(rsum+num+minrsum>rowsum || rowsum!=INT_MAX && rsum+num+maxrsum<rowsum) return false;
  if(csum+num+mincsum>colsum || colsum!=INT_MAX && csum+num+maxcsum<colsum) return false;
  return true;
}

bool solve1(cell **kakuro, element *list, int num_rows, int num_cols,int indx) {
  if (indx == num_rows*num_cols) {
    return true;
  }
  int i = list[indx].x;
  int j = list[indx].y;
  if (kakuro[i][j].val == -1) {
    return solve1(kakuro, list, num_rows, num_cols, indx + 1);
  }
  for (int k = 1; k <= 9; k++) {
    if (is_move_ok(kakuro, num_rows, num_cols, i, j, k)) {
      kakuro[i][j].val = k;
      if (solve1(kakuro, list, num_rows, num_cols, indx + 1))
        return true;
      kakuro[i][j].val = 0;
    }
  }
  return false;
}

bool solve2(cell **kakuro, int num_rows, int num_cols,int i, int j) {
  if (i==num_rows && j==num_cols+1) {
    return true;
  }
  if(j==num_cols+1){
    i++;
    j=1;
  }
  if (kakuro[i][j].val == -1) {
    return solve2(kakuro, num_rows, num_cols, i, j+1);
  }
  for (int k = 1; k <= 9; k++) {
    if (is_move_ok(kakuro, num_rows, num_cols, i, j, k)) {
      kakuro[i][j].val = k;
      if (solve2(kakuro, num_rows, num_cols, i, j+1))
        return true;
      kakuro[i][j].val = 0;
    }
  }
  return false;
}

void heuristic(cell **kakuro, int num_rows, int num_cols){
  int sum=kakuro[1][0].horizontal_sum,prev=0;

  // setting the horizontal sum heuristic

  for(int i=1;i<=num_rows;i++){
    for(int j=1;j<=num_cols;j++){
      if(kakuro[i][j].val==-1){
        int num_empty_cells=j-prev-1;
        int h=min(abs(sum-num_empty_cells*(num_empty_cells+1)/2),abs(sum-45+(9-num_empty_cells)*(9-num_empty_cells+1)/2));
        for(int k=prev+1;k<j;k++) kakuro[i][k].horizontal_sum=h;
        prev=j;
        sum=kakuro[i][j].horizontal_sum;
      }
      else if(j==num_cols){
        int num_empty_cells=j-prev;
        int h=min(abs(sum-num_empty_cells*(num_empty_cells+1)/2),abs(sum-45+(9-num_empty_cells)*(9-num_empty_cells+1)/2));
        for(int k=prev+1;k<=j;k++) kakuro[i][k].horizontal_sum=h;
        prev=0;
        if(i!=num_rows) sum=kakuro[i+1][0].horizontal_sum;
      }
    }
  }

  // setting the vertical sum heuristic

  sum=kakuro[0][1].vertical_sum,prev=0;
  for(int j=1;j<=num_cols;j++){
    for(int i=1;i<=num_rows;i++){
      if(kakuro[i][j].val==-1){
        int num_empty_cells=i-prev-1;
        int h=min(abs(sum-num_empty_cells*(num_empty_cells+1)/2),abs(sum-45+(9-num_empty_cells)*(9-num_empty_cells+1)/2));
        for(int k=prev+1;k<i;k++) kakuro[k][j].vertical_sum=h;
        prev=i;
        sum=kakuro[i][j].vertical_sum;
      }
      else if(i==num_rows){
        int num_empty_cells=i-prev;
        int h=min(abs(sum-num_empty_cells*(num_empty_cells+1)/2),abs(sum-45+(9-num_empty_cells)*(9-num_empty_cells+1)/2));
        for(int k=prev+1;k<=i;k++) kakuro[k][j].vertical_sum=h;
        prev=0;
        if(j!=num_cols) sum=kakuro[0][j+1].vertical_sum;
      }
    }
  }
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

  // heuristic(kakuro,num_rows,num_cols);

  /* element list[num_rows*num_cols];
  int indx=0;
  for(int r=1;r<=num_rows;r++){
    for(int c=1;c<=num_cols;c++){
      list[indx].x=r;
      list[indx].y=c;
      if(kakuro[r][c].val==-1) list[indx++].priority=INT_MAX;
      else list[indx++].priority=min(kakuro[r][c].vertical_sum,kakuro[r][c].horizontal_sum);
    }
  }

  qsort(list, num_rows*num_cols, sizeof(element), cmp); */

  solve2(kakuro, num_rows, num_cols, 1, 1);

  for (int i = 1; i <= num_rows; i++) {
    for (int j = 1; j <= num_cols; j++) {
      printf("%d ", kakuro[i][j].val);
    }
    printf("\n");
  }

  return 0;
}
