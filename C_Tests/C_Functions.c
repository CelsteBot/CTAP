#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int MyLev(char[], char[], int);
int GetIndexOf2DArray(int, int, int);
void PrintMatrix(int[], int, int);

#define MAX_STRING_SIZE 128
#define DISTANCE_SIZE [128 * 128]

int GetIndexOf2DArray(int x, int y, int xMax){
    return y * xMax + x;
}

void PrintMatrix(int matrix[], int xMax, int yMax){
    char minfoToStr[3];
    for (int y = 0; y < yMax; y++){
        for (int x = 0; x < xMax; x++){
            int i = GetIndexOf2DArray(x, y, xMax);
            sprintf(minfoToStr, "%d", matrix[i]);
            printf("%s  ", minfoToStr);
        }
        printf("\n");
    }
}

int MyLev(char token1[], char token2[], int threshold){
    //Initialize matrix info
    const int xMax = strlen(token1) + 1;
    const int yMax = strlen(token2) + 1;
    const int matrixSize = xMax * yMax;
    int distances DISTANCE_SIZE = {0};

    if (abs(xMax - yMax) > threshold) { return 0; }

    // Initialize Debug info
    char xToStr[3];
    char yToStr[3];
    char iToStr[5];

    // sprintf(xToStr, "%d", xMax);
    // sprintf(yToStr, "%d", yMax);
    // printf("Str 1 length: %s, Str 1: %s\n", xToStr, token1);
    // printf("Str 2 length: %s, Str 2: %s\n", yToStr, token2);

    // Set default values of the Matrix
    for (int x = 1; x < xMax; x++){
        int i = GetIndexOf2DArray(x, 0, xMax);
        distances[i] = x;
    }
    for (int y = 1; y < yMax; y++){
        int i = GetIndexOf2DArray(0, y, xMax);
        distances[i] = y;
    }

    // iterate through the matrix
    for (int x = 1; x < xMax; x++){
        int minOfRow = 1000;
        for (int y = 1; y < yMax; y++){
            // Check if letters are the same
            int i = GetIndexOf2DArray(x, y, xMax);
            int di = GetIndexOf2DArray(x-1, y-1, xMax);
            if (token1[x-1] == token2[y-1]){
                distances[i] = distances[di];
            }else{
                // Get values of the 2x2 matrix
                int xi = GetIndexOf2DArray(x-1, y, xMax);
                int yi = GetIndexOf2DArray(x, y-1, xMax);

                int a = distances[yi];
                int b = distances[xi];
                int c = distances[di];

                // Find minimum value in the 2x2 matrix
                if (a <= b && a <= c ){distances[i] = a + 1; }
                else if (b <= a && b <= c ){distances[i] = b + 1; }
                else {distances[i] = c + 1; }
            }

            //Check if this is the minimum of the row
            if (distances[i] < minOfRow){
                minOfRow = distances[i];
            }
        }
        // Check if Failed mid row
        if (minOfRow > threshold){
            return 0;
        }
    }

    return 1;
}