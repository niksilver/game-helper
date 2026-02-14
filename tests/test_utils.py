import pytest

from gamehelper.utils import optimise


class TestOptimise:
    """Tests for the optimise() function."""

    def _target_assessment(self, target):
        """Return an assessment function that targets a specific value."""
        def assess(value):
            if value < target:
                return (-1, False)
            elif value > target:
                return (1, False)
            else:
                return (0, True)
        return assess

    def test_initial_guess_is_just_right(self):
        """Should return immediately if initial guess is just right."""
        result = optimise(42, self._target_assessment(42))
        assert result == 42

    def test_initial_guess_too_small(self):
        """Should search upward when initial guess is too small."""
        result = optimise(5, self._target_assessment(42))
        assert result == 42

    def test_initial_guess_too_large(self):
        """Should search downward when initial guess is too large."""
        result = optimise(100, self._target_assessment(42))
        assert result == 42

    def test_initial_guess_of_one(self):
        """Should work when starting from 1."""
        result = optimise(1, self._target_assessment(50))
        assert result == 50

    def test_different_guesses_find_same_answer(self):
        """Different starting points should converge on the same answer."""
        target = 73
        assess = self._target_assessment(target)
        assert optimise(1,    assess) == target
        assert optimise(10,   assess) == target
        assert optimise(73,   assess) == target
        assert optimise(200,  assess) == target
        assert optimise(1000, assess) == target

    def test_no_exact_match_returns_best_acceptable(self):
        """When no exact match exists, should return the best acceptable value."""
        # Values below 10 are too small and not acceptable.
        # Values 10-15 are too small but acceptable.
        # Values above 15 are too large and not acceptable.
        def assess(value):
            if value < 10:
                return (-1, False)
            elif value <= 15:
                return (-1, True)
            else:
                return (1, False)

        # Initial guess below the acceptable range
        result = optimise(3, assess)
        assert 10 <= result <= 15

        # Initial guess above the acceptable range
        result = optimise(50, assess)
        assert 10 <= result <= 15

        # Initial guess within the acceptable range
        result = optimise(12, assess)
        assert 10 <= result <= 15

    def test_negative_target_raises_error(self):
        """When the target is negative, it can't be found and should raise ValueError."""
        assess = self._target_assessment(-5)

        with pytest.raises(ValueError):
            optimise(1, assess)

        with pytest.raises(ValueError):
            optimise(100, assess)

    def test_always_too_small_raises_error(self):
        """When assessment always says too small, should raise ValueError."""
        def assess(value):
            return (-1, False)

        with pytest.raises(ValueError):
            optimise(1, assess)

        with pytest.raises(ValueError):
            optimise(100, assess)
