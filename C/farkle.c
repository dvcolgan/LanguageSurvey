#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "farkle.h"

int num_players = 2;
int cur_player = 0;
int total_scores[2] = {0, 0};

int main()
{
    srand(time(0));
    //run_tests();
    player* players[2];
    int i;

    players[0] = create_player(HUMAN_PLAYER);
    players[0]->id = 0;
    players[1] = create_player(GREEDY_AI_PLAYER);
    players[1]->id = 1;

    while(1){
        take_turn(players[cur_player]);
        if (players[cur_player]->score >= 10000){
            break;
        }
        cur_player += 1;
        if (cur_player == num_players){
            cur_player = 0;
        }
    }
    printf("The winner is player %d!\n", cur_player);

    for(i=0; i<num_players; i++){
        free(players[i]);
    }

    return 0;
}

void run_tests()
{
    int dice[6] = {2, 1, 4, 3, 6, 5};
    int dice2[6] = {3, 4, 1, -1, -1, -1};
    int ret = array_contains(dice, dice2);
    print_dice("",dice);
    print_dice("",dice2);
    printf("%d ", ret);
}

/* set dice values to -1 if they are not used */
void take_turn(player* p)
{
    int i;
    int turn_score = 0;
    int* remaining = (int*)malloc(sizeof(int) * 6);
    int* set_aside = (int*)malloc(sizeof(int) * 6);
    for(i=0; i<6; i++){
        remaining[i] = 0;
        set_aside[i] = -1;
    }
    while(1){
        roll_dice(remaining);
        switch (p->type) {
            case HUMAN_PLAYER:
                query_human_set_aside(p, remaining, set_aside);
                break;
            case GREEDY_AI_PLAYER:
                break;
            case GA_PLAYER:
                break;
        }
        print_dice("Remaining: \n", remaining);
    }
    free(remaining);
    free(set_aside);
}

void query_human_set_aside(player* p, int* remaining, int* set_aside){
    int i,c;
    char choice;
    int potential_set_aside[6];
retry:

    for (i=0; i<6; i++) potential_set_aside[i] = -1;
    
    printf("\n\nScores:\n");
    for(i=0; i<num_players; i++){
        printf("Player %d: %d\n", i, total_scores[i]);
    }

    printf("Turn score: %d\n", p->turn_score);

    print_dice("\nSet Aside: ", set_aside);

    print_dice("\nYou roll the dice: ", remaining);

    /* read in the set aside from the keyboard, retrying if it is invalid */
    for (i=0; i<6; i++) potential_set_aside[i] = -1;

    for (i=0; i<num_active_dice(remaining); i++){
        choice = getc(stdin);
        if (!(choice >= 49 && choice <= 54)){
            printf("That set aside is not valid! not real number\n");
            goto retry;
        }
        potential_set_aside[i] = choice-48;
        choice = getc(stdin); /* eat the space */
        if (choice == '\n'){
            break;
        }
        if (choice != ' ') {
            printf("That set aside is not valid! not a space\n");
            printf("%d", choice);
            goto retry;
        }
    }
    if (num_active_dice(potential_set_aside) == 0 ||
        num_active_dice(potential_set_aside) > num_active_dice(remaining)){
        printf("That set aside is not valid! too many dice or zero\n");
        goto retry;
    }

    if(!array_contains(remaining, potential_set_aside)){
        printf("That set aside is not valid! dice not in set aside\n");
        goto retry;
    }

    /* copy the user's choice into the set aside */
    int start = num_active_dice(set_aside);
    int end = start + num_active_dice(potential_set_aside);
    for (i=start, c=0; i<end; i++, c++){
        set_aside[i] = potential_set_aside[c];
    }
    /* and remove the user's choice from remaining */
    for (i=0; i<num_active_dice(potential_set_aside); i++){
        remove_die(remaining, potential_set_aside[i]);
    }
}

int array_contains(int* container, int* containee)
{
    int container_copy[6];
    int containee_copy[6];
    int i;
    int die;
    for (i=0; i<6; i++){
        container_copy[i] = container[i];
        containee_copy[i] = containee[i];
    }

    while (num_active_dice(containee_copy) > 0) {
        die = containee_copy[0];
        remove_die(containee_copy, die);
        if (!remove_die(container_copy, die)){
            return 0;
        }
    }
    return 1;
}

/* returns true if it removed a die, otherwise false */
int remove_die(int* dice, int die)
{
    int i;
    for (i=0; i<6; i++){
        if(dice[i] == die){ 
            for (; i<5; i++){
                dice[i] = dice[i+1];
            }
            dice[5] = -1;
            return 1;
        }
    }
    return 0;
}

int num_active_dice(int* dice)
{
    int i;
    for (i=0; i<6; i++){
        if (dice[i] == -1){
            return i;
        }
    }
    return 6;
}

void print_dice(char* msg, int* dice)
{
    printf("%s", msg);
    int i;
    for(i=0; i<6; i++){
        if(dice[i] != -1){ /* don't print out the die if it is inactive */
            printf("%d ", dice[i]);
        }
    }
    printf("\n");
    
}

void roll_dice(int* dice)
{
    int i;
    for(i=0; i<6; i++){
        if (dice[i] != -1){
            dice[i] = rand() % 6 + 1;
        }
    }
}

player* create_player(int type)
{
    player *p = (player*) malloc(sizeof(player));

    p->type = type;
    p->score = 0;
    p->turn_score = 0;

    return p;
}

