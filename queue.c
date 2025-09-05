#include <stdio.h>
#include <stdlib.h>

struct Queue {
    int size;
    int front;
    int rear;
    int *Q;
};

// Function to create queue
void create(struct Queue *q, int size) {
    q->size = size;
    q->front = q->rear = -1;
    q->Q = (int *)malloc(q->size * sizeof(int));
}

// Function to insert element
void enqueue(struct Queue *q, int x) {
    if (q->rear == q->size - 1)
        printf("Queue is Full\n");
    else {
        q->rear++;
        q->Q[q->rear] = x;
    }
}

// Function to delete element
int dequeue(struct Queue *q) {
    int x = -1;
    if (q->front == q->rear)
        printf("Queue is Empty\n");
    else {
        q->front++;
        x = q->Q[q->front];
    }
    return x;
}

// Function to display elements
void Display(struct Queue q) {
    for (int i = q.front + 1; i <= q.rear; i++)
        printf("%d ", q.Q[i]);
    printf("\n");
}

int main() {
    struct Queue q;
    create(&q, 5);

    enqueue(&q, 10);
    enqueue(&q, 20);
    enqueue(&q, 30);
    enqueue(&q, 40);
    enqueue(&q, 50);

    Display(q);

    printf("Deleted: %d\n", dequeue(&q));
    printf("Deleted: %d\n", dequeue(&q));

    Display(q);

    return 0;
}