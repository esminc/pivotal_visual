#coding: utf-8

from pprint import pprint
import ConfigParser
import sys

from tracker import Tracker
from visual import Visual

def iterations_from_server(config):
    tracker = Tracker(dbdir=config.get('tracker', 'local_store_directory'))
    tracker.authenticate(config.get('tracker', 'username'), config.get('tracker', 'password'))
    iterations = tracker.get_stories(config.get('tracker', 'project_id'))
    return iterations

def iterations_from_file(config, filename):
    tracker = Tracker(dbdir=config.get('tracker', 'local_store_directory'))
    f = open(filename)
    contents = ''
    for l in f: contents += l
    f.close()
    iterations = tracker.parse_stories(contents)
    return iterations

def main():
    config = ConfigParser.ConfigParser()
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
        vis.draw_stories_for_iteration(it['stories'], i)

    raw_input()

if __name__=='__main__':
    main()



