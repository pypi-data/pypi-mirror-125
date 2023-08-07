ctq
===

A library of resource tree helps targeted at the pyramid framework.

Constructing a resource tree
----------------------------

Pyramid when seeking to find an context object in a resource tree takes a URL
such as ``/books/bible`` and atempts to traverse a root object treating the
root object as tree of mappings. So the above URL resolves in the context
object of ``root["books"]["bible"]``

``ctq`` aids in the construction of these a resource trees by being able to
decorate factory methods mapping them to item looksup::

    >>> from ctq import Resourceful, resource

    >>> class Root(Resourceful):
    ...
    ...     @resource('books')
    ...     def get_books(self):
    ...         return Shelf()

    >>> class Shelf(Resourceful):
    ...
    ...     @resource("bible")
    ...     def get_bible(self):
    ...         return Bible()

    >>> class Bible(object):
    ...     pass


``Resourceful`` is a class that is intended to be mixed into resource objects
with gives a mapping behavior for methods that are decorated with
``@resource``::

    >>> root = Root()
    >>> root["books"]["bible"]
    <Bible object at ...>

``Resourceful`` implements caching so subsiquent look ups of the same object result
in the same object being returned.::

    >>> a = root["books"]
    >>> b = root["books"]
    >>> a is b
    True

The resource decorator adds ``__parent__`` and ``__name__`` attributes which
pyramid expects for its traversal operations.::

    >>> books = root["books"]
    >>> books.__name__
    'books'
    >>> books.__parent__
    <Root object at ...>

Additionally if the factory fucntion returns an object with the parent and name
attributes already defined then it will not override them. This allows
sym-links within the traversal tree.::

    >>> class LinkExample(Resourceful):
    ...
    ...     @resource('shelf-1')
    ...     def get_shelf1(self):
    ...         return Shelf()
    ...
    ...     @resource('shelf-2')
    ...     def get_shelf2(self):
    ...         return Shelf()
    ...
    ...     @resource('shelf-default')
    ...     def get_shelf_default(self):
    ...         return self['shelf-1']

    >>> root2 = LinkExample()
    >>> root2['shelf-1'].__name__
    'shelf-1'
    >>> root2['shelf-2'].__name__
    'shelf-2'
    >>> root2['shelf-default'].__name__
    'shelf-1'

Event Handling
--------------

cqt provides a function ``emit(target: Any, name: str, data: Optional[dict])``
which creates an event object, searches and calls event handlers starting with
the target and bubbeling up to the root of a resource tree.

Event handlers can be declared using the ``@handle(*event_names, priority:
Optional[int])`` decorator on an instance method which accepts the paramiter
``event``.

For example::

    >>> from ctq import handle
    >>> from ctq import emit

    >>> class EventTreeRoot(object):
    ...
    ...     @handle('after-edit')
    ...     def on_after_edit(self, event):
    ...         print("Was very edited.")

    >>> class Foo(object):
    ...
    ...     @handle('after-edit')
    ...     def on_after_edit(self, event):
    ...         print("Was edited.")

    >>> foo = Foo()
    >>> foo.__parent__ = EventTreeRoot()

    >>> emit(foo, 'after-edit')
    Was edited.
    Was very edited.

Workflow behavior
-----------------

cqt provides a ``Workflowable`` class to add workflow behavior to objects this
adds some methods that are handy in performing workflow state transitions on
objects including emmiting events and guarding agenst illegal transitions.

The current workflow is get/set on the property ``self.workflow_state`` and
transitions are defined in the property ``self.workflow_transitions``. Events
emitted that the form ``workflow-before-ACTION`` and ``workflow-after-ACTION``

For example::

    >>> from ctq import Workflowable

    >>> class Document(Workflowable):
    ...
    ...     workflow_state = "new"
    ...
    ...     workflow_transitions = {
    ...         "submit-for-review": {"from": ["new"], "to": "pending-review"},
    ...         "publish": {"from": ["new", "pending-review"], "to": "public"},
    ...         "retract": {"from": ["public"], "to": "retracted"},
    ...     }
    ...
    ...     @handle("workflow-before-publish")
    ...     def on_before_publish(self, event):
    ...         print("about to publish")
    ...
    ...     @handle("workflow-after-publish")
    ...     def on_after_publish(self, event):
    ...         print("published!")

To action a workflow transition calle the ``self.workflow_action(action)``
method::
    
    >>> doc = Document()
    >>> doc.workflow_state
    'new'
    >>> doc.workflow_action("publish")
    about to publish
    published!
    >>> doc.workflow_state
    'public'
    >>> doc.workflow_action("publish")
    Traceback (most recent call last):
    ...
    ctq.workflow.WorkflowIllegalTransitionError: Can not publish on an instance of Document in the state public

Helper methods
--------------

Additionally there are some functions that enable performing verious tasks
around the tree

Traversing back up the tree with ``traverse_up(obj)``::

    >>> from ctq import traverse_up

    >>> context = root["books"]["bible"]
    >>> list(traverse_up(context))
    [<Bible object at ...>, <Shelf object at ...>, <Root object at ...>]

Getting the root object with ``get_root(obj)``::

    >>> from ctq import get_root

    >>> get_root(context)
    <Root object at ...>

Getting the path names of an object with ``resource_path_names(obj)``::

    >>> from ctq import resource_path_names

    >>> resource_path_names(context)
    ('', 'books', 'bible')

Use acquisition using with ``acquire(obj)``::

    >>> from ctq import acquire

    >>> root.site_name = "Small room with lots of books"
    >>> acquire(context).site_name
    'Small room with lots of books'

