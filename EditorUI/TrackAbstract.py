# This file is part of SNARE.
# Copyright (C) 2016  Philipp Merz and Malte Merdes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from EditorBackend.Waveform import Waveform


class TrackAbstract(QWidget):

    """
    TrackAbstract is the superclass from which most elements or layers of a Track inherit. That way they all share an
    identical interface based around Qt's signal-slot-concept. The signals and slots all have defined connections to
    their respective slots and signals of the parent object. Therefore, if an object of a class inherited from
    TrackAbstract creates another object that is also from a class that inherits TrackAbstract, their interface will
    automatically be connected in the way described here. This allows for an easy layering of objects, without any
    boilerplate connection making code whilst not breaking encapsulation rules. See the overall documentation of SNARE
    for a more detailed explanation on this design-pattern.
    """

    # SIGNALS
    # from Hardware
    sig_mousePress = pyqtSignal(QGraphicsSceneMouseEvent)
    sig_mouseRelease = pyqtSignal(QGraphicsSceneMouseEvent)
    sig_mouseMove = pyqtSignal(QGraphicsSceneMouseEvent)
    sig_mouseDoubleClick = pyqtSignal(QGraphicsSceneMouseEvent)
    sig_keyEnter = pyqtSignal(QKeyEvent)
    sig_keyRelease = pyqtSignal(QKeyEvent)

    # from PushButtons or Keyboard
    sig_playpause = pyqtSignal()
    sig_zoomIn = pyqtSignal()
    sig_zoomOut = pyqtSignal()
    sig_analyze = pyqtSignal()
    sig_finishSelection = pyqtSignal()
    sig_editSelection = pyqtSignal()
    sig_selectionChange = pyqtSignal(str, str)
    sig_skipForward = pyqtSignal()
    sig_skipBackward = pyqtSignal()
    sig_delete = pyqtSignal()
    sig_requestMark = pyqtSignal()

    # generated by program
    sig_requestWaveform = pyqtSignal(int, int, int)
    sig_viewChanged = pyqtSignal(QRectF)

    # Signals travelling in opposite direction
    # ToDo Mark travelling direction in naming convention
    sig_redraw = pyqtSignal(float)
    sig_startSelection = pyqtSignal(QGraphicsSceneMouseEvent)
    sig_moveSelection = pyqtSignal(QGraphicsSceneMouseEvent)
    sig_endSelection = pyqtSignal(QGraphicsSceneMouseEvent)
    sig_enableSelection = pyqtSignal(bool)
    sig_setSelection = pyqtSignal(str, str, dict, str)
    sig_setMark = pyqtSignal(int)
    sig_addWaveform = pyqtSignal(Waveform)
    sig_setView = pyqtSignal(QRectF)
    sig_update = pyqtSignal(float)
    sig_setPlaying = pyqtSignal(bool)

    def __init__(self, name, state, selections, analysisTypes, marks, cursorposition, height, width, smptopix, zoom, root=None):
        """
        After all signals have been created it is checked if a root-object has been supplied. If so, all connections
        will be made. Naming the parent "root" is to avoid confusion with the parent of a QWidget, which refers to a
        user-interface structure and not the object relations.

        :param name: Name assigned to this track
        :param state: Lock-state on creation
        :param selections: Initial list of selection names
        :param analysisTypes: Initial list of analysis types
        :param marks: Initial list of marks on the time axis. Not relevant here.
        :param cursorposition: Initial cursor position. Not relevant here.
        :param height: Dimensions available for the entire track.
        :param width:  Dimensions available for the entire track.
        :param smptopix: Conversion factor, how many samples are displayed as one pixel. (At zoom-factor 1)
        :param zoom: Initial zoom-factor
        :param parent: The object on top of which this object is stacked in the layer structure.
        """
        super(TrackAbstract, self).__init__()

        # Parameters to members
        self.name = name
        self.state = state
        self.selections = selections
        self.marks = marks
        self.cursorposition = cursorposition
        self.height = height
        self.width = width
        self.smptopix = smptopix
        self.zoom = zoom

        # named "root" instead of "parent" to avoid confusion with the qt-widget-parent
        self.root = None
        if root:
            # Handover Signal to parent-widget
            self.root = root
            # from Hardware
            self.sig_mousePress.connect(self.root.slo_mousePress)
            self.sig_mouseRelease.connect(self.root.slo_mouseRelease)
            self.sig_mouseMove.connect(self.root.slo_mouseMove)
            self.sig_mouseDoubleClick.connect(self.root.slo_mouseDoubleClick)
            self.sig_keyEnter.connect(self.root.slo_keyEnter)
            self.sig_keyRelease.connect(self.root.slo_keyRelease)

            # from PushButtons or Keyboard
            self.sig_playpause.connect(self.root.slo_playpause)
            self.sig_zoomIn.connect(self.root.slo_zoomIn)
            self.sig_zoomOut.connect(self.root.slo_zoomOut)
            self.sig_analyze.connect(self.root.slo_analyze)
            self.sig_finishSelection.connect(self.root.slo_finishSelection)
            self.sig_editSelection.connect(self.root.slo_editSelection)
            self.sig_selectionChange.connect(self.root.slo_selectionChange)
            self.sig_skipForward.connect(self.root.slo_skipForward)
            self.sig_skipBackward.connect(self.root.slo_skipBackward)
            self.sig_delete.connect(self.root.slo_delete)
            self.sig_requestMark.connect(self.root.slo_requestMark)

            # Generated by program
            self.sig_requestWaveform.connect(self.root.slo_requestWaveform)
            self.sig_viewChanged.connect(self.root.slo_viewChanged)

            # Signals travelling in opposite direction
            self.root.sig_redraw.connect(self.slo_redraw)
            self.root.sig_startSelection.connect(self.slo_startSelection)
            self.root.sig_moveSelection.connect(self.slo_moveSelection)
            self.root.sig_endSelection.connect(self.slo_endSelection)
            self.root.sig_enableSelection.connect(self.slo_enableSelection)
            self.root.sig_setSelection.connect(self.slo_setSelection)
            self.root.sig_setMark.connect(self.slo_setMark)
            self.root.sig_addWaveform.connect(self.slo_addWaveform)
            self.root.sig_setView.connect(self.slo_setView)
            self.root.sig_update.connect(self.slo_update)
            self.root.sig_setPlaying.connect(self.slo_setPlaying)

    # Default Signal-Relais
    # from Hardware
    def slo_mousePress(self, QGraphicsSceneMouseEvent):
        """
        Relays the signal to the parent object. Catches any mouse event triggered on any layer of the Track and sends it
        through all layers to TrackManager where it will be processed.

        :param QGraphicsSceneMouseEvent: Qt mouse event type.
        """
        self.sig_mousePress.emit(QGraphicsSceneMouseEvent)

    def slo_mouseRelease(self, QGraphicsSceneMouseEvent):
        """
        Relays the signal to the parent object. Catches any mouse event triggered on any layer of the Track and sends it
        through all layers to TrackManager where it will be processed.

        :param QGraphicsSceneMouseEvent: Qt mouse event type.
        """
        self.sig_mouseRelease.emit(QGraphicsSceneMouseEvent)

    def slo_mouseMove(self, QGraphicsSceneMouseEvent):
        """
        Relays the signal to the parent object. Catches any mouse event triggered on any layer of the Track and sends it
        through all layers to TrackManager where it will be processed.

        :param QGraphicsSceneMouseEvent: Qt mouse event type.
        """
        self.sig_mouseMove.emit(QGraphicsSceneMouseEvent)

    def slo_mouseDoubleClick(self, QGraphicsSceneMouseEvent):
        """
        Relays the signal to the parent object. Catches any mouse event triggered on any layer of the Track and sends it
        through all layers to TrackManager where it will be processed.

        :param QGraphicsSceneMouseEvent: Qt mouse event type.
        """
        self.sig_mouseDoubleClick.emit(QGraphicsSceneMouseEvent)

    def slo_keyEnter(self, QKeyEvent):
        """
        Relays the signal to the parent object. Catches any keyboard event triggered on any layer of the Track and sends
        it through all layers to TrackManager where it will be processed.

        :param QKeyEvent: Qt key event type.
        """
        self.sig_keyEnter.emit(QKeyEvent)

    def slo_keyRelease(self, QKeyEvent):
        """
        Relays the signal to the parent object. Catches any keyboard event triggered on any layer of the Track and sends
        it through all layers to TrackManager where it will be processed.

        :param QKeyEvent: Qt key event type.
        """
        self.sig_keyRelease.emit(QKeyEvent)

    # from PushButtons or Keyboard
    def slo_playpause(self):
        """
        Relays the signal to the parent object. For pressing play or pause (a switch button) at TrackButtons.
        """
        self.sig_playpause.emit()

    def slo_zoomIn(self):
        """
        Relays the signal to the parent object. For pressing "+" at TrackButtons.
        """
        self.sig_zoomIn.emit()

    def slo_zoomOut(self):
        """
        Relays the signal to the parent object. For pressing "-" at TrackButtons.
        """
        self.sig_zoomOut.emit()

    def slo_analyze(self):
        """
        Relays the signal to the parent object. For pressing "Analyze" at TrackButtons.
        """
        self.sig_analyze.emit()

    def slo_finishSelection(self):
        """
        Relays the signal to the parent object. For setting the selection state to "locked". (Lock symbol at
        TrackButtons)
        """
        self.sig_finishSelection.emit()

    def slo_editSelection(self):
        """
        Relays the signal to the parent object. For setting the selection state to "unlocked". (Lock symbol at
        TrackButtons)
        """
        self.sig_editSelection.emit()

    def slo_selectionChange(self, selectionName, analysisType):
        """
        Relays the signal to the parent object. Triggered when one of the dropdown menus at TrackButtons changed.

        :param selectionName: Name of the new selection.
        :param analysisType: Name of the new analysis type.
        """
        self.sig_selectionChange.emit(selectionName, analysisType)

    def slo_skipForward(self):
        """
        Relays the signal to the parent object. A request from TrackButtons to skip to the next mark.
        """
        self.sig_skipForward.emit()

    def slo_skipBackward(self):
        """
        Relays the signal to the parent object. A request from TrackButtons to skip to the previous mark.
        """
        self.sig_skipBackward.emit()

    def slo_delete(self):
        """
        Relays the signal to the parent object. A request from TrackButtons to delete this track.
        """
        self.sig_delete.emit()

    def slo_requestMark(self):
        """
        Relays the signal to the parent object. A request from TrackButtons to place a mark on the current TrackCursor
        position.
        """
        self.sig_requestMark.emit()

    # generated by program
    def slo_requestWaveform(self, block, widthPreScaling, height):
        """
        Relays the signal to the parent object. A signal from TrackWaveform, requesting the backend to render a specific
        waveform pixmap. The channel association is added at TrackManager.

        :param block: The block to be rendered.
        :param widthPreScaling: The width to fit the pixmap of one block in. Therefore the width equals the zoom-level, since the blocksize is static.
        :param height: Height of the pixmap.
        """
        self.sig_requestWaveform.emit(block, widthPreScaling, height)

    def slo_viewChanged(self, QRectF):
        """
        Relays the signal to the parent object. A signal triggered when the user changed the view by scrolling or
        dragging.

        :param QRectF: The rectangle inside the scene that is now displayed by the view.
        """
        self.sig_viewChanged.emit(QRectF)

    # Signals travelling in other direction
    def slo_redraw(self, factor):
        """
        Relays the signal to child objects. An actual implementation can be found at TrackSelection, TrackWaveform
        et al.

        :param factor: New zoom-level
        """
        self.sig_redraw.emit(factor)

    def slo_startSelection(self, QGraphicsSceneMouseEvent):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackSelection, it is one of four to
        control the state machine of TrackSelection

        :param QGraphicsSceneMouseEvent: A Qt-type containing at least the mouse button that was pressed and the cursor
        position
        """
        self.sig_startSelection.emit(QGraphicsSceneMouseEvent)

    def slo_moveSelection(self, QGraphicsSceneMouseEvent):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackSelection, it is one of four to
        control the state machine of TrackSelection

        :param QGraphicsSceneMouseEvent: A Qt-type containing at least the mouse button that was pressed and the cursor
        position
        """
        self.sig_moveSelection.emit(QGraphicsSceneMouseEvent)

    def slo_endSelection(self, QGraphicsSceneMouseEvent):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackSelection, it is one of four to
        control the state machine of TrackSelection

        :param QGraphicsSceneMouseEvent: A Qt-type containing at least the mouse button that was pressed and the cursor
        position
        """

        self.sig_endSelection.emit(QGraphicsSceneMouseEvent)

    def slo_enableSelection(self, bool):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackSelection, it is one of four to
        control the state machine of TrackSelection

        :param bool: Enter False to block the selection from changes
        """

        self.sig_enableSelection.emit(bool)

    def slo_setSelection(self, selectionName, analysisType, selection, state):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackSelection and TrackButtons.

        :param selectionName: Name of the selection to switch to.
        :param analysisType: Name of the type of analysis associated with the current selection.
        :param selection: Start and end samples of the actual selection.
        :param state: Lock state of the selection
        """
        self.sig_setSelection.emit(selectionName, analysisType, selection, state)

    def slo_setMark(self, smp):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackMarks.

        :param smp: Sample on which to put a mark
        """
        self.sig_setMark.emit(smp)

    def slo_addWaveform(self, Waveform):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackWaveform.

        :param Waveform: a Waveform-object.
        """
        self.sig_addWaveform.emit(Waveform)

    def slo_setView(self, QRectF):
        """
        Relays the signal to child-objects. The destination of this signal-path is TrackView.

        :param QRectF: A rectangle describing the part of the QGraphicScene to display.
        """
        self.sig_setView.emit(QRectF)

    def slo_update(self, pos):
        """
        Relays the signal to child-objects. The destination of this signal-path are all objects related to the waveform
        display, e.g. TrackWaveform and TrackTimeline.

        :param pos: Position in samples around which to update the view and scene.
        """
        self.sig_update.emit(pos)

    def slo_setPlaying(self, bool):
        """
        Relays the signal to child-objects. The destination of this signal-path is the play/pause-button of
        TrackButtons. It is necessary to display the right playback state on each channel.

        :param bool: True if playing.
        """
        self.sig_setPlaying.emit(bool)
