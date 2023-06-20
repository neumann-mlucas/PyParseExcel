from interpreter import formula_resolver

if __name__ == "__main__":
    test = "1 * (2 + 3)"
    r = formula_resolver(test)
    print("f{test} -> {r}")
