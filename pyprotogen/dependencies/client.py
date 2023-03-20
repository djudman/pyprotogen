from grpc.aio import insecure_channel, secure_channel
from grpc import ssl_channel_credentials
from py_grpc_prometheus.aio.prometheus_aio_client_interceptor import PromAioClientInterceptor
from .interceptors.client_logging import LoggingClientInterceptor


def get_channel(host: str, cert: str | None = None, enable_metrics: bool = True, enable_logging: bool = True):
    interceptors = []
    if enable_logging:
        prom = PromAioClientInterceptor(
            enable_client_handling_time_histogram=True,
            enable_client_stream_receive_time_histogram=True,
            enable_client_stream_send_time_histogram=True,
        )
        interceptors.append(prom)
    if enable_metrics:
        log = LoggingClientInterceptor()
        interceptors.append(log)
    if cert:
        creds = ssl_channel_credentials(cert.encode())
        ch = secure_channel(host, credentials=creds, interceptors=interceptors)
    else:
        ch = insecure_channel(host, interceptors=interceptors)
    return ch