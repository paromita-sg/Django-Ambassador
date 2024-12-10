import decimal
import stripe
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction
from django.core.mail import send_mail


from .serializers import LinkSerializer
from core.models import Link, Order, Product, OrderItems

# Create your views here.

class LinkAPIView(APIView):

    def get(self, _, code=''):
        link = Link.objects.filter(code=code).first()
        serializer = LinkSerializer(link)
        return Response(serializer.data)
    
class OrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        link = Link.objects.filter(code=data['code']).first()

        if not link:
            raise exceptions.APIException('invalid_code')
        
        try:
            order = Order()
            order.code = link.code
            order.user_id = link.user.id
            order.ambassador_email = link.user.email
            order.first_name = data['first_name']
            order.last_name = data['last_name']
            order.email = data['email']
            order.address = data['address']
            order.country = data['country']
            order.city = data['city']
            order.zip = data['zip']
            with transaction.atomic():
                order.save()

            line_items = []

            for item in data['products']:
                product = Product.objects.filter(pk=item['product_id']).first()
                quantity = decimal.Decimal(item['quantity'])

                order_item = OrderItems()
                order_item.order = order
                order_item.product_title = product.title
                order_item.price = product.price
                order_item.quantity = quantity
                order_item.ambassador_revenue = decimal.Decimal(.1) * product.price * quantity
                order_item.admin_revenuw = decimal.Decimal(.9) * product.price * quantity
                with transaction.atomic():
                    order_item.save()

                line_items.append(
                    {
                        'name': product.title,
                        'description': product.description,
                        'images': [
                            product.image
                        ],
                        'amount': int(100 * product.price), # in cents
                        'currency': 'usd',
                        'quantity': quantity
                    }
                )
            
            stripe.api_key = 'sk_test_51PoZcPRxHwFMn04mI3zbwV6NfQFBRydxKnRYGYU2ZK6Q53fDuQhKxaAOuRjHWMjZlNr8s5LI2clsxHfCx1Ehjaav001XsGA34z'

            source = stripe.checkout.Session.create(
                session_url = 'http://localhost:5000/success?source={CHECKOUT_SESSION_ID}',
                cancel_url = 'http://localhost:5000/error',
                payment_method_types=['card'],
                line_items=line_items
            )

            order.transaction_id = source['id']
            order.save()

            return Response(source)
        except Exception as e:
            transaction.rollback()

        return Response({
                'message': 'ERROR OCCURED'
            })


class OrderConfirmAPIView(APIView):
    def post(self, request):
        order = Order.objects.filter(transaction_id=request.data['source']).first()
        if not order:
            raise exceptions.APIException('Order not found')
        
        order.complete = 1
        order.save()

        # Admin Email
        send_mail(
            subject='An order has been completed',
            message='Order #' + str(order.id) + 'with a total of $' + str(order.admin_revenue) + 'has been completed!',
            from_email='from@example.com',
            recipient_list=['admin@admin.com']
        )

        # ambassador Email
        send_mail(
            subject='An order has been completed',
            message='You earned' + str(order.ambassador_revenue) + 'from the link #' + str(order.code),
            from_email='from@example.com',
            recipient_list=[order.ambassador_email]
        )

        return Response({
            'message': 'Order completed'
        })


        





