from collections.abc import Callable


def optimise(initial_guess:  int,
             assessment:     Callable[[int], tuple[int, bool]],
             ) -> int:
    """
    Find an optimal integer value by trial and error.
    Only searches values >= 1.

    `assessment` takes a value and returns `(direction, acceptable)` where
    `direction` is negative (too small), positive (too large), or zero
    (just right), and `acceptable` is True if this value is good enough
    if nothing better is found.

    Raises `ValueError` if no acceptable value can be found.
    """
    MAX_EXPANSIONS  = 64
    best_acceptable = None

    def assess_and_track(value):
        nonlocal best_acceptable
        direction, acceptable = assessment(value)
        if acceptable:
            best_acceptable = value
        return direction

    # Assess the initial guess
    direction = assess_and_track(initial_guess)
    if direction == 0:
        return initial_guess

    # Find bounds by expanding in the appropriate direction
    lo = initial_guess
    hi = initial_guess

    if direction < 0:
        # Too small — expand upward
        hi = max(initial_guess * 2, 1)
        for _ in range(MAX_EXPANSIONS):
            if assess_and_track(hi) >= 0:
                break
            hi = hi * 2
    else:
        # Too large — expand downward
        lo = max(initial_guess // 2, 1)
        while lo > 1 and assess_and_track(lo) > 0:
            lo = max(lo // 2, 1)

    # Binary search between lo and hi
    while lo < hi:
        mid       = (lo + hi) // 2
        direction = assess_and_track(mid)

        if direction == 0:
            return mid
        elif direction < 0:
            lo = mid + 1
        else:
            hi = mid - 1

    # Check the final converged value
    assess_and_track(lo)
    if best_acceptable is not None:
        return best_acceptable

    raise ValueError("Could not find an acceptable value")


def box(left:           float | None = None,
        top:            float | None = None,
        right:          float | None = None,
        bottom:         float | None = None,
        width:          float | None = None,
        height:         float | None = None,
        center:         float | None = None,
        middle:         float | None = None,
        default_width:  float        = 100,
        default_height: float        = 100,
        ) -> tuple[float, float, float, float, float, float]:
    """
    Calculate a complete box from partial parameters.

    For each axis, exactly 2 of the values must be determinable.
    Horizontal: `left`, `right`, `width`, `center`.
    Vertical: `top`, `bottom`, `height`, `middle`.
    If only 1 is given, `default_width` or `default_height` fills in
    for `width` or `height` respectively.

    Raises `ValueError` if too many or too few values are given.

    Returns `(left, top, right, bottom, width, height)`.
    """

    # Horizontal axis — resolve center into left or right
    h_count = sum(x is not None for x in (left, right, width, center))
    if h_count == 0:
        raise ValueError("Must specify at least one of left, right, width, center")
    if h_count > 2:
        raise ValueError("Too many horizontal values specified")
    if h_count == 1 and width is None:
        width = default_width
    if center is not None:
        if width is not None:
            left  = center - width / 2
            right = center + width / 2
        elif left is not None:
            right = left + 2 * (center - left)
        elif right is not None:
            left = right - 2 * (right - center)

    if left is None:
        left  = right - width
    if width is None:
        width = right - left
    if right is None:
        right = left + width

    # Vertical axis — resolve middle into top or bottom
    v_count = sum(x is not None for x in (top, bottom, height, middle))
    if v_count == 0:
        raise ValueError("Must specify at least one of top, bottom, height, middle")
    if v_count > 2:
        raise ValueError("Too many vertical values specified")
    if v_count == 1 and height is None:
        height = default_height
    if middle is not None:
        if height is not None:
            top    = middle - height / 2
            bottom = middle + height / 2
        elif top is not None:
            bottom = top + 2 * (middle - top)
        elif bottom is not None:
            top = bottom - 2 * (bottom - middle)

    if top is None:
        top    = bottom - height
    if height is None:
        height = bottom - top
    if bottom is None:
        bottom = top + height

    return (left, top, right, bottom, width, height)
