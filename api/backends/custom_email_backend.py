import smtplib
import ssl
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

class EmailBackend(DjangoEmailBackend):
    def open(self):
        """
        Abre una conexión SMTP sin pasar keyfile ni certfile.
        Crea un contexto SSL local en lugar de usar self.ssl_context.
        """
        if self.connection:
            return False
        connection = None
        try:
            # Creamos la conexión SMTP
            connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            connection.ehlo()
            
            # Si hay TLS, usamos un contexto local (no self.ssl_context)
            if self.use_tls:
                ssl_context = ssl.create_default_context()
                connection.starttls(context=ssl_context)
                connection.ehlo()
            
            # Login con usuario y contraseña si existen
            if self.username and self.password:
                connection.login(self.username, self.password)
            
            self.connection = connection
            return True
        except Exception:
            if connection:
                connection.close()
            raise
