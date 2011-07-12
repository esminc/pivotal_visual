#coding: utf-8

from pprint import pprint
import ConfigParser

from tracker import Tracker
from visual import Visual

def main():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    tracker = Tracker()
    tracker.authenticate(config.get('tracker', 'username'), config.get('tracker', 'password'))
    iterations = tracker.get_stories(config.get('tracker', 'project_id'))

    vis = Visual()
    vis.start()
    vis.draw_iteration_boxes(len(iterations))
    for i, it in enumerate(iterations):
        #pprint(it['stories'])
        vis.draw_stories_for_iteration(it['stories'], i)

    raw_input()

if __name__=='__main__':
    main()



