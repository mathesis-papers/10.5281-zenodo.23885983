import itertools
import json
import random
from fractions import Fraction


def matrix(rows):
    return [[Fraction(value) for value in row] for row in rows]


def identity(size):
    return matrix([[int(row == column) for column in range(size)] for row in range(size)])


def transpose(source):
    return [list(column) for column in zip(*source)]


def multiply(left, right):
    columns = transpose(right)
    return [[sum(first * second for first, second in zip(row, column))
             for column in columns] for row in left]


def inverse(source):
    size = len(source)
    augmented = [row[:] + unit for row, unit in zip(source, identity(size))]
    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column]), None)
        if pivot is None:
            raise ValueError('singular')
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        factor = augmented[column][column]
        augmented[column] = [entry / factor for entry in augmented[column]]
        for row in range(size):
            if row != column:
                factor = augmented[row][column]
                augmented[row] = [entry - factor * base
                                  for entry, base in zip(augmented[row], augmented[column])]
    return [row[size:] for row in augmented]


def absolute(source):
    return [[abs(entry) for entry in row] for row in source]


def objective_matrix(source):
    return multiply(absolute(source), absolute(inverse(source)))


def unit_spectrum_certificate(source):
    size = len(source)
    unit = identity(size)
    residual = [[source[row][column] - unit[row][column]
                 for column in range(size)] for row in range(size)]
    power = unit
    for iteration in range(size):
        power = multiply(power, residual)
    return all(entry == 0 for row in power for entry in row)


def triangular_permutations_exist(source):
    size = len(source)
    permutations = list(itertools.permutations(range(size)))
    return any(all(source[rows[row]][columns[column]] == 0
                   for row in range(size) for column in range(row + 1, size))
               for rows in permutations for columns in permutations)


def rational_orthogonal(size, generator):
    orthogonal = identity(size)
    if size > 1:
        for iteration in range(2 * size):
            first, second = generator.sample(range(size), 2)
            rotation = identity(size)
            rotation[first][first] = rotation[second][second] = Fraction(3, 5)
            rotation[first][second] = Fraction(-4, 5)
            rotation[second][first] = Fraction(4, 5)
            orthogonal = multiply(orthogonal, rotation)
    assert multiply(transpose(orthogonal), orthogonal) == identity(size)
    return orthogonal


def signed_permutation(size, generator):
    columns = list(range(size))
    generator.shuffle(columns)
    result = matrix([[0] * size for row in range(size)])
    for row, column in enumerate(columns):
        result[row][column] = generator.choice([-1, 1])
    return result


def main():
    generator = random.Random(515549)
    exhaustive_count = 0
    equality_count = 0
    for values in itertools.product(range(-2, 3), repeat=4):
        source = matrix([values[:2], values[2:]])
        try:
            product = objective_matrix(source)
        except ValueError:
            continue
        assert product[0][0] >= 1 and product[1][1] >= 1
        certificate = unit_spectrum_certificate(product)
        assert certificate == triangular_permutations_exist(source)
        exhaustive_count += 1
        equality_count += int(certificate)

    random_counts = {}
    for size, target in [(3, 256), (4, 64)]:
        count = 0
        while count < target:
            source = matrix([[generator.randint(-3, 3) for column in range(size)]
                             for row in range(size)])
            try:
                product = objective_matrix(source)
            except ValueError:
                continue
            assert unit_spectrum_certificate(product) == triangular_permutations_exist(source)
            assert all(product[row][column] >= int(row == column)
                       for row in range(size) for column in range(size))
            count += 1
        random_counts[str(size)] = count

    constructed_count = 0
    invariance_count = 0
    for size in range(1, 9):
        for sample in range(8):
            lower = matrix([[generator.randint(-4, 4) if column < row else
                             generator.randint(1, 4) if column == row else 0
                             for column in range(size)] for row in range(size)])
            orthogonal = rational_orthogonal(size, generator)
            source = multiply(lower, transpose(orthogonal))
            attaining = multiply(source, orthogonal)
            assert attaining == lower
            product = objective_matrix(attaining)
            assert all(product[row][column] == 0 for row in range(size)
                       for column in range(row + 1, size))
            assert all(product[index][index] == 1 for index in range(size))
            assert unit_spectrum_certificate(product)
            constructed_count += 1
            for trial in range(3):
                signed = signed_permutation(size, generator)
                assert objective_matrix(multiply(attaining, signed)) == product
                invariance_count += 1

    source = matrix([[Fraction(3, 5), Fraction(4, 5)],
                     [Fraction(-1, 5), Fraction(7, 5)]])
    orthogonal = matrix([[Fraction(3, 5), Fraction(-4, 5)],
                         [Fraction(4, 5), Fraction(3, 5)]])
    lower = matrix([[1, 0], [1, 1]])
    assert multiply(source, orthogonal) == lower
    assert multiply(transpose(orthogonal), orthogonal) == identity(2)
    assert objective_matrix(lower) == matrix([[1, 0], [2, 1]])
    residual = matrix([[0, 0], [2, 0]])
    assert multiply(residual, residual) == matrix([[0, 0], [0, 0]])
    assert objective_matrix(source) == matrix([[1, Fraction(24, 25)],
                                             [Fraction(14, 25), 1]])
    assert Fraction(24, 25) * Fraction(14, 25) == Fraction(16 * 21, 625)

    diagonal = matrix([[1, 0], [0, 2]])
    unnormalized = matrix([[1, -1], [1, 1]])
    left = absolute(multiply(diagonal, unnormalized))
    right = absolute(multiply(transpose(unnormalized), inverse(diagonal)))
    balanced_product = [[entry / 2 for entry in row] for row in multiply(left, right)]
    assert [sum(row) for row in right] == [Fraction(3, 2), Fraction(3, 2)]
    assert balanced_product == matrix([[1, Fraction(1, 2)], [2, 1]])
    assert balanced_product[0][1] * balanced_product[1][0] == 1

    print(json.dumps({
        'arithmetic': 'fractions.Fraction; exact, no floating-point eigenvalues',
        'seed': 515549,
        'exhaustive_nonsingular_2x2_entries_minus2_to2': exhaustive_count,
        'unit_spectrum_cases_in_exhaustive_2x2': equality_count,
        'random_equality_characterization_cases': random_counts,
        'constructed_attainment_cases_dimensions_1_to_8': constructed_count,
        'signed_permutation_invariance_cases': invariance_count,
        'rational_nonidentity_defective_example': 'passed',
        'balancing_and_spectral_incompatibility_example': 'passed',
        'scope': 'Finite exact rational controls for the enumerated cases; the universal results have written proofs in the note.',
        'status': 'passed',
    }, indent=2))


if __name__ == '__main__':
    main()
