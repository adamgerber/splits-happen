#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import sys
import argparse
from collections import defaultdict

class ScoreProcessor(object):
    SYMBOL_STRIKE = 'X'
    SYMBOL_SPARE  = '/'
    SYMBOLS_CLEARING = set([SYMBOL_STRIKE, SYMBOL_SPARE])
    SYMBOL_MISS   = '-'
    MAX_THROWS_PER_FRAME = 2

    def __init__(self, results):
        self.results = results

    def get_score(self):
        # the scores for each frame
        frames = []

        # all frames waiting to have their scores augmented by
        # a given throw (the key)
        frames_waiting_on_throw = defaultdict(list)

        throw_total = len(self.results) - 1

        throw_i = -1
        frame_i = -1
        remaining_throws = 0 # force a new frame

        while throw_i < throw_total:
            throw_i += 1
            symbol = self.results[throw_i]

            # if necessary, setup a new frame
            if remaining_throws is 0:
                frame_i += 1
                frames.append(0)
                remaining_throws = self.MAX_THROWS_PER_FRAME

            # did this throw clear the lane?
            if symbol in self.SYMBOLS_CLEARING:

                # if so, attach this frame to the proper number of future throws
                if symbol is self.SYMBOL_STRIKE:
                    points = 10
                    frames_waiting_on_throw[throw_i + 2].append(frame_i)
                else:
                    points = 10 - points

                frames_waiting_on_throw[throw_i + 1].append(frame_i)
                remaining_throws = 0

            else:
                # otherwise, just handle the score
                points = 0 if symbol is self.SYMBOL_MISS else int(symbol)
                remaining_throws -= 1

            # update all previous frames affected by this throw
            frames[frame_i] += points
            for frame in frames_waiting_on_throw[throw_i]:
                frames[frame] += points

        # for generality, scores are allowed to accumulate for frames beyond 10,
        # so exclude those frames from final score
        return sum(frames[:10])


def main():
    usage = 'usage: %s <scores>\n       %s test\n' % (sys.argv[0], sys.argv[0])

    if len(sys.argv) != 2:
        print '%s: error in arguments' % (sys.argv[0])
        print usage
    else:
        args = sys.argv[1]

        if args.lower() in ['test', '-test', '--test']:
            test()
        else:
            try:
                scorer = ScoreProcessor(args)
                print scorer.get_score()
            except:
                print '%s: invalid scores: %s' % (sys.argv[0], args)
                print usage


def test():
    test_pairs = []
    test_pairs.append([300, 'XXXXXXXXXXXX'])
    test_pairs.append([150, '5/5/5/5/5/5/5/5/5/5/5'])
    test_pairs.append([90,  '9-9-9-9-9-9-9-9-9-9-'])
    test_pairs.append([167, 'X7/9-X-88/-6XXX81'])

    pass_count = 0
    attempt_count = 0

    print 'Testing...'
    for expected_score, result in test_pairs:
        scorer = ScoreProcessor(result)
        computed_score = scorer.get_score()
        attempt_count += 1
        if computed_score == expected_score:
            pass_count += 1
        else:
            print 'FAIL %s: %s, expected %s' % (result, computed_score, expected_score) 

    print '%s / %s' % (pass_count, attempt_count)
    print '%s %s%%' % ('OK' if pass_count == attempt_count else 'FAIL', 100.0 * pass_count / attempt_count)


if __name__ == '__main__':
    main()

