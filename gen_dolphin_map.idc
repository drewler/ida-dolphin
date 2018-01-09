#define UNLOADED_FILE   1
#include <idc.idc>

/*
 * Code from gist by @jackoalan
 * https://gist.github.com/jackoalan/9a3e7e0c71f531686900
 */  

static main(void)
{
	auto address = NextFunction(0);
	auto filestr = AskFile(1, "*.map", "Dolphin MAP output file");
	auto file = fopen(filestr, "w");
	fprintf(file, ".text\n");
	while (address != -1) {
		auto name = GetFunctionName(address);
		auto demangle_name = Demangle(name, GetLongPrm(INF_LONG_DN));
		if (strlen(demangle_name) > 1)
			name = demangle_name;
		if (strlen(name) > 1) {
			fprintf(file, "%08X %08X %08X %d %s\n",
					address, GetFunctionAttr(address, FUNCATTR_END) - address,
					address, 0, name);
		}
		address = NextFunction(address);
	}
	fclose(file);
}