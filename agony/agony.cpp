#include "graph.h"
#include <stdio.h>


int
main(int argc, char **argv)
{
	agony ag;

	if (argc == 1) {
		printf("USAGE: %s <input file> [<output file>]\n", argv[0]);
		printf("input file format:\n");
		printf("<from1> <to1>\n");
		printf("<from2> <to2>\n");
		printf("...\n");
		return 1;
	}
	
	FILE *in = fopen(argv[1], "r");
	if (in == NULL) return 1;
	ag.read(in);
	fclose(in);

	ag.cycledfs();
	ag.initagony();
	ag.initrank();
	printf("%d %d\n", ag.primal(), ag.dual());
	ag.minagony();
	printf("%d\n", ag.dual());

	if (argc > 2) {
		FILE *out = fopen(argv[2], "w");
		if (out == NULL) return 1;
		ag.writeagony(out);
		fclose(out);
	}

	return 0;
}
