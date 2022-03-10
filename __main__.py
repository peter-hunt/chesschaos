from sys import version_info


__all__ = ['chesschaos_main']


def chesschaos_main():
    if version_info < (3, 8):
        raise ValueError('at least python 3.8 is required by this project')

    from game import Game
    Game().run()


if __name__ == '__main__':
    chesschaos_main()
