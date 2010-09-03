#include <stdio.h>

main()
{
    char c;
    while ((c=getchar()) != EOF){
        if (c=='\t'){putchar('\\'); putchar('t');}
        else if (c=='\b'){putchar('\\'); putchar('b');}
        else if (c=='\\'){putchar('\\'); putchar('\\');}
        else putchar(c);
    }
}
