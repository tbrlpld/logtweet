# -*- coding: utf-8 -*-

"""Fixtures shared among the tests."""

from bs4 import BeautifulSoup
import pytest


@pytest.fixture
def example_soup():
    """Create soup object for example page."""
    page_content = """<html>
<body>
<h1>100 Days Of Code - Log</h1>
<h2>Day 1: October 16, 2019, Wednesday</h2>
<h3>Today&#39;s Progress</h3>
<p>Gone through first bit of Flask introduction and set up the basic project structure in #100DayOfWebInPython.
Also, enabled Markdown formatting for posts in the Flaskr blog app (as suggested in the &#34;Keep Developing&#34; section of the Flask tutorial).</p>
<h3>Thoughts</h3>
<p>I have used Flask before, but the <code>.flaskenv</code> file for the <code>python-dotenv</code> package to set the environment variable automatically is a nice addition to simplify the setup (and distribution I guess).</p>
<p><code>markupsafe.escape()</code> can be used to sanitize user input on the sever side.</p>
<h3>Link(s) to work</h3>
<ol>
<li><a href="http://example.com/1">Example Link 1</a></li>
<li><a href="http://example.com/2">Example Link 2</a></li>
<li><a href="http://example.com/3">Example Link 3</a></li>
</ol>
<h2>Day 2: October 17, 2019, Thursday</h2>
<h3>Today&#39;s Progress</h3>
<p>Gone through first bit of Flask introduction and set up the basic project structure in #100DayOfWebInPython.
Also, enabled Markdown formatting for posts in the Flaskr blog app (as suggested in the &#34;Keep Developing&#34; section of the Flask tutorial).</p>
<h3>Thoughts</h3>
<p>I have used Flask before, but the <code>.flaskenv</code> file for the <code>python-dotenv</code> package to set the environment variable automatically is a nice addition to simplify the setup (and distribution I guess).</p>
<p><code>markupsafe.escape()</code> can be used to sanitize user input on the sever side.</p>
<h3>Link(s) to work</h3>
<ol>
<li><a href="http://example.com/4">Example Link 4</a></li>
<li><a href="http://example.com/5">Example Link 5</a></li>
<li><a href="http://example.com/6">Example Link 6</a></li>
</ol>

</body>
</html>"""
    return BeautifulSoup(page_content, "html.parser")

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
