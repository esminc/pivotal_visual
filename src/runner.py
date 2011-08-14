#coding: utf-8

from pprint import pprint
import ConfigParser
import sys

from tracker import Tracker
from visual import Visual

class RunnerConfig(object):
    def __init__(self, defaults=None):
        self.defaults = defaults

    def read(self, filename):
        self.config = ConfigParser.ConfigParser(self.defaults)
        self.config.read(filename)

        class Section(object):
            def __init__(self, config, section):
                self.config = config
                self.section = section

            def get(self, option):
                return self.config.get(self.section, option)

        for s in self.config.sections():
            exec "self.%s = Section(self.config, '%s')"%(s, s)

    def get(self, *args):
        return self.config.get(*args)

def iterations_from_server(config):
    tracker = Tracker(dbdir=config.tracker.get('local_store_directory'))
    tracker.authenticate(config.tracker.get('username'), config.get('tracker', 'password'))
    iterations = tracker.get_stories(config.tracker.get('project_id'))
    return iterations

def iterations_from_file(config, filename):
    tracker = Tracker(dbdir=config.tracker.get('local_store_directory'))
    f = open(filename)
    contents = ''
    for l in f: contents += l
    f.close()
    iterations = tracker.parse_stories(contents)
    return iterations

def main():
    config = RunnerConfig({'local_store_directory':''})
    config.read('config.ini')

    if len(sys.argv) >= 2:
        iterations = iterations_from_file(config, sys.argv[1])
    else:
        iterations = iterations_from_server(config)
    vis = Visual()
    vis.start()
    vis.draw_iteration_boxes(len(iterations))
    for i, it in enumerate(iterations):
        #pprint(it['stories'])
        #pprint(it['number'])
        vis.draw_iteration_number(it['number'], i)
        vis.draw_stories_for_iteration(it['stories'], i)

    raw_input()

if __name__=='__main__':
    main()



