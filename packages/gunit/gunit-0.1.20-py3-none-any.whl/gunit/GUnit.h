#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define typeof __typeof__

typedef void (*gunit_function_t)();

#define gnoopt __attribute__((optimize(0)))

/**
 * All asserts will call this function. GDB will catch any call to this function
 * and logs it
 */
gnoopt inline static void gunit_mono() {
  return;
}

template<typename T> bool gunit_mono_hook(T expected, T result, bool no, uintmax_t line_number, const char *file) {
  gunit_mono();
  return (expected == result) ^ no;
}

#define GUNIT_MONO_HOOK(expected, result, negate) gunit_mono_hook((expected), (result), (negate), __LINE__, __FILE__)

/**
 * All asserts will call this function. GDB will catch any call to this function
 * and logs it
 */
gnoopt inline static void gunit_range() {
  return;
}

template <typename T> bool gunit_range_hook(T expected, T result, bool no, uintmax_t line_number, const char *file) {
  gunit_range();
  return (!no && (expected > result)) || (no && (expected < result));
}

#define GUNIT_RANGE_HOOK(expected, result, negate) gunit_range_hook((expected), (result), (negate), __LINE__, __FILE__)

/**
 * Function for asserting arrays and objects
 */
gnoopt inline static bool gunit_array(void *expected, void *result, intmax_t size, intmax_t line_number, const char *file, bool no) {
  uint8_t *ex = (uint8_t *) expected;
  uint8_t *re = (uint8_t *) result;

  // Check if equal
  for (uint32_t i = 0; i < size; ++i) {
    if (ex[i] != re[i])
      return gunit_mono_hook(ex[i], re[i], no, line_number, file);
  }

  // If no differences were found
  return gunit_mono_hook(true, true, !no, line_number, file);
}

#define GUNIT_ARRAY_HOOK(expected, result, size, negate) \
gunit_array((void *) (expected), (void *) (result), (size) * sizeof(expected[0]), __LINE__, __FILE__, negate)

#define GUNIT_STRUCT_HOOK(expected, result, negate) \
gunit_array((void *) &(expected), (void *) &(result), sizeof(expected), __LINE__, __FILE__, negate)

gnoopt inline static void gunit_fail_hook(intmax_t line_number, const char *file, const gunit_function_t test) {
  return;
}

gnoopt inline static void gunit_fail(intmax_t line_number, const char *file, const gunit_function_t *tests, intmax_t nr_of_tests) {
  for (intmax_t i = 0; i < nr_of_tests; ++i) {
    gunit_fail_hook(line_number, file, tests[i]);
  }
}

#define GUNIT_FAIL_PROCEDURE(tests, nr_of_tests) gunit_fail(__LINE__, __FILE__, (tests), (nr_of_tests))

/**
 * This has to be called at the end of a test suite
 */
gnoopt inline static void gunit_end() {
  volatile bool x = false;
  if (x) {
    gunit_fail_hook(0, "0", NULL);
    gunit_mono_hook(0, 0, false, 0, "0");
    gunit_range_hook(0, 0, false, 0, "0");
  }

  return;
}

/**
 * Execute a test suite
 */
gnoopt inline static void gunit_suite(gunit_function_t before, gunit_function_t after, const gunit_function_t *tests,
                                      intmax_t nr_of_tests) {
  for (intmax_t i = 0; i < nr_of_tests; ++i) {
    if (before)
      (*before)();

    (*tests[i])();

    if (after)
      (*after)();
  }
}

/**
 * Execute given tests with before and after functions
 */
#define GEXECUTE(before, after, ...)  {gunit_suite(before, after, (const gunit_function_t[]){__VA_ARGS__}, \
    sizeof((gunit_function_t[]){__VA_ARGS__}) / sizeof(gunit_function_t));}

/**
 * Exevute tests without before or after
 */
#define GSIMPLE_EXECUTE(...) GEXECUTE(NULL, NULL, __VA_ARGS__)

/**
 * Signal the end of all the tests
 */
#define GEND() {gunit_end();}

/**
 * Assert if given values are equel.
 */
#define GASSERT(expected, result) {if (!GUNIT_MONO_HOOK(expected, result, false)) return;}

/**
 * Assert if given values are not equal.
 */
#define GNOT_ASSERT(not_expected, result) {if (!GUNIT_MONO_HOOK(not_expected, result, true)) return;}

/**
 * Assert if given arrays contain same elements
 */
#define GARRAY_ASSERT(expected, result, nr_of_elements) {if (!GUNIT_ARRAY_HOOK(expected, result, nr_of_elements, false)) return;}

/**
 * Assert if given arrays don't have same elements
 */
#define GARRAY_NOT_ASSERT(not_expected, result, nr_of_elements) {if (!GUNIT_ARRAY_HOOK(not_expected, result, nr_of_lements, true)) return;}

/**
 * Assert if given structs contain same values
 */
#define GSTRUCT_ASSERT(expected, result) {if (!GUNIT_STRUCT_HOOK(expected, result, false)) return;}

/**
 * Assert if given structs don't contain same values
 */
#define GSTRUCT_NOT_ASSERT(not_expected, result) {if (!GUNIT_STRUCT_HOOK(not_expected, result, true)) return;}

/**
 * Asserts if the value is less than expected
 */
#define GLESS_ASSERT(expected, result) {if (!GUNIT_RANGE_HOOK(expected, result, false)) return;}

/**
 * Asserts if the value is greater than expected
 */
#define GGREATER_ASSERT(expected, result) {if (!GUNIT_RANGE_HOOK(expected, result, true)) return;}

/**
 * Asserts if the value is in between the given values
 */
#define GINTERVAL_ASSERT(expectedhigh, expectedlow, result) {GLESS_ASSERT(expectedhigh, result); GGREATER_ASSERT(expectedlow, result);}

/**
 * Inline data for the test. Use this
 * to give arguments to your test.
 */
#define GINLINE_DATA(name, test, ...) static void name() {test(__VA_ARGS__);}

/**
 * Fail the given tests
 */
#define GFAIL(...) {GUNIT_FAIL_PROCEDURE((const gunit_function_t[]){__VA_ARGS__}, \
                    sizeof((gunit_function_t[]){__VA_ARGS__}) / sizeof(gunit_function_t));}


/**
 * Assert for boolean
 * Fails if false
 */
#define GBOOL(result) GASSERT((bool) true, (bool) (result))
