from PollyReports import Report, Band, Element, Rule
from reportlab.pdfgen.canvas import Canvas


def generate_report(name, results, footer=True):
    rpt = Report(results)
    rpt.detailband = Band([
                           Element((0, 0), ('Helvetica-Oblique', 10),
                                   key='name'),
                           Element((400, 0), ('Helvetica-Oblique', 10),
                                   key='status'),
                           ])

    passed = str(get_passed_tests(results))
    failed = str(get_failed_tests(results))
    total = str(len(results))

    rpt.reportfooter = Band([
                            Rule((380, 4), 72),
                            Element((280, 9), ('Helvetica-Bold', 10),
                                    text='Passed scenarios'),
                            Element((414, 9), ('Helvetica-Bold', 10),
                                    text=passed),
                            Element((280, 25), ('Helvetica-Bold', 10),
                                    text='Failed scenarios'),
                            Element((414, 25), ('Helvetica-Bold', 10),
                                    text=failed),
                            Element((280, 41), ('Helvetica-Bold', 10),
                                    text='Total'),
                            Element((414, 41), ('Helvetica-Bold', 10),
                                    text=total),
                            Element((0, 16), ('Helvetica-Bold', 10),
                                    text=''),
                            ])

    create_header(rpt)

    if footer:
        create_footer(rpt)

    name = name[:-8]
    canvas = Canvas(name + '.pdf')
    rpt.generate(canvas)
    canvas.save()


def create_header(rpt, report_name=None):
    if report_name is None:
        report_name = 'Test Results'

    rpt.pageheader = Band([
                            Element((0, 0), ('Helvetica-Bold', 17),
                                    text=report_name),
                            Element((0, 24), ('Helvetica', 12),
                                    text='Scenario'),
                            Element((400, 24), ('Helvetica', 12),
                                    text='Status'),
                            Rule((0, 43), 7.5*72),
                            Element((0, 45), ('Helvetica-Bold', 2),
                                    text=''),
                           ])


def create_footer(rpt):
    rpt.pagefooter = Band([
                            Element((0, 16), ('Helvetica-Bold', 10),
                                    sysvar='pagenumber',
                                    format=lambda x: 'Page %d' % x),
                           ])


def get_passed_tests(results):
    p = 0
    for test in results:
        if test['status'] == 'passed':
            p += 1
    return p


def get_failed_tests(results):
    f = 0
    for test in results:
        if test['status'] == 'failed':
            f += 1
    return f
