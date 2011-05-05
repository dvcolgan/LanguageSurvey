#include <stdio.h>

main()
{
    int c, i, j, state, len;

    char hist[256];

    len = 0;

    for (i=0; i<256; i++){
        hist[i] = 0;
    }

    while((c=getchar()) != EOF){
        hist[c]++;
    }

    for (i=32; i<126; i++){
        printf("%c|", i);
        for (j=0; j<hist[i]; j++){
            putchar('=');
        }
        putchar('\n');
    }

    int longest = 0;
    for (i=32; i<126; i++){
        if (hist[i] > longest) longest = hist[i];
    }

    for (i=0; i<longest; i++){
        for (j=32; j<126; j++){
            if (hist[j] >= (longest-i))
                printf("|");
            else
                printf(" ");
        }
        putchar('\n');
    }
    for (i=32; i<126; i++){
        printf("%c", i);
    }
    putchar('\n');

}
