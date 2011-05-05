#include <stdio.h>

main()
{
    char c, prev;
    prev = '|';
    while ((c=getchar()) != EOF){
        if (!(prev == ' ' && c == ' ')){
            putchar(c);
        }
        prev = c;
    }
}
