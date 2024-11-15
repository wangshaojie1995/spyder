# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Helper classes to get and set shortcuts in Spyder.
"""

# Standard library imports
from typing import Callable, Optional

# Third-party imports
from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import QShortcut, QWidget

# Local imports
from spyder.config.manager import CONF
from spyder.plugins.shortcuts.utils import (
    ShortcutData,
    SHORTCUTS_FOR_WIDGETS_DATA,
)


class SpyderShortcutsMixin:
    """Provide methods to get, set and register shortcuts."""

    def get_shortcut(
        self,
        name: str,
        context: Optional[str] = None,
        plugin_name: Optional[str] = None,
    ) -> str:
        """
        Get a shortcut sequence stored under the given name and context.

        Parameters
        ----------
        name: str
            The shortcut name (e.g. "run cell").
        context: str, optional
            Name of the shortcut context, e.g. "editor" for shortcuts that have
            effect when the Editor is focused or "_" for global shortcuts. If
            not set, the widget's CONF_SECTION will be used as context.
        plugin_name: str, optional
            Name of the plugin where the shortcut is defined. This is necessary
            for third-party plugins that have shortcuts with a context
            different from the plugin name.

        Returns
        -------
        shortcut: str
            Key sequence of the shortcut.

        Raises
        ------
        configparser.NoOptionError
            If the shortcut does not exist in the configuration.
        """
        context = self.CONF_SECTION if context is None else context
        return CONF.get_shortcut(context, name, plugin_name)

    def set_shortcut(
        self,
        shortcut: str,
        name: str,
        context: Optional[str] = None,
        plugin_name: Optional[str] = None,
    ):
        """
        Set a shortcut sequence with a given name and context.

        Parameters
        ----------
        shortcut: str
            Key sequence of the shortcut.
        name: str
            The shortcut name (e.g. "run cell").
        context: str, optional
            Name of the shortcut context, e.g. "editor" for shortcuts that have
            effect when the Editor is focused or "_" for global shortcuts. If
            not set, the widget's CONF_SECTION will be used as context.
        plugin_name: str, optional
            Name of the plugin where the shortcut is defined. This is necessary
            for third-party plugins that have shortcuts with a context
            different from the plugin name.

        Raises
        ------
        configparser.NoOptionError
            If the shortcut does not exist in the configuration.
        """
        context = self.CONF_SECTION if context is None else context
        return CONF.set_shortcut(context, name, shortcut, plugin_name)

    def register_shortcut_for_widget(
        self,
        name: str,
        triggered: Callable,
        widget: Optional[QWidget] = None,
        context: Optional[str] = None,
    ):
        """
        Register a shortcut for a widget that inherits this mixin.

        Parameters
        ----------
        name: str
            The shortcut name (e.g. "run cell").
        triggered: Callable
            Callable (i.e. function or method) that will be triggered by the
            shortcut.
        widget: QWidget, optional
            Widget to which this shortcut will be registered. If not set, the
            widget that calls this method will be used.
        context: str, optional
            Name of the shortcut context, e.g. "editor" for shortcuts that have
            effect when the Editor is focused or "_" for global shortcuts. If
            not set, the widget's CONF_SECTION will be used as context.
        """
        context = self.CONF_SECTION if context is None else context
        widget = self if widget is None else widget

        # Register shortcut to widget
        keystr = self.get_shortcut(name, context)
        qsc = QShortcut(QKeySequence(keystr), widget)
        qsc.activated.connect(triggered)
        qsc.setContext(Qt.WidgetWithChildrenShortcut)

        # Keep track of all widget shortcuts. This is necessary to show them in
        # Preferences.
        data = ShortcutData(qobject=None, name=name, context=context)
        if data not in SHORTCUTS_FOR_WIDGETS_DATA:
            SHORTCUTS_FOR_WIDGETS_DATA.append(data)
