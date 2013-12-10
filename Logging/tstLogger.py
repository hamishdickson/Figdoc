import logger

__author__ = 'DicksonH'


def main():
    log = logger.pdfLogger()
    log.write_info("this is a test")

if __name__ == '__main__':
    main()