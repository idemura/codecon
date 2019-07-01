#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <map>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using namespace std;

using i32 = int32_t;
using i64 = int64_t;
using pii = std::pair<int, int>;

int main(int argc, char **argv) {
    i64 k = 0;
    scanf("%lld", &k);
    i64 first = 0;
    i64 last = 10;
    int width = 1;
    while (k >= (last - first) * width) {
        k -= (last - first) * width;
        first = last;
        last *= 10;
        width++;
    }
    char temp[32];
    snprintf(temp, sizeof(temp), "%lld", first + k / width);
    printf("%d\n", int(temp[k % width] - '0'));
    return 0;
}
