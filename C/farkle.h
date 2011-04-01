#define HUMAN_PLAYER 0
#define GREEDY_AI_PLAYER 1
#define GA_PLAYER 2

typedef struct {
    int type;
    int score;
    int turn_score;
    int id;
} player;

player* create_player(int type);
void take_turn(player* p);
void roll_dice(int* dice);
void query_human_set_aside(player* p, int* remaining, int* set_aside);
int array_contains(int* container, int* containee);
int remove_die(int* dice, int die);
int num_active_dice(int* dice);
void print_dice(char* msg, int* dice);
void run_tests();
