mwparallelparser
================

**mwparallelparser** (the *MediaWiki Parallel Parser*) is a Python package
that provides parallel parser for MediaWiki_ wikicode

The name parallel parser refers to idea of `parallel markup`_ proposed
by Ted Nelson. In the parallel markup approach the raw text data and the
formatting information are kept separately. Each formatting tag contains
information about its position in the document. This format has many
advantages over traditional embedded markup.  Among others, it is much more
nautral for many machine learning related topics.

There several key assumptions for the parser, that should be kept in mind:
* The raw text data should be as clean as possible. Parser should remove
any formatting syntax, even when corresponding parallel markup isn't produced.
* The white spaces should be removed if they don't provide any
additional information. That means that several following spaces in the wikicode
should be rendered as one space character if it is a part of a normal paragraph.
Also the empty lines are removed.

Usage
-----
Normal usage is rather straightforward (where ``parallel_wikicode`` is the wikicode):

>>> from mwparallelparser import Parser
>>> parser = Parser()
>>> parallel_wikicode = parser.parse(parallel_wikicode)
>>> print(wikicode['lines'])
>>> print(wikicode['tags'])

The ``wikicode['lines']`` contains the raw text lines, generated from the given wikicode.
The lines are kept in a List (without new line character at the end). Unless specified otherwise
by some tag, each line represents a paragraph. Just like in the original MediaWiki parser,
the paragraphs are `joined to a single output line`_ if they are separated only by one new line
character in a source file.

The ``wikicode['tags']`` contains a List of parallel tags in the document. Each tag is represented by
a Dict with the following structure:

.. code-block:: python

    {
        'type': string,  # tag type, in mwparallelparser usually the same as HTML tag name
        'spans': [       # a List of tags positions in the document
            {'line': int,
             'start': int,
             'length': int},
            {'line': int}
        ],
        'attributes': {} # dictionary of tag attributes. Individual for each tag type.
    }

Each span must be a continuous fragment of the document, but no longer than one line of the output. If the
tag is longer than one line, many spans are defined. There are two types of spans. The first are line spans,
which selects the entire line: ``{'line': int}``. The second are inline spans, that selects only part of a line:
``{'line': int, 'start': int, 'length': int}``. In the inline spans the ``'start'`` defines the index of a first
character inside the span, the ``'length'`` defines number of characters that are included in the span.

wiki link
~~~~~~~~~
The `wiki link`_ tag defines an internal MediaWiki hyperlink to another article in
the **main namespace**. Each wiki link is defined by the tag with the following structure:

.. code-block:: python

    {
        'type': 'link',
        'spans': [
            {'line': int,
             'start': int,
             'length': int}
        ],
        'attributes': {
            'destination': string
        }
    }

Since links cannot exceeds paragraph boundaries, each wiki link has only one span. The ``'destination'``
attribute defines the title of the destination page of a link.


.. _MediaWiki:                        https://www.mediawiki.org
.. _parallel markup:                  https://www.xml.com/pub/a/w3j/s3.nelson.html
.. _joined to a single output line:   https://www.mediawiki.org/wiki/Help:Formatting#Paragraphs
.. _wiki link:                        https://www.mediawiki.org/wiki/Help:Links