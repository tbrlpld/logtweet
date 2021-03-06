# -*- coding: utf-8 -*-


class TestCreateTweetHistoryMsg(object):
    """Tests for ``create_tweet_history_msg`` function."""

    def test_turn_multiline_tweet_into_single_line_history_msg(self):
        tweet_content = "This is a\n\nmultiline\n\ntweet."
        expected_msg = "This is a  multiline  tweet."
        from logtweet.history import create_tweet_history_msg

        actual_msg = create_tweet_history_msg(tweet_content)

        assert actual_msg == expected_msg


class TestIsStringInFile(object):
    """Tests for ``is_string_in_filelines`` function."""

    def test_finds_string_alone_in_line(self, test_file):
        search_string = "This is what I am looking for."
        file_content = f"""This is some thing.
{search_string}
This is something else."""
        test_file.write_text(file_content)
        from logtweet.history import is_string_in_filelines

        found = is_string_in_filelines(
            search_string,
            filepath=test_file.as_posix(),
        )

        assert found is True

    def test_finds_string_with_prefix_in_line(self, test_file):
        search_string = "This is what I am looking for."
        file_content = f"""This is some thing.
Here is something, but '{search_string}' is in this line too.
This is something else."""
        test_file.write_text(file_content)
        from logtweet.history import is_string_in_filelines

        found = is_string_in_filelines(
            search_string,
            filepath=test_file.as_posix(),
        )

        assert found is True

    def test_false_for_string_not_in_file(self, test_file):
        search_string = "This is what I am looking for."
        file_content = f"""This is some thing.
This is NOT what I am looking for.
This is something else."""
        test_file.write_text(file_content)
        from logtweet.history import is_string_in_filelines

        found = is_string_in_filelines(
            search_string,
            filepath=test_file.as_posix(),
        )

        assert found is False


class TestAddTweetToHistory(object):
    """Tests for ``add_tweet_to_history`` function."""

    def test_adding_tweet_as_one_line_to_history_file(
        self,
        monkeypatch,
        test_file,
    ):
        test_filepath = str(test_file.as_posix())
        tweet_content = "This is a\n\nmultiline\n\ntweet."

        from logtweet.history import add_tweet_to_history
        add_tweet_to_history(tweet_content, history_filepath=test_filepath)

        # Can be tested with ``create_tweet_history_msg`` and ``is_string_in_filelines``
        from logtweet.history import create_tweet_history_msg, is_string_in_filelines
        tweet_history_msg = create_tweet_history_msg(tweet_content)
        assert is_string_in_filelines(tweet_history_msg, filepath=test_filepath)

    def test_after_multiple_execution_all_tweets_in_history(
        self,
        test_file,
    ):
        test_filepath = test_file.as_posix()
        tweet1_content = "This is a\n\nmultiline\n\ntweet."
        tweet2_content = "This is another tweet."

        from logtweet.history import add_tweet_to_history
        add_tweet_to_history(tweet1_content, history_filepath=test_filepath)
        add_tweet_to_history(tweet2_content, history_filepath=test_filepath)

        # Can be tested with ``create_tweet_history_msg`` and ``is_string_in_filelines``
        from logtweet.history import create_tweet_history_msg, is_string_in_filelines
        tweet1_history_msg = create_tweet_history_msg(tweet1_content)
        tweet2_history_msg = create_tweet_history_msg(tweet2_content)
        assert is_string_in_filelines(tweet1_history_msg, filepath=test_filepath)
        assert is_string_in_filelines(tweet2_history_msg, filepath=test_filepath)

    def test_number_of_executions_corresponds_to_filelines(
        self,
        test_file,
    ):
        """
        Test that number of executions leads to same number of lines in file.

        This is to make sure that the formatting in the file is fine and every
        message is written into a single line.
        """
        test_filepath = test_file.as_posix()
        tweet1_content = "This is a\n\nmultiline\n\ntweet."
        tweet2_content = "This is another tweet."

        from logtweet.history import add_tweet_to_history
        add_tweet_to_history(tweet1_content, history_filepath=test_filepath)
        add_tweet_to_history(tweet2_content, history_filepath=test_filepath)

        with open(test_filepath, "r") as test_fileobj:
            lines = test_fileobj.readlines()
        assert len(lines) == 2


class TestIsTweetInHistory(object):
    """Test for ``is_tweet_in_history`` function."""

    def test_finds_multiline_tweet_if_in_history_as_one_line(
        self,
        test_file,
    ):
        tweet_content = "This is a\n\nmultiline\n\ntweet."
        from logtweet.history import create_tweet_history_msg
        tweet_history_msg = create_tweet_history_msg(tweet_content)
        test_file_content = f"""This is something.
{tweet_history_msg}
This is some more."""
        test_file.write_text(test_file_content)
        from logtweet.history import is_tweet_in_history

        found = is_tweet_in_history(
            tweet_content,
            history_filepath=test_file.as_posix(),
        )

        assert found is True

    def test_finds_tweet_if_in_history_with_prefix(
        self,
        test_file,
    ):
        """Test history message with prefix in file."""
        tweet_content = "This is a\n\nmultiline\n\ntweet."
        from logtweet.history import create_tweet_history_msg
        tweet_history_msg = create_tweet_history_msg(tweet_content)
        test_file_content = f"""This is something.
Here is something. But '{tweet_history_msg}' is here too.
This is some more."""
        test_file.write_text(test_file_content)
        from logtweet.history import is_tweet_in_history

        found = is_tweet_in_history(
            tweet_content,
            history_filepath=test_file.as_posix(),
        )

        assert found is True

    def test_false_if_tweet_not_in_history(
        self,
        test_file,
    ):
        """Test false if no history message in file."""
        tweet_content = "This is a\n\nmultiline\n\ntweet."
        test_file_content = f"""This is something.
This is some more."""
        test_file.write_text(test_file_content)
        from logtweet.history import is_tweet_in_history

        found = is_tweet_in_history(
            tweet_content,
            history_filepath=test_file.as_posix(),
        )

        assert found is False
