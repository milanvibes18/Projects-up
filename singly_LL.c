#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

struct Node {
    int data;
    struct Node *next;
} *first = NULL, *second = NULL, *third = NULL;

struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void create(int A[], int n) {
    int i;
    struct Node *t, *last;
    first = (struct Node*)malloc(sizeof(struct Node));
    first->data = A[0];
    first->next = NULL;
    last = first;

    for(i = 1; i < n; i++) {
        t = createNode(A[i]);
        last->next = t;
        last = t;
    }
}

void Display(struct Node *p) {
    while(p) {
        printf("%d ", p->data);
        p = p->next;
    }
}

void RDisplay(struct Node *p) {
    if(p) {
        printf("%d ", p->data);
        RDisplay(p->next);
    }
}

int Count(struct Node *p) {
    int c = 0;
    while(p) {
        c++;
        p = p->next;
    }
    return c;
}
int RCount(struct Node *p) {
    if(!p) return 0;
    return RCount(p->next) + 1;
}

int Sum(struct Node *p) {
    int s = 0;
    while(p) {
        s += p->data;
        p = p->next;
    }
    return s;
}
int RSum(struct Node *p) {
    if(!p) return 0;
    return RSum(p->next) + p->data;
}

int Max(struct Node *p) {
    int m = INT_MIN;
    while(p) {
        if(p->data > m) m = p->data;
        p = p->next;
    }
    return m;
}
int RMax(struct Node *p) {
    int x = 0;
    if(!p) return INT_MIN;
    x = RMax(p->next);
    return (x > p->data) ? x : p->data;
}

int Min(struct Node *p) {
    int m = INT_MAX;
    while(p) {
        if(p->data < m) m = p->data;
        p = p->next;
    }
    return m;
}
int RMin(struct Node *p) {
    int x = 0;
    if(!p) return INT_MAX;
    x = RMin(p->next);
    return (x < p->data) ? x : p->data;
}

struct Node* LSearch(struct Node *p, int key) {
    while(p) {
        if(key == p->data)
            return p;
        p = p->next;
    }
    return NULL;
}
struct Node* RSearch(struct Node *p, int key) {
    if(!p) return NULL;
    if(key == p->data) return p;
    return RSearch(p->next, key);
}

void Insert(struct Node *p, int index, int x) {
    int i;
    struct Node *t;
    if(index < 0 || index > Count(p)) return;
    t = createNode(x);

    if(index == 0) {
        t->next = first;
        first = t;
    } else {
        for(i = 0; i < index - 1; i++) p = p->next;
        t->next = p->next;
        p->next = t;
    }
}

void SortedInsert(struct Node *p, int x) {
    struct Node *t, *q = NULL;
    t = createNode(x);
    if(first == NULL) first = t;
    else {
        while(p && p->data < x) {
            q = p;
            p = p->next;
        }
        if(p == first) {
            t->next = first;
            first = t;
        } else {
            t->next = q->next;
            q->next = t;
        }
    }
}

int Delete(struct Node *p, int index) {
    struct Node *q = NULL;
    int x = -1, i;

    if(index < 1 || index > Count(p)) return -1;

    if(index == 1) {
        q = first;
        x = first->data;
        first = first->next;
        free(q);
        return x;
    } else {
        for(i = 0; i < index - 1; i++) {
            q = p;
            p = p->next;
        }
        q->next = p->next;
        x = p->data;
        free(p);
        return x;
    }
}

int isSorted(struct Node *p) {
    int x = INT_MIN;
    while(p) {
        if(p->data < x) return 0;
        x = p->data;
        p = p->next;
    }
    return 1;
}

void RemoveDuplicate(struct Node *p) {
    struct Node *q = p->next;
    while(q) {
        if(p->data != q->data) {
            p = q;
            q = q->next;
        } else {
            p->next = q->next;
            free(q);
            q = p->next;
        }
    }
}

void Reverse1(struct Node *p) {
    int *A, i = 0;
    struct Node *q = p;
    A = (int*)malloc(sizeof(int) * Count(p));
    while(q) { A[i++] = q->data; q = q->next; }
    q = p; i--;
    while(q) { q->data = A[i--]; q = q->next; }
    free(A);
}

void Reverse2(struct Node *p) {
    struct Node *q = NULL, *r = NULL;
    while(p) {
        r = q;
        q = p;
        p = p->next;
        q->next = r;
    }
    first = q;
}

void Reverse3(struct Node *q, struct Node *p) {
    if(p) {
        Reverse3(p, p->next);
        p->next = q;
    } else {
        first = q;
    }
}

void create2(int A[], int n) {
    int i;
    struct Node *t, *last;
    second = (struct Node*)malloc(sizeof(struct Node));
    second->data = A[0];
    second->next = NULL;
    last = second;

    for(i = 1; i < n; i++) {
        t = createNode(A[i]);
        last->next = t;
        last = t;
    }
}

void Concat(struct Node *p, struct Node *q) {
    third = p;
    while(p->next) p = p->next;
    p->next = q;
}

void Merge(struct Node *p, struct Node *q) {
    struct Node *last;
    if(p->data < q->data) {
        third = last = p;
        p = p->next;
        last->next = NULL;
    } else {
        third = last = q;
        q = q->next;
        last->next = NULL;
    }
    while(p && q) {
        if(p->data < q->data) {
            last->next = p;
            last = p;
            p = p->next;
            last->next = NULL;
        } else {
            last->next = q;
            last = q;
            q = q->next;
            last->next = NULL;
        }
    }
    if(p) last->next = p;
    if(q) last->next = q;
}

int main() {
    int A[] = {3, 5, 7, 10, 25, 8, 32, 2};
    create(A, 8);

    printf("Display: ");
    Display(first); printf("\n");

    printf("Recursive Display: ");
    RDisplay(first); printf("\n");

    printf("Count = %d (iter), %d (rec)\n", Count(first), RCount(first));
    printf("Sum = %d (iter), %d (rec)\n", Sum(first), RSum(first));
    printf("Max = %d (iter), %d (rec)\n", Max(first), RMax(first));
    printf("Min = %d (iter), %d (rec)\n", Min(first), RMin(first));

    struct Node *temp = LSearch(first, 25);
    if(temp) printf("Key Found %d\n", temp->data);
    else printf("Key Not Found\n");

    Insert(first, 3, 100);
    printf("After Insert: ");
    Display(first); printf("\n");

    Delete(first, 3);
    printf("After Delete: ");
    Display(first); printf("\n");

    Reverse2(first);
    printf("After Reverse: ");
    Display(first); printf("\n");

    return 0;
}