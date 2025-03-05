# custom_email_backend.py

import smtplib
import ssl
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

class EmailBackend(DjangoEmailBackend):
    def open(self):
        """
        Abre una conexión SMTP sin pasar keyfile ni certfile, 
        ya que en Python 3.12 estos argumentos ya no son soportados.
        """
        if self.connection:
            return False
        connection = None
        try:
            connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            connection.ehlo()
            if self.use_tls:
                if self.ssl_context is None:
                    self.ssl_context = ssl.create_default_context()
                # Llamamos a starttls() pasando solo el contexto
                connection.starttls(context=self.ssl_context)
                connection.ehlo()
            if self.username and self.password:
                connection.login(self.username, self.password)
            self.connection = connection
            return True
        except Exception:
            if connection:
                connection.close()
            raise
