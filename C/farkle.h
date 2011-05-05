#define HUMAN_PLAYER 0
#define GREEDY_AI_PLAYER 1

#define E -1 //for empty

typedef struct {
    int type;
    int turn_score;
    int id;
    int threshold;
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
