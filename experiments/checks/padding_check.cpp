// Verify all subsets at a prime, or select the weakly sum-free five-element
// remainders with --five. Every ordering is checked directly. Multiplication
// by a nonzero residue preserves partial-sum distinctness.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint64_t;
using Word = std::array<int, 64>;

static Mask bit(int x) { return Mask{1} << x; }

struct Check {
    int p;
    std::uint64_t cases = 0, retries = 0, orbits = 0;
    std::uint64_t random_state = 20261124;

    int add(int x, int y) const {
        int z = x + y;
        return z < p ? z : z - p;
    }

    Mask vertices(const Word& word, int n, Mask expected) const {
        Mask seen = 0, labels = 0;
        int s = 0;
        for (int i = 0; i < n; ++i) {
            int a = word[i];
            if (a <= 0 || a >= p || (labels & bit(a)) || (seen & bit(s)))
                throw std::runtime_error("repeated vertex or invalid label");
            labels |= bit(a);
            seen |= bit(s);
            s = add(s, a);
        }
        if (s != 0 || labels != expected)
            throw std::runtime_error("wrong total or label set");
        return seen;
    }

    bool insert_pair(const Word& parent, int n, Mask seen, int b, Word& child) const {
        int u = 0;
        for (int i = 0; i < n; ++i) {
            int v = add(u, parent[i]);
            for (int shift : {b, p - b}) {
                if (seen & (bit(add(u, shift)) | bit(add(v, shift)))) continue;
                std::copy_n(parent.begin(), i, child.begin());
                child[i] = shift;
                child[i + 1] = parent[i];
                child[i + 2] = p - shift;
                std::copy(parent.begin() + i + 1, parent.begin() + n, child.begin() + i + 3);
                return true;
            }
            u = v;
        }
        return false;
    }

    unsigned next_random() {
        random_state ^= random_state << 13;
        random_state ^= random_state >> 7;
        random_state ^= random_state << 17;
        return static_cast<unsigned>(random_state);
    }

    // A capped search finds positive certificates only. Exhausting the cap
    // never counts as a proof that no word exists.
    bool search(Word& word, int i, int n, int s, Mask visited, int& budget) {
        if (i == n - 1) return add(s, word[i]) == 0;
        if (--budget <= 0) return false;
        int count = n - i, start = next_random() % count;
        for (int j = 0; j < count && budget > 0; ++j) {
            int k = i + (start + j) % count, v = add(s, word[k]);
            if (visited & bit(v)) continue;
            std::swap(word[i], word[k]);
            if (search(word, i + 1, n, v, visited | bit(v), budget)) return true;
            std::swap(word[i], word[k]);
        }
        return false;
    }

    void all_paddings(const Word& word, int n, Mask labels,
                      const std::vector<int>& available, size_t start) {
        Mask seen = vertices(word, n, labels);
        ++cases;
        for (size_t j = start; j < available.size(); ++j) {
            int b = available[j];
            Word child;
            if (!insert_pair(word, n, seen, b, child)) {
                ++retries;
                std::copy_n(word.begin(), n, child.begin());
                child[n] = b;
                child[n + 1] = p - b;
                bool found = false;
                for (int attempt = 0; attempt < 256 && !found; ++attempt) {
                    int budget = 5000;
                    found = search(child, 0, n + 2, 0, bit(0), budget);
                }
                if (!found) throw std::runtime_error("no certificate found within search budget");
            }
            all_paddings(child, n + 2, labels | bit(b) | bit(p - b), available, j + 1);
        }
    }

    void test_seed(const Word& u) {
        Mask seed = 0;
        for (int i = 0; i < 5; ++i) seed |= bit(u[i]);
        for (int i = 0; i < 5; ++i) {
            if (seed & bit(p - u[i])) return;
            for (int j = 0; j < i; ++j)
                if (seed & bit(add(u[i], u[j]))) return;
        }
        // Choose the least mask among all dilates containing 1.
        for (int scale = 1; scale < p; ++scale) {
            Mask image = 0;
            for (int i = 0; i < 5; ++i) image |= bit(scale * u[i] % p);
            if ((image & bit(1)) && image < seed) return;
        }
        std::vector<int> available;
        for (int b = 1; b <= p / 2; ++b)
            if (!(seed & (bit(b) | bit(p - b)))) available.push_back(b);
        ++orbits;
        all_paddings(u, 5, seed, available, 0);
    }

    void validate_prime() const {
        if (p < 11 || p >= 64) throw std::runtime_error("expected a prime from 11 through 61");
        for (int q = 2; q * q <= p; ++q)
            if (p % q == 0) throw std::runtime_error("modulus must be prime");
    }

    void five_only() {
        validate_prime();
        for (int a = 2; a < p; ++a) for (int b = a + 1; b < p; ++b)
            for (int c = b + 1; c < p; ++c) {
                int d = (p - (1 + a + b + c) % p) % p;
                if (d > c) test_seed(Word{1, a, b, c, d});
            }
        if (cases != orbits * (Mask{1} << (p / 2 - 5)))
            throw std::runtime_error("incomplete enumeration");
        std::cout << "p=" << p << " orbits=" << orbits << " completions=" << cases
                  << " fallback_searches=" << retries << '\n';
    }
    Word powers{};
    Mask exponent_mask = 0;
    std::uint64_t covered = 0;
    int maximum_asymmetry = 63;

    void check_asymmetric_seed(Mask exponents, const Word& seed, int size) {
        // Multiplication is cyclic rotation in primitive-root coordinates.
        // Only consider images containing 1, exactly the rotations by a
        // set exponent. The number fixing the mask is its stabilizer order.
        int stabilizer = 0;
        for (Mask bits = exponents; bits; bits &= bits - 1) {
            int j = __builtin_ctzll(bits);
            Mask image = ((exponents >> j) | (exponents << (p - 1 - j))) & exponent_mask;
            if (image < exponents) return;
            stabilizer += image == exponents;
        }
        Mask labels = 0;
        for (int i = 0; i < size; ++i) labels |= bit(seed[i]);
        std::vector<int> available;
        for (int b = 1; b <= p / 2; ++b)
            if (!(labels & (bit(b) | bit(p - b)))) available.push_back(b);
        Word word = seed;
        if (size != 0) {
            bool found = false;
            for (int attempt = 0; attempt < 256 && !found; ++attempt) {
                int budget = 5000;
                found = search(word, 0, size, 0, bit(0), budget);
            }
            if (!found) throw std::runtime_error("missing seed certificate");
        }
        ++orbits;
        covered += ((p - 1) / stabilizer) * (Mask{1} << available.size());
        all_paddings(word, size, labels, available, 0);
    }

    void visit_seeds(int i, int sum, Mask exponents, Word& word, int size) {
        if (size == maximum_asymmetry) {
            if (sum == 0) check_asymmetric_seed(exponents, word, size);
            return;
        }
        int half = p / 2, a = powers[i], b = p - a;
        if (i == half - 1) {
            if (sum == 0) check_asymmetric_seed(exponents, word, size);
            else if (sum == b || sum == a) {
                word[size] = p - sum;
                int j = sum == b ? i : i + half;
                check_asymmetric_seed(exponents | bit(j), word, size + 1);
            }
            return;
        }
        visit_seeds(i + 1, sum, exponents, word, size);
        word[size] = a;
        visit_seeds(i + 1, add(sum, a), exponents | bit(i), word, size + 1);
        word[size] = b;
        visit_seeds(i + 1, add(sum, b), exponents | bit(i + half), word, size + 1);
    }

    std::uint64_t subset_count() const {
        // Independent count in additive coordinates. A class {b,-b} is
        // unused, used twice, or used with precisely one of the two signs.
        using Counts = std::array<std::array<std::uint64_t, 64>, 64>;
        Counts dp{};
        dp[0][0] = 1;
        int limit = std::min(maximum_asymmetry, p / 2);
        for (int b = 1; b <= p / 2; ++b) {
            Counts next{};
            for (int r = 0; r <= limit; ++r) for (int s = 0; s < p; ++s) {
                next[r][s] += 2 * dp[r][s];
                if (r == limit) continue;
                next[r + 1][add(s, b)] += dp[r][s];
                next[r + 1][add(s, p - b)] += dp[r][s];
            }
            dp = next;
        }
        std::uint64_t result = 0;
        for (int r = 0; r <= limit; ++r) result += dp[r][0];
        return result;
    }

    void all_sets() {
        validate_prime();
        exponent_mask = bit(p - 1) - 1;
        bool primitive = false;
        for (int g = 2; g < p && !primitive; ++g) {
            int x = 1, order = 0;
            do { powers[order++] = x; x = x * g % p; } while (x != 1);
            primitive = order == p - 1;
        }
        if (!primitive) throw std::runtime_error("could not generate multiplicative group");
        // Symmetric sets have empty remainder and cannot be normalized at 1.
        // Give the explicit two-parallel-path construction for each symmetric
        // set. Alternating decreasing smaller magnitudes stay in [0, b_2].
        for (Mask subset = 1; subset < bit(p / 2); ++subset) {
            Word magnitudes{}, word{};
            Mask labels = 0;
            int n = 0;
            for (int b = p / 2; b >= 1; --b) {
                if (!(subset & bit(b - 1))) continue;
                magnitudes[n++] = b;
                labels |= bit(b) | bit(p - b);
            }
            for (int i = 1; i < n; ++i) {
                int a = i % 2 ? magnitudes[i] : p - magnitudes[i];
                word[i - 1] = a;
                word[2 * n - 1 - i] = p - a;
            }
            word[n - 1] = magnitudes[0];
            word[2 * n - 1] = p - magnitudes[0];
            vertices(word, 2 * n, labels);
            ++cases;
        }
        covered = bit(p / 2);
        Word word{1};
        visit_seeds(1, 1, bit(0), word, 1);
        auto expected = (bit(p - 1) + p - 1) / p;
        if (maximum_asymmetry >= p / 2 && covered != expected)
            throw std::runtime_error("wrong total count of zero-sum sets");
        if (covered != subset_count()) throw std::runtime_error("wrong independent subset count");
        std::cout << "p=" << p << " asymmetric_seed_orbits=" << orbits
                  << " words_checked=" << cases << " zero_sum_sets_including_empty=" << covered
                  << " padding_fallbacks=" << retries << std::endl;
    }

};

int main(int argc, char** argv) {
    bool five = argc > 1 && std::string(argv[1]) == "--five";
    bool bounded = argc > 1 && std::string(argv[1]) == "--at-most-five";
    int first = (five || bounded) ? 2 : 1;
    if (argc <= first) {
        std::cerr << "Usage: padding_check [--five|--at-most-five] PRIME...\n";
        return 1;
    }
    for (int i = first; i < argc; ++i) {
        Check check{std::stoi(argv[i])};
        if (bounded) check.maximum_asymmetry = 5;
        if (five) check.five_only(); else check.all_sets();
    }
}
