#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>

#define HUMAN_PLAYER 0
#define GREEDY_AI_PLAYER 1

#define E -1 //for empty

typedef struct {
    int type;
    int turn_score;
    int id;
    int threshold;
    int win_count;
} player;

player* create_player(int type, int id, int threshold);
void take_turn(player* p);
void query_human_set_aside(player* p, int* remaining, int* set_aside, int* proposed_set_aside);
int query_human_stop(player* p, int* remaining, int* set_aside);

void query_greedy_player_set_aside(player* p, int* remaining, int* set_aside, int* proposed_set_aside);
int query_greedy_player_stop(player* p, int* remaining, int* set_aside);

int have_farkle(int* dice);
void roll_dice(int* dice);
int score_dice(int* dice);
void drop_n_dice(int* dice, int count);
void copy_dice(int* dice, int* copy);
int compare_dice_freqs(const void *a, const void *b);
void sort_by_frequency(int* dice);
int dice_contains(int* container, int* containee);
int remove_die(int* dice, int die);
int num_active_dice(int* dice);
void print_dice(char* msg, int* dice);

void run_tests();

int num_players = 4;
int cur_player = 0;
int total_scores[4] = {0, 0, 0, 0};
int die_counts[7] = {E, 0, 0, 0, 0, 0, 0};
int have_leftovers = 0;

int main()
{
    srand(time(0));
    //run_tests();
    player* players[4];
    int i, c;

    for (i=0; i<10000; i++){

        players[0] = create_player(GREEDY_AI_PLAYER, 0, 300);
        players[1] = create_player(GREEDY_AI_PLAYER, 1, 500);
        players[2] = create_player(GREEDY_AI_PLAYER, 2, 800);
        players[3] = create_player(GREEDY_AI_PLAYER, 3, 1000);

        for (c=0; c<num_players; c++){
            total_scores[c] = 0;
        }
        while(1){
            take_turn(players[cur_player]);
            if(total_scores[players[cur_player]->id] >= 10000){
                break;
            }
            cur_player += 1;
            if(cur_player == num_players){
                cur_player = 0;
            }
        }
        //printf("The winner is player %d!\n", cur_player);
        if (i%1000==0) printf("Done with game %d\n", i);
        players[cur_player]->win_count++;

        for(c=0; c<num_players; c++){
            //printf("Player %d had %d wins.\n", players[c]->id, players[c]->win_count);
            free(players[c]);
        }

    }

    for(c=0; c<num_players; c++){
        printf("Player %d had %d wins.\n", players[c]->id, players[c]->win_count);
    }

    return 0;
}


void take_turn(player* p)
{
    int i,c;
    int stop;
    p->turn_score = 0;
    int remaining[6] = {0,0,0,0,0,0};
    int set_aside[6] = {E,E,E,E,E,E};
    int proposed_set_aside[6] = {E,E,E,E,E,E};
    for(i=0; i<6; i++){
        remaining[i] = 0;
        set_aside[i] = E;
    }
    //printf("\n\nPlayer %d's turn\n\n", p->id);
    while(1){
        roll_dice(remaining);

        if(have_farkle(remaining)){
            print_dice("You got a farkle!\nDice:", remaining);
            return;
        }
        switch (p->type) {
            case HUMAN_PLAYER:
                query_human_set_aside(p, remaining, set_aside, proposed_set_aside);
                break;
            case GREEDY_AI_PLAYER:
                query_greedy_player_set_aside(p, remaining, set_aside, proposed_set_aside);
                break;
        }

        p->turn_score += score_dice(proposed_set_aside);

        /* copy the user's choice into the set aside */
        int start = num_active_dice(set_aside);
        int end = start + num_active_dice(proposed_set_aside);
        for (i=start, c=0; i<end; i++, c++){
            set_aside[i] = proposed_set_aside[c];
        }
        /* and remove the user's choice from remaining */
        for (i=0; i<num_active_dice(proposed_set_aside); i++){
            remove_die(remaining, proposed_set_aside[i]);
        }

        /* if they set aside all dice, activate them all again */
        if(num_active_dice(remaining) == 0){
            for (i=0; i<6; i++){
                remaining[i] = 0;
            }
        }

        switch (p->type) {
            case HUMAN_PLAYER:
                stop = query_human_stop(p, remaining, set_aside);
                break;
            case GREEDY_AI_PLAYER:
                stop = query_greedy_player_stop(p, remaining, set_aside);
                break;
        }
        if (stop){
            total_scores[p->id] += p->turn_score;
            return;
        }
    }
}

int have_farkle(int* dice)
{
    return score_dice(dice) == 0;
}

void query_human_set_aside(player* p, int* remaining, int* set_aside, int* proposed_set_aside){
    int i;
    char choice;
retry:

    for (i=0; i<6; i++) proposed_set_aside[i] = E;
    
    //printf("Scores:\n");
    for(i=0; i<num_players; i++){
        //printf("Player %d: %d\n", i, total_scores[i]);
    }

    //printf("Turn score: %d\n", p->turn_score);

    print_dice("\nSet Aside: ", set_aside);

    print_dice("\nYou roll the dice: ", remaining);

    /* read in the set aside from the keyboard, retrying if it is invalid */
    for (i=0; i<6; i++) proposed_set_aside[i] = E;

    for (i=0; i<num_active_dice(remaining); i++){
        choice = getc(stdin);
        if(!(choice >= 49 && choice <= 54)){
            //printf("That set aside is not valid! not real number\n");
            goto retry;
        }
        proposed_set_aside[i] = choice-48;
        choice = getc(stdin); /* eat the space */
        if(choice == '\n'){
            break;
        }
        if(choice != ' ') {
            //printf("That set aside is not valid! not a space\n");
            //printf("%d", choice);
            goto retry;
        }
    }
    if(num_active_dice(proposed_set_aside) == 0 ||
        num_active_dice(proposed_set_aside) > num_active_dice(remaining)){
        //printf("That set aside is not valid! too many dice or zero\n");
        goto retry;
    }

    if(!dice_contains(remaining, proposed_set_aside)){
        //printf("That set aside is not valid! dice not in set aside\n");
        goto retry;
    }

    int score = score_dice(proposed_set_aside);
    if(have_leftovers || score == 0){
        //printf("That set aside is not valid! has leftovers or score is 0\n");
        goto retry;
    }
}

int query_human_stop(player* p, int* remaining, int* set_aside)
{
    char choice;
    //printf("You have %d points.  Hit enter to continue rolling, or type 's' to end your turn.\n", p->turn_score);

    choice = getc(stdin);
    if (choice == '\n'){
        return 0;
    } else {
        while ( (choice = getc(stdin)) != '\n');
        return 1;
    }
}

void query_greedy_player_set_aside(player* p, int* remaining, int* set_aside, int* proposed_set_aside)
{
    int i, c;
    print_dice("\nAI player rolled:", remaining);

    for (c=0; c<6; c++){
        proposed_set_aside[c] = E;
    }

    if (num_active_dice(remaining) == 6 && score_dice(remaining) > 1000){
        copy_dice(remaining, proposed_set_aside);
    }
    sort_by_frequency(remaining);
    c = 0;
    for(i=0; i<6; i++){
        if (remaining[i] == 1 || remaining[i] == 5 ||
            die_counts[remaining[i]] >= 3){
            proposed_set_aside[c] = remaining[i];
            c++;
        }
    }
    
}

int query_greedy_player_stop(player* p, int* remaining, int* set_aside)
{
    return (p->turn_score >= p->threshold);
}


/* sets the global flag have_leftovers if there are unused dice */
int score_dice(int* dice)
{
    int score = 0;
    int i;

    int dice_copy[6];
    for (i=0; i<6; i++){
        dice_copy[i] = dice[i];
    }

    sort_by_frequency(dice_copy);    

    if (num_active_dice(dice_copy) == 6){
        /* six of a kind */
        if(dice_copy[0] == dice_copy[1] && dice_copy[0] == dice_copy[2] &&
           dice_copy[0] == dice_copy[3] && dice_copy[0] == dice_copy[4] && dice_copy[0] == dice_copy[5]){
            drop_n_dice(dice_copy, 6);
            score += 3000;
        }

        /* two sets of three */
        if(dice_copy[0] != E && dice_copy[0] == dice_copy[1] && dice_copy[0] == dice_copy[2] &&
           dice_copy[3] == dice_copy[4] && dice_copy[3] == dice_copy[5]){
            drop_n_dice(dice_copy, 6);
            score += 2500;
        }

        /* a set of four and a set of two */
        if(dice_copy[0] != E && dice_copy[0] == dice_copy[1] &&
           dice_copy[0] == dice_copy[2] && dice_copy[0] == dice_copy[3] &&
           dice_copy[4] == dice_copy[5]){
            drop_n_dice(dice_copy, 6);
            score += 1500;
        }

        /* three sets of two */
        if(dice_copy[0] != E && dice_copy[0] == dice_copy[1] &&
           dice_copy[2] == dice_copy[3] && dice_copy[4] == dice_copy[5]){
           drop_n_dice(dice_copy, 6);
            score += 1500;
        }

        /* straight */
        if(dice_copy[0] != E && dice_copy[0] == 1 && dice_copy[3] == 4 &&
           dice_copy[1] == 2 && dice_copy[4] == 5 &&
           dice_copy[2] == 3 && dice_copy[5] == 6){
            drop_n_dice(dice_copy, 6);
            score += 1500;
        }
    }

    if (num_active_dice(dice_copy) >= 5){
        /* five of a kind */
        if(dice_copy[0] == dice_copy[1] && dice_copy[0] == dice_copy[2] &&
             dice_copy[0] == dice_copy[3] && dice_copy[0] == dice_copy[4]){
            drop_n_dice(dice_copy, 5);
            score += 2000;
        }
    }

    if (num_active_dice(dice_copy) >= 4){
        /* four of a kind */
        if(dice_copy[0] == dice_copy[1] && dice_copy[0] == dice_copy[2] && dice_copy[0] == dice_copy[3]){
            drop_n_dice(dice_copy, 4);
            score += 1000;
        }
    }

    if (num_active_dice(dice_copy) >= 3){
        /* three of a kind */
        if(dice_copy[0] == dice_copy[1] && dice_copy[0] == dice_copy[2]){
            if(dice_copy[0] == 1)
                score += 300;
            else
                score += dice_copy[0] * 100;
            drop_n_dice(dice_copy, 3);
        }
    }

    /* ones and fives */
    for (i=0; i<6; i++){
        if (dice_copy[i] == 1){
            dice_copy[i] = E;
            score += 100;
        }
        if (dice_copy[i] == 5){
            dice_copy[i] = E;
            score += 50;
        }
    }

    have_leftovers = 0;
    for (i=0; i<6; i++){
        if (dice_copy[i] != E){
            have_leftovers = 1;
        }
    }

    return score;
}

void drop_n_dice(int* dice, int count)
{
    int i;
    for (i=0; i<count; i++){
        remove_die(dice, dice[0]);
    }
}

void copy_dice(int* dice, int* copy)
{
    int i;
    for (i=0; i<6; i++){
        copy[i] = dice[i];
    }
}

int compare_dice_freqs(const void *a, const void *b)
{
    int die1 = *(const int *)a;
    int die2 = *(const int *)b;
    /* if we hit an E, the other is larger, if there is a tie, sort by dot number, otherwise sort of die count */
    if(die1 == E) return 1;
    else if(die2 == E) return E;
    else if(die_counts[die1] == die_counts[die2]) return die2 - die1;
    else return die_counts[die2] - die_counts[die1];
}


void sort_by_frequency(int* dice)
{
    int i;
    /* find the counts of each die, referencing a global so we can use them in the comparison function */
    for (i=1; i<=6; i++){
        die_counts[i] = 0;
    }
    for (i=0; i<6; i++){
        if(dice[i] != E)
            die_counts[dice[i]]++;
    }

    qsort(dice, 6, sizeof(int), compare_dice_freqs);
}



int dice_contains(int* container, int* containee)
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
        if(!remove_die(container_copy, die)){
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
            dice[5] = E;
            return 1;
        }
    }
    return 0;
}

int num_active_dice(int* dice)
{
    int i;
    for (i=0; i<6; i++){
        if(dice[i] == E){
            return i;
        }
    }
    return 6;
}

void print_dice(char* msg, int* dice)
{
    //printf("%s", msg);
    int i;
    for(i=0; i<6; i++){
        if(dice[i] != E){ /* don't print out the die if it is inactive */
            //printf("%d ", dice[i]);
        }
    }
    //printf("\n");
    
}

void roll_dice(int* dice)
{
    int i;
    for(i=0; i<6; i++){
        if(dice[i] != E){
            dice[i] = rand() % 6 + 1;
        }
    }
}

player* create_player(int type, int id, int threshold)
{
    player *p = (player*) malloc(sizeof(player));

    p->type = type;
    p->turn_score = 0;
    p->id = id;
    p->threshold = threshold;

    return p;
}

void run_tests()
{
    int dice0[6] = {1,E,E,E,E,E};
    assert(score_dice(dice0) == 100);
    int dice1[6] = {5,E,E,E,E,E};
    assert(score_dice(dice1) == 50);
    int dice2[6] = {2,E,E,E,E,E};
    assert(score_dice(dice2) == 0);
    int dice3[6] = {3,E,E,E,E,E};
    assert(score_dice(dice3) == 0);
    int dice4[6] = {4,E,E,E,E,E};
    assert(score_dice(dice4) == 0);
    int dice5[6] = {6,E,E,E,E,E};
    assert(score_dice(dice5) == 0);
    int dice6[6] = {1,5,E,E,E,E};
    assert(score_dice(dice6) == 150);
    int dice7[6] = {1,1,E,E,E,E};
    assert(score_dice(dice7) == 200);
    int dice8[6] = {5,5,E,E,E,E};
    assert(score_dice(dice8) == 100);
    int dice9[6] = {2,3,E,E,E,E};
    assert(score_dice(dice9) == 0);
    int dice10[6] = {4,6,E,E,E,E};
    assert(score_dice(dice10) == 0);
    int dice11[6] = {1,1,1,E,E,E};
    assert(score_dice(dice11) == 300);
    int dice12[6] = {2,2,2,E,E,E};
    assert(score_dice(dice12) == 200);
    int dice13[6] = {3,3,3,E,E,E};
    assert(score_dice(dice13) == 300);
    int dice14[6] = {4,4,4,E,E,E};
    assert(score_dice(dice14) == 400);
    int dice15[6] = {5,5,5,E,E,E};
    assert(score_dice(dice15) == 500);
    int dice16[6] = {6,6,6,E,E,E};
    assert(score_dice(dice16) == 600);
    int dice17[6] = {2,3,4,E,E,E};
    assert(score_dice(dice17) == 0);
    int dice18[6] = {1,5,6,E,E,E};
    assert(score_dice(dice18) == 150);
    int dice19[6] = {3,5,6,E,E,E};
    assert(score_dice(dice19) == 50);
    int dice20[6] = {1,1,1,1,E,E};
    assert(score_dice(dice20) == 1000);
    int dice21[6] = {2,2,2,2,E,E};
    assert(score_dice(dice21) == 1000);
    int dice22[6] = {3,3,3,3,E,E};
    assert(score_dice(dice22) == 1000);
    int dice23[6] = {4,4,4,4,E,E};
    assert(score_dice(dice23) == 1000);
    int dice24[6] = {5,5,5,5,E,E};
    assert(score_dice(dice24) == 1000);
    int dice25[6] = {6,6,6,6,E,E};
    assert(score_dice(dice25) == 1000);
    int dice26[6] = {6,6,6,1,E,E};
    assert(score_dice(dice26) == 700);
    int dice27[6] = {4,4,4,5,E,E};
    assert(score_dice(dice27) == 450);
    int dice28[6] = {3,3,3,4,E,E};
    assert(score_dice(dice28) == 300);
    int dice29[6] = {1,2,3,4,E,E};
    assert(score_dice(dice29) == 100);
    int dice30[6] = {3,4,5,6,E,E};
    assert(score_dice(dice30) == 50);
    int dice31[6] = {2,3,4,6,E,E};
    assert(score_dice(dice31) == 0);
    int dice32[6] = {1,1,1,1,1,E};
    assert(score_dice(dice32) == 2000);
    int dice33[6] = {2,2,2,2,2,E};
    assert(score_dice(dice33) == 2000);
    int dice34[6] = {3,3,3,3,3,E};
    assert(score_dice(dice34) == 2000);
    int dice35[6] = {4,4,4,4,4,E};
    assert(score_dice(dice35) == 2000);
    int dice36[6] = {5,5,5,5,5,E};
    assert(score_dice(dice36) == 2000);
    int dice37[6] = {6,6,6,6,6,E};
    assert(score_dice(dice37) == 2000);
    int dice38[6] = {1,1,1,1,1,1};
    assert(score_dice(dice38) == 3000);
    int dice39[6] = {2,2,2,2,2,2};
    assert(score_dice(dice39) == 3000);
    int dice40[6] = {3,3,3,3,3,3};
    assert(score_dice(dice40) == 3000);
    int dice41[6] = {4,4,4,4,4,4};
    assert(score_dice(dice41) == 3000);
    int dice42[6] = {5,5,5,5,5,5};
    assert(score_dice(dice42) == 3000);
    int dice43[6] = {6,6,6,6,6,6};
    assert(score_dice(dice43) == 3000);
    int dice44[6] = {1,1,1,2,2,2};
    assert(score_dice(dice44) == 2500);
    int dice45[6] = {3,3,3,4,4,4};
    assert(score_dice(dice45) == 2500);
    int dice46[6] = {5,5,5,6,6,6};
    assert(score_dice(dice46) == 2500);
    int dice47[6] = {1,1,2,2,3,3};
    assert(score_dice(dice47) == 1500);
    int dice48[6] = {4,4,5,5,6,6};
    assert(score_dice(dice48) == 1500);
    int dice49[6] = {1,1,1,1,2,2};
    assert(score_dice(dice49) == 1500);
    int dice50[6] = {3,3,3,3,4,4};
    assert(score_dice(dice50) == 1500);
    int dice51[6] = {5,5,5,5,6,6};
    assert(score_dice(dice51) == 1500);
    int dice52[6] = {6,2,5,2,6,4};
    assert(score_dice(dice52) == 50);
    int dice53[6] = {6,5,3,2,1,1};
    assert(score_dice(dice53) == 250);

}
