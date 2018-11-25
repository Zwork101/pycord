########
API Docs
########

When working with pycord, keep these things in mind.

1. Listener and Events, are usually interchangeable.
2. Objects like Gateway are useful when making plugins and such. TrioGateway is useful for building bots and such.
3. There will be spelling mistaks an d grammical stuff isues. Either deal with it or make a PR with all the issues you
   can find.

******
Models
******

These are the objects that the discord API and gateway will return. You can't modify them all at once by changing a
parent class, however you can switch them out individually. If you do, all other Models that use that Model will use
yours instead. For example, if you set :py:data:`pycord.config.USER` to your own class, Models such as
py:class:`pycord.models.message.Message` will change to use that. (In that case, the author attribute would change).

Channels
========

Channel
-------

.. autoclass:: pycord.models.channel.Channel
    :show-inheritance:
    :members:

Channel Types
-------------

.. autoclass:: pycord.models.channel.ChannelTypes
    :show-inheritance:
    :members:

Emoji
=====

Emoji
-----

.. autoclass:: pycord.models.emoji.Emoji
    :show-inheritance:
    :members:

Reaction
--------

.. autoclass:: pycord.models.message.Reaction
    :show-inheritance:
    :members:

Embed
=====

Embed
-----

.. autoclass:: pycord.models.message.Embed
    :show-inheritance:
    :members:

Embed footer
------------

.. autoclass:: pycord.models.message.EmbedFooter
    :show-inheritance:
    :members:

Embed image
-----------

.. autoclass:: pycord.models.message.EmbedImage
    :show-inheritance:
    :members:

Embed thumbnail
---------------

.. autoclass:: pycord.models.message.EmbedThumbnail
    :show-inheritance:
    :members:

Embed video
-----------

.. autoclass:: pycord.models.message.EmbedVideo
    :show-inheritance:
    :members:

Embed provider
--------------

.. autoclass:: pycord.models.message.EmbedProvider
    :show-inheritance:
    :members:

Embed author
------------

.. autoclass:: pycord.models.message.EmbedAuthor
    :show-inheritance:
    :members:

Embed fields
------------

.. autoclass:: pycord.models.message.EmbedField
    :show-inheritance:
    :members:

Invites
=======

Invite
------

.. autoclass:: pycord.models.invite.Invite
    :show-inheritance:
    :members:

Invite Meta Data
----------------

.. autoclass:: pycord.models.invite.InviteMetadata
    :show-inheritance:
    :members:

Messages
========

Message
-------

.. autoclass:: pycord.models.message.Message
    :show-inheritance:
    :members:

Message types
-------------

.. autoclass:: pycord.models.message.MessageTypes
    :show-inheritance:
    :members:

Message activity
----------------

.. autoclass:: pycord.models.message.MessageActivity
    :show-inheritance:
    :members:

Message activity types
----------------------

.. autoclass:: pycord.models.message.MessageActivityType
    :show-inheritance:
    :members:

Message application
-------------------

.. autoclass:: pycord.models.message.MessageApplication
    :show-inheritance:
    :members:

Attachment
----------

.. autoclass:: pycord.models.message.Attachment
    :show-inheritance:
    :members:

Snowflake
=========

.. autoclass:: pycord.models.snowflake.Snowflake
    :show-inheritance:
    :members:

User
====

.. autoclass:: pycord.models.user.User
    :show-inheritance:
    :members:

Webhook
=======

.. autoclass:: pycord.models.webhook.Webhook
    :show-inheritance:
    :members:
