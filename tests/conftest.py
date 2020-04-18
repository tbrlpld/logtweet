# -*- coding: utf-8 -*-

"""Fixtures shared among the tests."""

from datetime import date

from bs4 import BeautifulSoup
import pytest


@pytest.fixture
def example_soup():
    """Create soup object for example page."""

    # Does it make sense to pull the actual formatting from a template?
    # I keep referencing my own log. It would be good to create an actual
    # template that can easily be reused.
    # This makes more sense once I base the input on markdown and not on html.
    # The problem would be that the tests have an outside dependency, that
    # could fail for any reason (network, URL change, etc. )
    # I could try this with a git submodule. Including the template repo as a
    # submodule would make it available locally. They would still be connected.

    page_content = """<html>
<body>
<h1>100 Days Of Code - Log</h1>
<h2>Day 1: October 16, 2019, Wednesday</h2>
<h3>Today&#39;s Progress</h3>
<p>It's the first paragraph. It's 50 characters long.</p>
<p>The second paragraph. This is one that's 60 characters long.</p>
<h3>Thoughts</h3>
<p>I have used Flask before, but the <code>.flaskenv</code> file for the <code>python-dotenv</code> package to set the environment variable automatically is a nice addition to simplify the setup (and distribution I guess).</p>
<p><code>markupsafe.escape()</code> can be used to sanitize user input on the sever side.</p>
<h3>Link(s)</h3>
<ol>
<li><a href="http://example.com/1">Example Link 1</a></li>
<li><a href="http://example.com/2">Example Link 2</a></li>
<li><a href="http://example.com/3">Example Link 3</a></li>
</ol>
<h2>Day 2: October 17, 2019, Thursday</h2>
<h3>Today&#39;s Progress</h3>
<p></p>
<h3>Thoughts</h3>
<p>I have used Flask before, but the <code>.flaskenv</code> file for the <code>python-dotenv</code> package to set the environment variable automatically is a nice addition to simplify the setup (and distribution I guess).</p>
<p><code>markupsafe.escape()</code> can be used to sanitize user input on the sever side.</p>
<h3>Link(s)</h3>
<ol>
<li><a href="http://example.com/4">Example Link 4</a></li>
<li><a href="http://example.com/5">Example Link 5</a></li>
<li><a href="http://example.com/6">Example Link 6</a></li>
</ol>

</body>
</html>"""
    return BeautifulSoup(page_content, "html.parser")

@pytest.fixture
def test_file(tmp_path):
    return tmp_path / "test.txt"


# Page content for reference
# <html>
#     <body>
#     <h1>100 Days Of Code - Log</h1>
#     <h2>Day 1: October 16, 2019, Wednesday</h2>
#     <h3>Today&#39;s Progress</h3>
#     <p>Gone through first bit of Flask introduction and set up the basic project structure in #100DayOfWebInPython.
#     Also, enabled Markdown formatting for posts in the Flaskr blog app (as suggested in the &#34;Keep Developing&#34; section of the Flask tutorial).</p>
#     <h3>Thoughts</h3>
#     <p>I have used Flask before, but the <code>.flaskenv</code> file for the <code>python-dotenv</code> package to set the environment variable automatically is a nice addition to simplify the setup (and distribution I guess).</p>
#     <p><code>markupsafe.escape()</code> can be used to sanitize user input on the sever side.</p>
#     <h3>Link(s) to work</h3>
#     <ol>
#       <li><a href="http://example.com/1">Example Link 1</a></li>
#       <li><a href="http://example.com/2">Example Link 2</a></li>
#       <li><a href="http://example.com/3">Example Link 3</a></li>
#     </ol>
#     </body>
# </html>
