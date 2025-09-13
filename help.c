#include <stdio.h>
#include <stdlib.h>

// 1. Concatenate Doubly Linked Lists
struct DNode {
    int data;
    struct DNode* prev;
    struct DNode* next;
};

void concatenateDLL() {
    struct DNode *head1 = (struct DNode*)malloc(sizeof(struct DNode));
    head1->data = 10;
    head1->prev = NULL;
    head1->next = NULL;
    struct DNode* temp = head1;

    int arr1[] = {20, 30};
    for (int i = 0; i < 2; i++) {
        struct DNode* node = (struct DNode*)malloc(sizeof(struct DNode));
        node->data = arr1[i];
        node->prev = temp;
        node->next = NULL;
        temp->next = node;
        temp = node;
    }

    struct DNode *head2 = (struct DNode*)malloc(sizeof(struct DNode));
    head2->data = 40;
    head2->prev = NULL;
    head2->next = NULL;
    temp = head2;

    int arr2[] = {50, 60};
    for (int i = 0; i < 2; i++) {
        struct DNode* node = (struct DNode*)malloc(sizeof(struct DNode));
        node->data = arr2[i];
        node->prev = temp;
        node->next = NULL;
        temp->next = node;
        temp = node;
    }

    struct DNode* tail = head1;
    while (tail->next) tail = tail->next;
    tail->next = head2;
    head2->prev = tail;

    printf("Concatenated: ");
    temp = head1;
    while (temp) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}


// 2. Tower of Hanoi
void towerOfHanoi(int n, char from, char to, char aux) {
    if (n == 0) return;
    towerOfHanoi(n-1, from, aux, to);
    printf("Move disk %d from %c to %c\n", n, from, to);
    towerOfHanoi(n-1, aux, to, from);
}

void towerOfHanoiMain() {
    int n = 4;
    towerOfHanoi(n, 'X', 'Z', 'Y');
}


// 3. Array Operations with Min-Max Removal
void arrayMinMax() {
    int arr[5] = {8, 2, 14, 6, 10};
    int n = 5, k = 3;

    for (int step = 0; step < k; step++) {
        int min = arr[0], max = arr[0], minIdx = 0, maxIdx = 0;
        for (int i = 1; i < n; i++) {
            if (arr[i] < min) { min = arr[i]; minIdx = i; }
            if (arr[i] > max) { max = arr[i]; maxIdx = i; }
        }

        for (int i = minIdx; i < n-1; i++) arr[i] = arr[i+1];
        n--;
        if (maxIdx > minIdx) maxIdx--;
        for (int i = maxIdx; i < n-1; i++) arr[i] = arr[i+1];
        n--;

        arr[n++] = max - min;
    }

    int sum = 0;
    for (int i = 0; i < n; i++) sum += arr[i];
    printf("Final sum = %d\n", sum);
}


// 4. Petrol Pump Circular Tour
void petrolPumpTour() {
    int petrol[] = {5, 8, 2, 6};
    int dist[]   = {6, 5, 4, 5};
    int n = 4;

    int start = 0, balance = 0, deficit = 0;
    for (int i = 0; i < n; i++) {
        balance += petrol[i] - dist[i];
        if (balance < 0) {
            start = i + 1;
            deficit += balance;
            balance = 0;
        }
    }

    if (balance + deficit >= 0) {
        printf("Start index %d\n", start);
    } else {
        printf("No possible tour\n");
    }
}


// 5. Linear Search
void linearSearch() {
    int arr[] = {15, 25, 35, 45, 55};
    int n = 5, key = 45;

    int comparisons = 0, found = -1;
    for (int i = 0; i < n; i++) {
        comparisons++;
        if (arr[i] == key) {
            found = i;
            break;
        }
    }

    if (found != -1) {
        printf("Found %d at index %d\n", key, found);
    } else {
        printf("Not found\n");
    }
    printf("Comparisons = %d\n", comparisons);
}


// 6. Binary Search
void binarySearch() {
    int arr[] = {3, 9, 15, 21, 27, 33};
    int n = 6, key = 15;

    int low = 0, high = n-1, found = -1;
    while (low <= high) {
        int mid = (low + high) / 2;
        if (arr[mid] == key) { found = mid; break; }
        else if (arr[mid] < key) low = mid + 1;
        else high = mid - 1;
    }

    if (found != -1) printf("%d found at index %d\n", key, found);
    else printf("Not found\n");
}


// 7. Interpolation Search
int interpolationSearch(int arr[], int n, int x) {
    int low = 0, high = n - 1;
    while (low <= high && arr[low] <= x && x <= arr[high]) {
        if (low == high) return (arr[low] == x) ? low : -1;
        int pos = low + ((double)(high - low) / (arr[high] - arr[low])) * (x - arr[low]);
        if (arr[pos] == x) return pos;
        if (arr[pos] < x) low = pos + 1;
        else high = pos - 1;
    }
    return -1;
}

void interpolationSearchMain() {
    int arr[] = {12, 24, 36, 48, 60, 72};
    int n = 6, key = 48;
    int idx = interpolationSearch(arr, n, key);
    if (idx != -1) printf("%d at index %d\n", key, idx);
    else printf("Not found\n");
}


// 8. Bubble Sort
void bubbleSort() {
    int arr[] = {42, 19, 73, 8, 56};
    int n = 5, swaps = 0;

    printf("Before: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                int tmp = arr[j]; arr[j] = arr[j+1]; arr[j+1] = tmp;
                swaps++;
            }
        }
    }

    printf("After: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\nSwaps = %d\n", swaps);
}


// 9. Insertion Sort
void insertionSort() {
    int arr[] = {18, 12, 25, 7, 3};
    int n = 5;

    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j+1] = arr[j];
            j--;
        }
        arr[j+1] = key;

        printf("Step %d: ", i);
        for (int k = 0; k < n; k++) printf("%d ", arr[k]);
        printf("\n");
    }
}


// 10. Selection Sort
void selectionSort() {
    int arr[] = {29, 10, 14, 37, 13};
    int n = 5, comps = 0, swaps = 0;

    for (int i = 0; i < n-1; i++) {
        int minIdx = i;
        for (int j = i+1; j < n; j++) {
            comps++;
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        if (minIdx != i) {
            int tmp = arr[i]; arr[i] = arr[minIdx]; arr[minIdx] = tmp;
            swaps++;
        }
    }

    printf("Sorted: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\nComparisons = %d, Swaps = %d\n", comps, swaps);
}


// Main
int main() {
    getchar();

    printf("--- 1. Concatenate Doubly Linked Lists ---\n");
    concatenateDLL();

    printf("--- 2. Tower of Hanoi ---\n");
    towerOfHanoiMain();

    printf("--- 3. Array Operations with Min-Max Removal ---\n");
    arrayMinMax();

    printf("--- 4. Petrol Pump Circular Tour ---\n");
    petrolPumpTour();

    printf("--- 5. Linear Search ---\n");
    linearSearch();

    printf("--- 6. Binary Search ---\n");
    binarySearch();

    printf("--- 7. Interpolation Search ---\n");
    interpolationSearchMain();

    printf("--- 8. Bubble Sort ---\n");
    bubbleSort();

    printf("--- 9. Insertion Sort ---\n");
    insertionSort();

    printf("--- 10. Selection Sort ---\n");
    selectionSort();

    return 0;
}
