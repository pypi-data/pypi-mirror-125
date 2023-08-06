# -*- coding: utf-8 -*-
## @namespace grepros.search
"""
Search core.

------------------------------------------------------------------------------
This file is part of grepros - grep for ROS1 bag files and live topics.
Released under the BSD License.

@author      Erki Suurjaak
@created     28.09.2021
@modified    30.10.2021
------------------------------------------------------------------------------
"""
import copy
import collections
import re

from . common import ROS_NUMERIC_TYPES, MatchMarkers, filter_fields, get_message_fields, \
                     get_message_value, merge_spans, wildcard_to_regex


class Searcher(object):
    """ROS message grepper."""


    def __init__(self, args):
        """
        @param   args                     arguments object like argparse.Namespace
        @param   args.PATTERNS            pattern(s) to find in message field values
        @param   args.RAW                 PATTERNS are ordinary strings, not regular expressions
        @param   args.CASE                use case-sensitive matching in PATTERNS
        @param   args.INVERT              select non-matching messages
        @param   args.BEFORE              number of messages of leading context to emit before match
        @param   args.AFTER               number of messages of trailing context to emit after match
        @param   args.MAX_MATCHES         number of matched messages to emit (per file if bag input)
        @param   args.MAX_TOPIC_MATCHES   number of matched messages to emit from each topic
        @param   args.MAX_TOPICS          number of topics to print matches from
        @param   args.SELECT_FIELDS       message fields to use in matching if not all
        @param   args.NOSELECT_FIELDS     message fields to skip in matching
        """
        self._args     = copy.deepcopy(args)
        self._patterns = {}  # {key: [(() if any field else ('nested', 'path'), re.Pattern), ]}
        # {topic: {message ID: message}}
        self._messages = collections.defaultdict(collections.OrderedDict)
        # {topic: {message ID: rospy.Time}}
        self._stamps   = collections.defaultdict(collections.OrderedDict)
        # {topic: {None: count processed, True: count matched, False: count emitted as context}}
        self._counts   = collections.defaultdict(lambda: collections.defaultdict(int))
        # {topic: {message ID: True if matched else False if emitted else None}
        self._statuses = collections.defaultdict(collections.OrderedDict)

        self._parse_patterns()


    def search(self, source, sink):
        """
        Greps messages yielded from source and emits matched content to sink.

        @param   source  inputs.SourceBase instance
        @param   sink    outputs.SinkBase instance
        @return          count matched
        """
        for d in (self._messages, self._stamps, self._counts, self._statuses): d.clear()
        source.bind(sink), sink.bind(source)

        counter, total, batch = 0, 0, None
        for topic, msg, stamp in source.read():
            if batch != source.get_batch():
                total += sum(x[True] for x in self._counts.values())
                for d in (self._counts, self._messages, self._stamps, self._statuses):
                    d.clear()
                counter, batch = 0, source.get_batch()

            msgid = counter = counter + 1
            self._counts[topic][None] += 1
            self._messages[topic][msgid] = msg
            self._stamps  [topic][msgid] = stamp
            self._statuses[topic][msgid] = None

            matched = self._is_processable(source, topic, stamp) and self.get_match(msg)
            if matched:
                self._statuses[topic][msgid] = True
                self._counts[topic][True] += 1
                sink.emit_meta()
                for i, s, m in self._get_context(topic, before=True):
                    self._counts[topic][False] += 1
                    sink.emit(topic, i, s, m, None)
                    self._statuses[topic][i] = False
                sink.emit(topic, self._counts[topic][None], stamp, msg, matched)
            elif self._args.AFTER and self._has_in_window(topic, self._args.AFTER + 1, status=True):
                for i, s, m in self._get_context(topic, before=False):
                    self._counts[topic][False] += 1
                    sink.emit(topic, i, s, m, None)
                    self._statuses[topic][i] = False
            source.notify(matched)

            self._prune_data(topic)
            if self._is_max_done(topic):
                break  # for topic

        source.close(), sink.close()
        return total + sum(x[True] for x in self._counts.values())


    def _is_processable(self, source, topic, stamp):
        """
        Returns whether processing current message in topic is acceptable:
        that topic or total maximum count has not been reached,
        and current message in topic is in configured range, if any.
        """
        if self._args.MAX_MATCHES \
        and sum(x[True] for x in self._counts.values()) >= self._args.MAX_MATCHES:
            return False
        if self._args.MAX_TOPIC_MATCHES \
        and self._counts[topic][True] >= self._args.MAX_TOPIC_MATCHES:
            return False
        if self._args.MAX_TOPICS:
            topics_matched = [t for t, x in self._counts.items() if x[True]]
            if topic not in topics_matched and len(topics_matched) >= self._args.MAX_TOPICS:
                return False
        return source.is_processable(topic, self._counts[topic][None], stamp)


    def _prune_data(self, topic):
        """Drops history older than context window."""
        WINDOW = max(self._args.BEFORE, self._args.AFTER) + 1
        for dct in (self._messages, self._stamps, self._statuses):
            while len(dct[topic]) > WINDOW:
                dct[topic].pop(next(iter(dct[topic])))


    def _parse_patterns(self):
        """Parses pattern arguments into re.Patterns."""
        self._patterns.clear()
        contents, raw, case = [], self._args.RAW, self._args.CASE
        for v in self._args.PATTERNS:
            split = v.find("=", 1, -1)
            v, path = (v[split + 1:], v[:split]) if split > 0 else (v, ())
            # Special case if '' or "": add pattern for matching empty string
            v = (re.escape(v) if raw else v) + ("|^$" if v in ("''", '""') else "")
            path = tuple(path.split(".")) if path else ()
            contents.append((path, re.compile("(%s)" % v, 0 if case else re.I)))
        self._patterns["content"] = contents

        selects, noselects = self._args.SELECT_FIELDS, self._args.NOSELECT_FIELDS
        for key, vals in [("select", selects), ("noselect", noselects)]:
            self._patterns[key] = [(tuple(v.split(".")), wildcard_to_regex(v)) for v in vals]


    def _get_context(self, topic, before=False):
        """Returns unemitted context for latest match, as [(index, timestamp, message)]."""
        result = []
        count = self._args.BEFORE + 1 if before else self._args.AFTER
        candidates = list(self._statuses[topic])[-count:]
        current_index = self._counts[topic][None]
        for i, msgid in enumerate(candidates) if count else ():
            if self._statuses[topic][msgid] is None:
                idx = current_index + (i - len(candidates) if before else 0)
                result += [(idx, self._stamps[topic][msgid], self._messages[topic][msgid])]
        return result


    def _is_max_done(self, topic):
        """Returns whether max match count has been reached (and message after-context emitted)."""
        result = False
        if self._args.MAX_MATCHES:
            if sum(x[True] for x in self._counts.values()) >= self._args.MAX_MATCHES \
            and not self._has_in_window(topic, self._args.AFTER, status=None, full=True):
                result = True
        return result


    def _has_in_window(self, topic, length, status, full=False):
        """Returns whether given status exists in recent message window."""
        if not length or full and len(self._statuses[topic]) < length:
            return False
        return status in list(self._statuses[topic].values())[-length:]


    def get_match(self, msg):
        """
        Returns transformed message if all patterns find a match in message, else None.

        Matching field values are converted to strings and surrounded by markers.
        """
        scalar = lambda n: n[:n.index("[")] if "[" in n else n  # Returns type from type[..]

        def wrap_matches(v, top, is_collection=False):
            """Returns string with parts matching patterns wrapped in marker tags."""
            spans = []
            # Omit collection brackets from match unless empty: allow matching "[]"
            v1 = v2 = v[1:-1] if is_collection and v != "[]" else v
            for i, (path, p) in enumerate(self._patterns["content"]):
                if not path or any(path == top[j:j + len(path)] for j in range(len(top))):
                    for match in (m for m in p.finditer(v1) if not v1 or m.start() != m.end()):
                        matched[i] = True
                        spans.append(match.span())
                        if self._args.INVERT:
                            break  # for match
            spans = merge_spans(spans) if not self._args.INVERT else \
                    [] if spans else [(0, len(v1))] if v1 or not is_collection else []
            for a, b in reversed(spans):  # Work from last to first, indices stay the same
                v2 = v2[:a] + MatchMarkers.START + v2[a:b] + MatchMarkers.END + v2[b:]
            return "[%s]" % v2 if is_collection and v != "[]" else v2

        def decorate_message(obj, top=()):
            """Recursively converts field values to pattern-matched strings."""
            selects, noselects = self._patterns["select"], self._patterns["noselect"]
            fieldmap = get_message_fields(obj)
            fieldmap = filter_fields(fieldmap, top, include=selects, exclude=noselects)
            for k, t in fieldmap.items():
                v, path = get_message_value(obj, k, t), top + (k, )
                is_collection = isinstance(v, (list, tuple))
                if hasattr(v, "__slots__"):
                    decorate_message(v, path)
                elif is_collection and scalar(t) not in ROS_NUMERIC_TYPES:
                    setattr(obj, k, [decorate_message(x, path) for x in v])
                else:
                    v1 = str(list(v) if isinstance(v, (bytes, tuple)) else v)
                    v2 = wrap_matches(v1, path, is_collection)
                    if len(v1) != len(v2):
                        setattr(obj, k, v2)
            if not hasattr(obj, "__slots__"):
                v1 = str(list(obj) if isinstance(obj, bytes) else obj)
                v2 = wrap_matches(v1, top)
                obj = v2 if len(v1) != len(v2) else obj
            return obj

        yml = "" if self._args.INVERT else str(msg)
        if yml and not all(any(p.finditer(yml)) for _, p in self._patterns["content"]):
            return None  # Skip detailed matching if patterns not present at all

        result, matched = copy.deepcopy(msg), {}  # {pattern index: True}
        decorate_message(result)
        yes = not matched if self._args.INVERT else len(matched) == len(self._patterns["content"])
        return result if yes else None
