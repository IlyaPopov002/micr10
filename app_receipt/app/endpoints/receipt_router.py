from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header

from app.models.receipt import Receipt, CreateReceiptRequest
from app.services.receipt_service import ReceiptService
import prometheus_client
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from fastapi import Request, Response

receipt_router = APIRouter(prefix='/receipt', tags=['receipt'])
metrics_router = APIRouter(tags=['Metrics'])


provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: "food-delivery"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name = 'Delivery Service'
tracer = trace.get_tracer(name)


delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])
metrics_router = APIRouter(tags=['Metrics'])

get_deliveries_count = prometheus_client.Counter(
    "get_deliveries_count",
    "Total got all deliveries"
)

created_delivery_count = prometheus_client.Counter(
    "created_delivery_count",
    "Total created deliveries"
)

started_delivery_count = prometheus_client.Counter(
    "started_printing_count",
    "Total started deliveries"
)

completed_delivery_count = prometheus_client.Counter(
    "completed_printing_count",
    "Total completed deliveries"
)

cancelled_delivery_count = prometheus_client.Counter(
    "cancelled_printing_count",
    "Total canceled deliveries"
)

def user_admin(role):
    if role == "service_user" or role == "service_admin":
        return True
    return False

def admin(role):
    if role == "service_admin":
        return True
    return False

# @receipt_router.get('/')
# def get_receipt(receipt_service: receiptService = Depends(receiptService)) -> list[receipt]:
#     return receipt_service.get_receipt()

@receipt_router.get('/')
def get_receipt(receipt_service: ReceiptService = Depends(ReceiptService), user: str = Header(...)) -> list[Receipt]:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    return receipt_service.get_receipt()
                raise HTTPException(403)
    except KeyError:
            raise HTTPException(404, f'Order with id={id} not found')


# @receipt_router.get('/{id}')
# def get_receipt_by_id(receipt_service: receiptService = Depends(receiptService)) -> list[receipt]:
#     return receipt_service.get_receipt()

@receipt_router.get('/{id}')
def get_receipt_by_id(id: UUID, receipt_service: ReceiptService = Depends(ReceiptService), user: str = Header(...)) -> Receipt:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if user_admin(user['role']):
                    get_deliveries_count.inc(1)
                    return receipt_service.get_receipt_by_id(id)
                raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')

@receipt_router.post('/add')
def add_receipt(
        receipt_info: CreateReceiptRequest,
        receipt_service: ReceiptService = Depends(ReceiptService)
) -> Receipt:
    try:
        print('\n///post_order///\n')
        receipt = receipt_service.create_receipt(receipt_info.ord_id, receipt_info.type, receipt_info.rec,
                                                 receipt_info.customer_info)
        return receipt.dict()
    except KeyError:
        raise HTTPException(400, f'Order with id={receipt_info.order_id} already exists')


# @receipt_router.post('/{id}/delete')
# def delete_receipt(id: UUID, receipt_service: receiptService = Depends(receiptService)) -> receipt:
#     try:
#         receipt = receipt_service.delete_receipt(id)
#         return receipt.dict()
#     except KeyError:
#         raise HTTPException(404, f'receipt with id={id} not found')

@receipt_router.post('/{id}/delete')
def delete_receipt(id: UUID, receipt_service: ReceiptService = Depends(ReceiptService),user: str = Header(...)) -> Receipt:
    try:
        user = eval(user)
        with tracer.start_as_current_span("Get deliveries"):
            if user['id'] is not None:
                if admin(user['role']):
                    get_deliveries_count.inc(1)
                    receipt = receipt_service.delete_receipt(id)
                    return receipt.dict()
            raise HTTPException(403)
    except KeyError:
        raise HTTPException(404, f'Order with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Order with id={id} can\'t be deleted')

@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
