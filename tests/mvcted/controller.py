# -*- coding: utf-8 -*-


def Controller():
    def __init__(self):
        pass
        
    def run(self):
        pass


def main():
    sys.setdefaultencoding("utf-8")
    controller = Controller()
    controller.run()
    
            
if __name__ == '__main__':
    # Next three lines are important for sublime console unicode support
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    main()
