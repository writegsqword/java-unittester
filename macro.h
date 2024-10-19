//remember to define 
//Object result;
#define UNIT_TEST(METHOD_NAME, idx, expected, ...) __NL__  \
    result = (Object)METHOD_NAME(__NL__ __VA_ARGS__); __NL__  __NL__ \
    System.out.println(#METHOD_NAME + __NL__ \
    " Output " + #idx + ": " + __NL__  \
    result.toString() + "\n"); __NL__ __NL__\
    if (!((Object)expected).toString()__NL__.equals(result.toString())) { __NL__ \
    __TAB__ System.out.println("FAILED: " + __NL__ #METHOD_NAME + " " + #idx); __NL__  \
    __TAB__ return false; __NL__ \
    }
