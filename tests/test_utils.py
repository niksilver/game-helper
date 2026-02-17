import pytest

from gamehelper.utils import optimise, box


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


class TestBox:
    """Tests for the box() function."""

    def test_box(self):
        """Should calculate the missing values from the given ones."""

        # left + width → right
        assert box(left           = 10,
                   top            = 20,
                   width          = 100,
                   height         = 50,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 20, 110, 70, 100, 50)

        # left + right → width
        assert box(left           = 10,
                   top            = 20,
                   right          = 110,
                   bottom         = 70,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 20, 110, 70, 100, 50)

        # right + width → left
        assert box(top            = 20,
                   right          = 110,
                   width          = 100,
                   height         = 50,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 20, 110, 70, 100, 50)

        # top + height → bottom
        assert box(left           = 0,
                   top            = 10,
                   width          = 50,
                   height         = 30,
                   default_width  = 200,
                   default_height = 200,
                   ) == (0, 10, 50, 40, 50, 30)

        # top + bottom → height
        assert box(left           = 0,
                   top            = 10,
                   width          = 50,
                   bottom         = 40,
                   default_width  = 200,
                   default_height = 200,
                   ) == (0, 10, 50, 40, 50, 30)

        # bottom + height → top
        assert box(left           = 0,
                   width          = 50,
                   bottom         = 40,
                   height         = 30,
                   default_width  = 200,
                   default_height = 200,
                   ) == (0, 10, 50, 40, 50, 30)

        # Only left given → width defaults to default_width
        assert box(left           = 10,
                   top            = 0,
                   height         = 50,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 0, 210, 50, 200, 50)

        # Only top given → height defaults to default_height
        assert box(left           = 0,
                   top            = 10,
                   width          = 50,
                   default_width  = 200,
                   default_height = 100,
                   ) == (0, 10, 50, 110, 50, 100)

        # center + width → left and right
        assert box(center         = 60,
                   top            = 0,
                   width          = 100,
                   height         = 50,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 0, 110, 50, 100, 50)

        # center + left → right and width
        assert box(left           = 10,
                   center         = 60,
                   top            = 0,
                   height         = 50,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 0, 110, 50, 100, 50)

        # center + right → left and width
        assert box(center         = 60,
                   right          = 110,
                   top            = 0,
                   height         = 50,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 0, 110, 50, 100, 50)

        # middle + height → top and bottom
        assert box(left           = 0,
                   width          = 50,
                   middle         = 25,
                   height         = 30,
                   default_width  = 200,
                   default_height = 200,
                   ) == (0, 10, 50, 40, 50, 30)

        # middle + top → bottom and height
        assert box(left           = 0,
                   width          = 50,
                   top            = 10,
                   middle         = 25,
                   default_width  = 200,
                   default_height = 200,
                   ) == (0, 10, 50, 40, 50, 30)

        # middle + bottom → top and height
        assert box(left           = 0,
                   width          = 50,
                   middle         = 25,
                   bottom         = 40,
                   default_width  = 200,
                   default_height = 200,
                   ) == (0, 10, 50, 40, 50, 30)

        # Only center given → width defaults to default_width
        assert box(center         = 110,
                   top            = 0,
                   height         = 50,
                   default_width  = 200,
                   default_height = 200,
                   ) == (10, 0, 210, 50, 200, 50)

        # Only middle given → height defaults to default_height
        assert box(left           = 0,
                   width          = 50,
                   middle         = 60,
                   default_width  = 200,
                   default_height = 100,
                   ) == (0, 10, 50, 110, 50, 100)

        # Too many horizontal values → error
        with pytest.raises(ValueError):
            box(left           = 10,
                right          = 110,
                top            = 0,
                height         = 50,
                width          = 100,
                default_width  = 200,
                default_height = 200,
                )

        with pytest.raises(ValueError):
            box(left           = 10,
                center         = 60,
                right          = 110,
                top            = 0,
                height         = 50,
                default_width  = 200,
                default_height = 200,
                )

        # Too many vertical values → error
        with pytest.raises(ValueError):
            box(left           = 0,
                width          = 50,
                top            = 10,
                bottom         = 40,
                height         = 30,
                default_width  = 200,
                default_height = 200,
                )

        with pytest.raises(ValueError):
            box(left           = 0,
                width          = 50,
                top            = 10,
                middle         = 25,
                bottom         = 40,
                default_width  = 200,
                default_height = 200,
                )

        # No horizontal values → error
        with pytest.raises(ValueError):
            box(top            = 0,
                height         = 50,
                default_width  = 200,
                default_height = 200,
                )

        # No vertical values → error
        with pytest.raises(ValueError):
            box(left           = 0,
                width          = 50,
                default_width  = 200,
                default_height = 200,
                )
