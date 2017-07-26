class MarkdownLogger(object):

    @staticmethod
    def println(msg, bold=False, italic=False):
        new_msg = msg if not bold else "__%s__" % msg
        new_msg = new_msg if not italic else "_%s_" % new_msg
        print new_msg, "  "

    @staticmethod
    def print_header(header, level=1):
        print "\n", "#"*level, header

    @staticmethod
    def print_header2(header):
        MarkdownLogger.print_header(header, 2)

    @staticmethod
    def print_header3(header):
        MarkdownLogger.print_header(header, 3)

    @staticmethod
    def print_url(label, url):
        print "[%s](%s)" % (label, url)

    @staticmethod
    def print_para(msg):
        print "\n", msg, "\n"

    @staticmethod
    def print_hr():
        print "***"

    @staticmethod
    def print_code(msg):
        print "\n", "```"
        print msg
        print "```\n"

    @staticmethod
    def print_list(items, ordered=False):
        delimiter = "1." if ordered else "*"
        for item in items:
            print delimiter, item
        print "\n"

    @staticmethod
    def print_table(headers, rows):
        print "\n|", "|".join(headers), "|"
        print "|", " ------ |" * len(headers)
        for r in rows:
            print "| ", "  |".join(r), " |"
        print "\n"

    @staticmethod
    def print_error(msg):
        MarkdownLogger.print_hr()
        MarkdownLogger.print_header3("Error")
        if hasattr(msg, '__call__'):
            #function
            msg()
        else:
            MarkdownLogger.print_para(msg)
        MarkdownLogger.print_hr()
