import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type
from email.mime.base import MIMEBase
from email.encoders import encode_base64


class Emailer():
    """Basically a helper class to help with sending emails in Figdocs."""

    def __init__(self):
        """Just establish a connection to the SMTP server and retrieve config"""

        self._config = logger.figconfig.get_config("emailing")
        self._server = smtplib.SMTP(self._get_server_address())

    def _get_server_address(self):

        return self._config['server']

    def close_connection(self):

        self._server.quit()

    def send_email(self, to_address, subject, plain_text=None, html_text=None, attachments=None):
        """Pretty self explanatory - send an email!

        There are no parameters for from address or server since these should probably
        be stored in configuration and the same across all emails.
        """

        if plain_text is None and html_text is None:
            # TODO: Come up with a sensible way to handle errors here
            print('Need at least one message file')

        msg = MIMEMultipart('alternative')
        from_address = self._get_sender()
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address
        if plain_text is not None:
            plain = MIMEText(open(plain_text).read(), 'plain')
            msg.attach(plain)
        if html_text is not None:
            html = MIMEText(open(html_text).read(), 'html')
            msg.attach(html)
        if attachments is not None:
            for attachment in attachments:
                mimetype, encoding = guess_type(attachment)
                mimetype = mimetype.split('/', 1)
                attach_file = open(attachment, 'rb')
                attach_obj = MIMEBase(mimetype[0], mimetype[1])
                attach_obj.set_payload(attach_file.read())
                attach_file.close()
                encode_base64(attach_obj)
                attach_obj.add_header('Content-Disposition', 'attachment',
                                      filename=os.path.basename(attachment))
                msg.attach(attach_obj)

        self._server.sendmail(from_address, [to_address], msg.as_string())

    def _get_sender(self):

        return self._config['sender']

if __name__ == '__main__':

    test = Emailer()
    test.send_email('testemail', 'Hi James',
                    r'C:\Users\talbotj\PycharmProjects\Figdoc\Emailing\emlplain.txt',
                    r'C:\Users\talbotj\PycharmProjects\Figdoc\Emailing\emlmsg.html',
                    [r'C:\Users\talbotj\PycharmProjects\Figdoc\Emailing\testpdf.pdf',
                     r'C:\Users\talbotj\PycharmProjects\Figdoc\Emailing\testxml.xml'])
    test.close_connection()
