#include <stdio.h>

#define IN  1
#define OUT 0

main()
{
    int c, state;

    state = OUT;

    while((c=getchar()) != EOF){
        if (c != '\n') putchar(c);
        if (c == ' ' || c == '\t' || c == '\n'){
            state = OUT;
            putchar('\n');
        }
        else if (state == OUT){
            state = IN;
        }
    }
}
