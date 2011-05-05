#include <stdio.h>

main()
{
    char c;
    long blanks, tabs, newlines;
    blanks = tabs = newlines = 0;
    while ((c=getchar()) != EOF){
        if (c==' ') blanks++;
        if (c=='\t') tabs++;
        if (c=='\n') newlines++;
    }
    printf("Blanks: %ld, Tabs: %ld, Newlines: %ld\n", blanks, tabs, newlines);
}
