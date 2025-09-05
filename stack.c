#include<stdio.h>
#include<stdlib.h>
#include<string.h>

struct stack{
    int size;
    int top;
    int *s;
};
void create(struct stack *p){
    printf("enter the size:");
    scanf("%d",p->size);
    p->top=-1;
    p->s=(int*)malloc(p->size * sizeof(int));
}
void display(struct stack p){
    int i;
    for(i=p.top;i>=0;i--){
        printf("%d",p.s[i]);
    }
    printf("\n");
}
void push(struct stack *p){
    
}