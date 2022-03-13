from sys import version_info


__all__ = ['chesschaos_main']


def chesschaos_main():
    if version_info < (3, 10):
        raise ValueError('at least python 3.10 is required by this project')

    from menu import Window
    Window().run()


if __name__ == '__main__':
    chesschaos_main()
