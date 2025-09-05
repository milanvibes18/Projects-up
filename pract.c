#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct Node{
    int data;
    struct Node* next;
};
struct Node* create(int arr[],int size){
    if (size == 0) return NULL;

    struct Node* head=(struct Node*)malloc(sizeof(struct Node));
    
    head->data=arr[0];
    head->next=NULL;
    struct Node* current = head;

    for(int i=1;i<size;i++){
        struct Node* newNode=(struct Node*)malloc(sizeof(struct Node));
        newNode->data=arr[i];
        newNode->next=NULL;

        current->next=newNode;
        current= newNode;
    }
    return head;
}
void display(struct Node* p){
    while(p!=NULL){
        printf("%d->",p->data);
        p=p->next;
    }
    printf("NULL\n");
}
void concatenate(struct Node **head, struct Node* head1){
    struct Node* temp= *head;
    if (*head==NULL){
        *head=head1;
    }
    else{
        
        while(temp->next!=NULL){
            temp=temp->next;
        }
        temp->next=head1;
    }
    
}
void insert_beg(struct Node** head, int x){
    struct Node* temp= (struct Node*)malloc(sizeof(struct Node));
    temp->data=x;
    temp->next= *head;
    *head=temp;
    
}
void insert_end(struct Node** head, int x){
    struct Node* temp= (struct Node*)malloc(sizeof(struct Node));
    temp->data=x;
    if(*head==NULL){
        *head=temp;
        return;
    }
    
    struct Node* last=*head;
    while(last->next!=NULL){
        last=last->next;
    }
    
    last->next=temp;
    temp->next=NULL;
    
}
void insert_pos(struct Node** head, int index, int x){
    struct Node* temp= (struct Node*)malloc(sizeof(struct Node));
    struct Node* last= *head;

    temp->data=x;
    temp->next=NULL;
    if(index==0){
        insert_beg(head,x);
        return;
    }
    for(int i=0;i<index-1;i++){
            if (last == NULL) {
        printf("Index out of range\n");
        free(temp);
        return;
    }
        last=last->next;
        
    }
   
    temp->next=last->next;
    last->next=temp;

}
void delete_beg(struct Node** head){
    if(*head==NULL){
        printf("empty");
        return;
    }
    struct Node* temp= *head;
    *head=(*head)->next;
    free(temp);
}
void delete_end(struct Node** head){
    if(*head==NULL){
        printf("empty");
        return;
    }
    while((*head)->next->next!=NULL){
        *head=(*head)->next;
    }
    struct Node* temp=*head;
    free(temp);

}
void delete_pos(struct Node** head, int index){
    if(*head==NULL){
        printf("empty");
        return;
    }
    struct Node* temp=*head;
    for(int i=1;temp != NULL && i<index-2;i++){
        temp=temp->next;
    }
    
    if(temp==NULL || temp->next==NULL){
        printf("out of range");
        return;
    }
    struct Node* todelete= temp->next;
    temp->next=temp->next->next;
    free(todelete);
}

int main(){
    int arr[]={10,20,30,40};
    
    struct Node* head= create(arr,sizeof(arr)/sizeof(arr[0]));
    int arr1[]={15,225,65};
    struct Node* head1= create(arr1, sizeof(arr1)/sizeof(arr1[0]));
    
    display(head);
    display(head1);
    concatenate(&head,head1);
    display(head);
    insert_beg(&head,5);
    display(head);
    insert_end( &head, 5);
    display(head);
    insert_pos(&head, 2,64);
    display(head);
    delete_beg(&head);
    display(head);
    delete_pos(&head,2);
    display(head);
    return 0;
}