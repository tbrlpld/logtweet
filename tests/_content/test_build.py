# -*- coding: utf-8 -*-

"""Test functions regarding creation of the tweet."""

import pytest  # type: ignore


class TestMakePreamble(object):
    """Tests for `make_preamble` function."""

    @pytest.mark.parametrize(
        "day_number, expected_return",
        [
            (1, "1/#100DaysOfCode"),
            (2, "2/#100DaysOfCode"),
            (10, "10/#100DaysOfCode"),
            (99, "99/#100DaysOfCode"),
            (100, "100/#100DaysOfCode"),
            (999, "999/#100DaysOfCode"),
        ],
    )
    def test_valid_int_inputs(self, day_number, expected_return):
        """Return the correct preamble for a given heading string."""
        from logtweet._content.build import make_preamble
        actual_return = make_preamble(day_number)

        assert actual_return == expected_return

    @pytest.mark.parametrize(
        "day_number, received_type",
        [
            ("1", "str"),
        ],
    )
    def test_exception_if_invalid_day_number_type(
        self,
        day_number,
        received_type,
    ):
        """Raise exception for invalid formatted heading strings."""
        from logtweet._content.build import make_preamble
        with pytest.raises(
            TypeError,
            match=r"^Expected 'int', got '{0}'.*$".format(received_type),
        ):
            make_preamble(day_number)
