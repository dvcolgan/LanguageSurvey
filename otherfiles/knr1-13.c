#include <stdio.h>

#define IN  1
#define OUT 0

main()
{
    int c, i, j, state, len;

    int hist[20];

    state = OUT;
    len = 0;

    for (i=0; i<20; i++){
        hist[i] = 0;
    }

    while((c=getchar()) != EOF){
        if (c == ' ' || c == '\t' || c == '\n'){
            if (len >= 20) printf("Word greater than 20 chars!\n");
            else hist[len]++;

            state = OUT;
            len = 0;
        }
        else{
            if (state == OUT) state = IN;
            len++;
        }
    }

    for (i=0; i<20; i++){
        printf("%2d|", i);
        for (j=0; j<hist[i]; j++){
            putchar('=');
        }
        putchar('\n');
    }

    int longest = 0;
    for (i=0; i<20; i++){
        if (hist[i] > longest) longest = hist[i];
    }

    for (i=0; i<longest; i++){
        for (j=0; j<20; j++){
            if (hist[j] >= (longest-i))
                printf(" []");
            else
                printf("   ");
        }
        putchar('\n');
    }
    for (i=0; i<20; i++){
        printf("%3d", i);
    }

}
