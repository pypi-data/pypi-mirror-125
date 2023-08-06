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
gnoopt inline static void gunit_mone_hook_() {
  return;
}

#define GUNIT_MONO_TYPE(t) \
gnoopt inline static t gunit_mono_hook_ ## t(t expected, t result, intmax_t line_number, const char *file, bool no) { \
  gunit_mono_hook_();                    \
  return (expected == result) ^ no;      \
}

/**
 * All asserts will call this function. GDB will catch any call to this function
 * and logs it
 */
gnoopt inline static void gunit_range_hook_() {
  return;
}

#define GUNIT_RANGE_TYPE(t) \
gnoopt inline static t gunit_range_hook_ ## t(t expected, t result, intmax_t line_number, const char *file, bool no) { \
  gunit_range_hook_();                                                \
  return (!no && (expected > result)) || (no && (expected < result)); \
}

#define GUNIT_TYPE(t)  GUNIT_MONO_TYPE(t) GUNIT_RANGE_TYPE(t)

#define GUNIT_MONO_TYPE_CALL(t, expected, result, negate) gunit_mono_hook_ ## t(expected, result, __LINE__, __FILE__, negate)
#define GUNIT_RANGE_TYPE_CALL(t, expected, result, negate) gunit_range_hook_ ## t(expected, result, __LINE__, __FILE__, negate)

GUNIT_TYPE(uint8_t);
GUNIT_TYPE(uint16_t);
GUNIT_TYPE(uint32_t);
GUNIT_TYPE(uint64_t);
GUNIT_TYPE(int8_t);
GUNIT_TYPE(int16_t);
GUNIT_TYPE(int32_t);
GUNIT_TYPE(int64_t);
GUNIT_TYPE(float);
GUNIT_TYPE(double);

#define GUNIT_MONO_HOOK_TYPE(t)  t: GUNIT_MONO_TYPE_CALL(t, (expected), (result), (negate))
#define GUNIT_MONO_HOOK(expected, result, negate) \
_Generic((expected),                              \
  GUNIT_MONO_HOOK_TYPE(uint8_t),                  \
  GUNIT_MONO_HOOK_TYPE(uint16_t),                 \
  GUNIT_MONO_HOOK_TYPE(uint32_t),                 \
  GUNIT_MONO_HOOK_TYPE(uint64_t),                 \
  GUNIT_MONO_HOOK_TYPE(int8_t),                   \
  GUNIT_MONO_HOOK_TYPE(int16_t),                  \
  GUNIT_MONO_HOOK_TYPE(int32_t),                  \
  GUNIT_MONO_HOOK_TYPE(int64_t),                  \
  GUNIT_MONO_HOOK_TYPE(float),                    \
  GUNIT_MONO_HOOK_TYPE(double)                    \
)(expected)

#define GUNIT_RANGE_HOOK_TYPE(t)  t: GUNIT_RANGE_TYPE_CALL(t, (expected), (result), (negate))
#define GUNIT_RANGE_HOOK(expected, result, negate) \
_Generic((expected),                               \
  GUNIT_RANGE_HOOK_TYPE(uint8_t),                  \
  GUNIT_RANGE_HOOK_TYPE(uint16_t),                 \
  GUNIT_RANGE_HOOK_TYPE(uint32_t),                 \
  GUNIT_RANGE_HOOK_TYPE(uint64_t),                 \
  GUNIT_RANGE_HOOK_TYPE(int8_t),                   \
  GUNIT_RANGE_HOOK_TYPE(int16_t),                  \
  GUNIT_RANGE_HOOK_TYPE(int32_t),                  \
  GUNIT_RANGE_HOOK_TYPE(int64_t),                  \
  GUNIT_RANGE_HOOK_TYPE(float),                    \
  GUNIT_RANGE_HOOK_TYPE(double)                    \
)(expected)

/**
 * Function for asserting arrays and objects
 */
gnoopt inline static bool gunit_array(void *expected, void *result, intmax_t size, intmax_t line_number, const char *file, bool no) {
  uint8_t *ex = (uint8_t *) expected;
  uint8_t *re = (uint8_t *) result;

  // Check if equal
  for (uint32_t i = 0; i < size; ++i) {
    if (ex[i] != re[i])
      return gunit_mono_hook_(ex[i], re[i], line_number, file, no);
  }

  // If no differences were found
  return gunit_mono_hook_((intmax_t) expected, (intmax_t) result, line_number, file, !no);
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
    gunit_hook(0, 0, 0, "0", false);
    gunit_range_hook(0, 0, 0, "0", false);
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
#define GFAIL(...) {gunit_fail(__LINE__, __FILE__, (const gunit_function_t[]){__VA_ARGS__}, \
                    sizeof((gunit_function_t[]){__VA_ARGS__}) / sizeof(gunit_function_t));}


/**
 * Assert for boolean
 * Fails if false
 */
#define GBOOL(result) GASSERT((bool) true, (bool) (result))
